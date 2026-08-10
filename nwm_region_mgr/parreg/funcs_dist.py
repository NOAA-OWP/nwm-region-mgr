"""Function to create donor-receiver pairs using distance methods.

This function performs donor-receiver pairing using either Gower's distance (method = "gower") or
  the distance computed by unsupervised random forest classification (method = "urf")

"""

import logging
import random
import time

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from nwm_region_mgr.parreg import utils_algo
from nwm_region_mgr.parreg.pairer import Pairer
from nwm_region_mgr.parreg.unsupervised_random_forest import URF

logger = logging.getLogger(__name__)


class DistancePairer(Pairer):
    """Distance Pairer."""

    @property
    def attrs(self):
        """Attributes"""
        return {
            "main": self.config["attrs"]["main"],
            "base": self.config["attrs"]["base"],
        }

    def get_receivers_to_process(self, processed_receivers_df: pd.DataFrame) -> list:
        """Receivers that still need to be processed."""
        # check if donors are identified for all receivers
        recs = self.df_attr_all[~self.df_attr_all["is_donor"]]["divide_id"].values
        # logger.info(f"Number of already processed receivers: {len(processed_receivers_df)}")
        if len(processed_receivers_df) > 0:
            return [
                value
                for value in recs
                if value not in processed_receivers_df["divide_id"].values
            ]
        else:
            return recs

    def get_donors_in_receivers_snow_category(
        self, df_attr_for_round: pd.DataFrame, receiver: str
    ) -> list:
        """Get all donors in the same snow category as the receiver."""
        snow_category_of_receiver = df_attr_for_round.loc[
            (df_attr_for_round["divide_id"] == receiver)
            & (~df_attr_for_round["is_donor"]),
            "snowy",
        ]
        return df_attr_for_round[
            (df_attr_for_round["is_donor"])
            & (df_attr_for_round["snowy"] == snow_category_of_receiver.iloc[0])
        ]["divide_id"].to_list()

    def apply_constraints(
        self,
        receiver: str,
        candidate_donors_for_round: list,
        dist_attr_for_round: pd.DataFrame,
        donors_for_round: list,
    ) -> tuple:
        """Find donors within the defined buffer iteratively so that closest donors with attr distance below the predefined value can be found.

        1.  Set a buffer distance.
        2.  Filter candidate donors by zero_spa_dist (spatial filter).
        3.  If donors remain after filtering by zero_spa_dist, select the nearest donor. Otherwise filter using the buffer.
        4.  Ensure the identified donor is from the same snow group as the receiver.
        5.  Filter candidate donors by max_attr_dist (attribute distance filter).
        6.  Ensure that the minimum attribute distance for the donor is less than min_attr_dist.
        7.  If no donors meet all constraints/filters, set a new buffer distance and try again.
        """
        buffer = self.config["min_spa_dist"] - 100  # unit: km
        while buffer < self.config["max_spa_dist"] - 100:
            buffer = buffer + 100

            # if there exists donor catchment within a short distance,
            distances_to_donors = self.dist_spatial.loc[receiver]
            donors_within_spatial_distance = distances_to_donors.loc[
                distances_to_donors <= self.config["zero_spa_dist"]
            ].index.tolist()

            # select that catchment as donor; (list of one donor)
            if len(donors_within_spatial_distance) > 0:
                # select that catchment as donor;
                donors = [distances_to_donors[donors_within_spatial_distance].idxmin()]
            else:
                # otherwise, narrow down to donors within the buffer
                donors = distances_to_donors.loc[
                    distances_to_donors <= buffer
                ].index.tolist()

            # potential donors in the same snowy category
            donors = list(set(donors).intersection(set(candidate_donors_for_round)))
            donors.sort()
            # potential donors with dist <= maxAttrDist
            attr_distance_to_current_donors = dist_attr_for_round.loc[receiver, donors]
            idx = [
                i
                for i in attr_distance_to_current_donors.index
                if attr_distance_to_current_donors[i] <= self.config["max_attr_dist"]
            ]
            if (
                len(idx) == 0
            ):  # if not, continue to the next round with a larger neighborhood
                continue

            # if a suitable donor is found (or all donors have been assessed), break the loop and stop searching
            if attr_distance_to_current_donors[idx].min() <= self.config[
                "min_attr_dist"
            ] or len(donors) == len(donors_for_round):
                return donors, attr_distance_to_current_donors.loc[idx]

        return [], []

    def identify_donor_slow(
        self,
        receiver: str,
        donors_for_round: list,
        df_attr_for_round: pd.DataFrame,
        dist_attr_for_round: pd.DataFrame,
        run: str,
    ) -> pd.DataFrame:
        """Identify donors (to be used in parallel computing)."""
        processed_receivers_round_df = pd.DataFrame()

        candidate_donors_for_round = self.get_donors_in_receivers_snow_category(
            df_attr_for_round, receiver
        )

        filtered_donors, attr_distance_to_current_donors = self.apply_constraints(
            receiver, candidate_donors_for_round, dist_attr_for_round, donors_for_round
        )

        # if donors are identified
        if len(filtered_donors) > 0:
            # narrow down to those that satisfy the maxAttrDist threshold
            donors = attr_distance_to_current_donors.index.tolist()

            # assign donor
            processed_receivers_round_df = pd.concat(
                (
                    processed_receivers_round_df,
                    utils_algo.assign_donors(
                        run,
                        donors,
                        [receiver],
                        self.config,
                        attr_distance_to_current_donors,
                        self.dist_spatial,
                        self.df_attr_all,
                    ),
                ),
                axis=0,
            )

        return processed_receivers_round_df

    def update_columns_index(
        self, donors_for_round: list, receivers_for_round: list, dist_attr: pd.DataFrame
    ) -> pd.DataFrame:
        """Update the columns and index for distance attributes."""
        dist_attr.columns = donors_for_round
        dist_attr.index = receivers_for_round
        return dist_attr.round(3)

    def get_receivers_to_process_for_round(
        self,
        receivers_to_process: list,
        processed_receivers_for_round: list,
        receivers_for_round: list,
    ) -> list:
        """Determine which receivers to be processed for the current round.

        process only those not-yet processed receivers.
        """
        receivers_to_process = [
            r
            for r in receivers_to_process
            if r in receivers_for_round and r not in processed_receivers_for_round
        ]

        logger.info(f"{len(receivers_to_process)} receivers to be processed this round")
        return receivers_to_process

    def pair(self):
        """Perform donor-receiver pairing using Gower's distance or URF approach."""
        np.random.seed(5)
        random.seed(5)

        processed_receivers_df = pd.DataFrame()

        # two rounds of processing, first with attributes defined by the selected scenario (e.g., 'hlr'),
        # and then with 'base' attrs for catchments with no donors found in the 1st round
        for run in self.attrs:  # attr round
            receivers_to_process = self.get_receivers_to_process(processed_receivers_df)
            if len(receivers_to_process) == 0:
                continue

            logger.info(
                f"Number of receivers to be processed in {run} attributes: {len(receivers_to_process)}"
            )

            # reduce the attribute table to attributes for the current attr round
            logger.info(f"Using {run} attributes: {self.attrs[run]}")
            df_attr0 = self.df_attr_all[self.config["non_attr_cols"] + self.attrs[run]]

            # iteratively process all the receivers to handle data gaps so that
            # receivers with the same missing attributes are processed in the same round
            processed_receivers_for_round = []  # receivers that have already been processed in previous krounds
            kround = 0
            while len(
                [x for x in receivers_to_process if x in processed_receivers_for_round]
            ) != len(receivers_to_process):
                kround = kround + 1
                logger.info(
                    f"------------------------{run} attributes,  Round {kround}--------------------"
                )

                # figure out valid attributes to use this round
                df_attr_for_round = utils_algo.get_valid_attrs(
                    receivers_to_process,
                    processed_receivers_for_round,
                    df_attr0,
                    self.attrs[run],
                    self.config,
                )
                # donors and receivers for this round
                donors_for_round = df_attr_for_round[df_attr_for_round["is_donor"]][
                    "divide_id"
                ].tolist()
                receivers_for_round = df_attr_for_round[~df_attr_for_round["is_donor"]][
                    "divide_id"
                ].tolist()

                # apply principal component analysis and compute distances
                dist_attr_for_round = self.process(
                    df_attr_for_round, donors_for_round, receivers_for_round
                )
                dist_attr_for_round = self.update_columns_index(
                    donors_for_round, receivers_for_round, dist_attr_for_round
                )

                # determine which receivers to be processed for the current round
                # process only those not-yet processed receivers
                receivers_to_process_for_round = (
                    self.get_receivers_to_process_for_round(
                        receivers_to_process,
                        processed_receivers_for_round,
                        receivers_for_round,
                    )
                )

                processed_receivers_round_df = Parallel(n_jobs=self.config["njobs"])(
                    delayed(self.identify_donor_slow)(
                        receiver,
                        donors_for_round,
                        df_attr_for_round,
                        dist_attr_for_round,
                        run,
                    )
                    for receiver in receivers_to_process_for_round
                )
                processed_receivers_round_df = pd.concat(
                    processed_receivers_round_df, axis=0
                )
                logger.info(
                    f"Number of processed receivers in this round: {len(processed_receivers_round_df)}"
                )

                # update list of processed receivers for this round
                processed_receivers_for_round += receivers_to_process_for_round

                # update processed receivers df
                processed_receivers_df = pd.concat(
                    (processed_receivers_df, processed_receivers_round_df), axis=0
                )
                logger.info(
                    f"Number of processed receivers after {run} attributes: {len(processed_receivers_df)}"
                )

        return processed_receivers_df


class GowerPairer(DistancePairer):
    """Pairer using Gower distance."""

    @property
    def method(self):
        """Method."""
        return "gower"

    def process(
        self,
        df_attr_for_round: pd.DataFrame,
        donors_for_round: list,
        receivers_for_round: list,
    ):
        """Process data."""
        df_attr_reduced, weights = utils_algo.apply_pca(
            df_attr_for_round.drop(self.config["non_attr_cols"], axis=1)
        )

        time1 = time.time()
        # compute Gower's distance between donors and receivers only, i.e., avoid calculating distance
        # between donors and donors, receivers and receivers (faster)
        number_of_donors = len(donors_for_round)
        number_of_receivers = len(receivers_for_round)

        range_of_reduced_attr = df_attr_reduced.max() - df_attr_reduced.min()
        range_array = np.repeat(
            np.matrix(range_of_reduced_attr), number_of_receivers, axis=0
        )

        weights_array = np.repeat(np.matrix(weights), number_of_receivers, axis=0)

        df_attr_reduced_receiver = df_attr_reduced.iloc[number_of_donors:]

        dist_attr_for_round = Parallel(n_jobs=self.config["njobs"])(
            delayed(self.compute_gower_distance_slow)(
                i,
                df_attr_reduced,
                df_attr_reduced_receiver,
                range_array,
                weights_array,
                number_of_receivers,
            )
            for i in range(number_of_donors)
        )
        dist_attr_for_round = pd.concat(dist_attr_for_round, axis=1)

        logger.info(
            f"Time consumed for distance calculation using Gower's distance is : --- {time.time() - time1} seconds ---"
        )
        return dist_attr_for_round

    def compute_gower_distance_slow(
        self,
        i,
        df_attr_reduced,
        df_attr_reduced_receiver,
        range_array,
        weights_array,
        number_of_receivers,
    ):
        """Calculate Gower's distance between donors and receivers (to be used in parallel computing)."""
        scores_donor = np.repeat(
            np.matrix(df_attr_reduced.iloc[i]), number_of_receivers, axis=0
        )
        return (
            (scores_donor - df_attr_reduced_receiver).abs()
            / range_array
            * weights_array
        ).sum(axis=1)


class URFPairer(DistancePairer):
    """Pairer using Unsupervised Random Forest (URF) distance."""

    @property
    def method(self):
        """Method."""
        return "urf"

    def process(
        self,
        df_attr_for_round: pd.DataFrame,
        donors_for_round: list,
        receivers_for_round: list,
    ) -> pd.DataFrame:
        """Process data for a single regionalization round."""
        # PCA or pass-through
        if not self.config["pca"]:
            df_attr_reduced = df_attr_for_round.drop(
                self.config["non_attr_cols"], axis=1
            )
        else:
            df_attr_reduced, _ = utils_algo.apply_pca(
                df_attr_for_round.drop(self.config["non_attr_cols"], axis=1)
            )

        # Compute row positions for donors & receivers
        num_donors = len(donors_for_round)
        num_total = len(df_attr_for_round)
        donor_idx = np.arange(num_donors)
        receiver_idx = np.arange(num_donors, num_total)

        # Distance calculation (optimized)
        logger.info("Computing URF attribute distance...")
        t0 = time.time()

        rf1 = URF(n_trees=self.config["n_trees"], max_depth=self.config["max_depth"])

        x = df_attr_reduced.to_numpy()  # convert dataframe to numpy for efficiency
        dist_block = rf1.get_distance(
            x,
            njob=self.config["njobs"],
            donor_idx=donor_idx,
            receiver_idx=receiver_idx,
        )

        # Wrap result in DataFrame
        out = pd.DataFrame(
            dist_block,
            index=receivers_for_round,
            columns=donors_for_round,
        )

        logger.info(f"URF distance block computed in {time.time() - t0:.2f} seconds")

        return out


class ProximityPairer(Pairer):
    """Pairer using proximity."""

    @property
    def recs0(self):
        """Receivers."""
        return self.df_attr_all[~self.df_attr_all["is_donor"]]["divide_id"].tolist()

    @property
    def donors0(self):
        """Donors."""
        return self.df_attr_all[self.df_attr_all["is_donor"]]["divide_id"].tolist()

    def pair(self, donors=None, receivers=None):
        """Perform donor-receiver pairing using proximity."""
        donors = donors or self.donors0
        receivers = receivers or self.recs0
        return utils_algo.assign_donors(
            "proximity",
            donors,
            receivers,
            self.config,
            None,
            self.dist_spatial,
            None,
        )
