"""Functions to create donor-receiver pairs using clustering methods.

This function performs donor-receiver pairing based on clustering using
  k-means clustering (method = "kmeans")
  k-medoids clustering (method = "kmedoids")
  HDBSCAN (method = "hdbscan") - Hierarchical Density-Based Spatial Clustering of Applications with Noise.
     Finds core samples of high density and expands clusters from them.
  BIRCH (method = "birch") - Balanced Iterative Reducing & Clustering with Hierarchy. Scalable for large datasets.
     Order of points in the dataset influences the outcome. Hence interactive resampling is implemented here.

Notes:
  1) the clustering is done in multiple rounds to handle data gaps in attributes
  2) snow and non-snow basins are processed separately

"""

import logging
import random
import warnings

import numpy as np
import pandas as pd
from hdbscan import HDBSCAN
from joblib import Parallel, delayed
from sklearn.cluster import Birch, KMeans
from sklearn_extra.cluster import KMedoids

from nwm_region_mgr.parreg import utils_algo
from nwm_region_mgr.parreg.pairer import Pairer

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

logger = logging.getLogger(__name__)


class ClusterPairer(Pairer):
    """Cluster Pairer."""

    @property
    def attrs(self):
        """Attributes."""
        return self.config["attrs"]

    @property
    def receivers(self):
        """All receivers to find donor for."""
        return self.df_attr_all[~self.df_attr_all["is_donor"]]["divide_id"].values

    @property
    def total_number_of_receivers(self):
        """Total number of receivers."""
        return len(self.receivers)

    @property
    def df_attributes(self):
        """Reduce attribute table to the attributes for the current run.

        Note in the attribute table, donors are listed first, followed by receivers.
        """
        return self.df_attr_all[self.config["non_attr_cols"] + self.attrs["main"]]

    def _pair(self):
        """Perform donor-receiver pairing using clustering methods.

        1.  Identify groups of catchments with the same types of attributes.
        2.  Perform dimensionality reduction on the attributes (Principal Component Analysis).
        3.  Further split catchment groups by snow/no snow.
        4.  Apply clustering to pair each receiver catchment with a donor catchment.
        5.  If a receiver is not able to be clustered with a donor, then associate it with the spatially nearest donor in the group.
        """
        np.random.seed(5)
        random.seed(5)
        logger.info(
            f"Total number of receivers to be paired with donors: {self.total_number_of_receivers}"
        )

        processed_receivers_df = pd.DataFrame()

        # iteratively process all the receivers to handle data gaps (because some attributes may be missing for some catchments)
        kround = 0
        processed_receiver_ids = []
        while True:
            kround = kround + 1
            logger.info(f"------------------------ Round {kround}--------------------")

            # when all receivers are paired with donors, exit
            if len(processed_receiver_ids) == self.total_number_of_receivers:
                break

            # determine valid attributes to use this round
            df_attr = utils_algo.get_valid_attrs(
                self.receivers,
                processed_receiver_ids,
                self.df_attributes,
                self.attrs["main"],
                self.config,
            )

            # apply principal component analysis to reduce dimensionality
            df_attr_reduced, _ = utils_algo.apply_pca(
                df_attr.drop(self.config["non_attr_cols"], axis=1)
            )

            # process snowy and non-snowy catchments separately
            processed_receivers_df = self.process_snow_groups(
                df_attr, df_attr_reduced, processed_receivers_df, snowy=True
            )
            processed_receivers_df = self.process_snow_groups(
                df_attr, df_attr_reduced, processed_receivers_df, snowy=False
            )

            processed_receiver_ids = processed_receivers_df["divide_id"].unique()

        return processed_receivers_df

    def process_snow_groups(
        self,
        df_attr: pd.DataFrame,
        df_attr_reduced: pd.DataFrame,
        processed_receivers_df,
        snowy: bool,
    ):
        """Process a group subsetting further by snowy vs non-snowy.

        snowy is a bool
        """
        df_attr_copy = df_attr.copy()
        df_attr_reduced_copy = df_attr_reduced.copy()

        df_attr_reduced.index = df_attr.index
        df_attr_reduced = df_attr_reduced[df_attr["snowy"] == snowy]
        df_attr = df_attr[df_attr["snowy"] == snowy]

        donors = df_attr[df_attr["is_donor"]]["divide_id"].tolist()
        receivers = df_attr[~df_attr["is_donor"]]["divide_id"].tolist()

        if len(donors) == 0 and len(receivers) > 0:
            logger.warning(
                f"No donors available for {len(receivers)} {'snowy' if snowy else 'non-snowy'} catchments in this round."
                f"Select donors from all candidates for these receivers."
            )
            df_attr_reduced = df_attr_reduced_copy.copy()
            df_attr = df_attr_copy.copy()
            donors = df_attr[df_attr["is_donor"]]["divide_id"].tolist()
            receivers = df_attr[~df_attr["is_donor"]]["divide_id"].tolist()

        # remove any receivers that are also donors in df_attr (due to issues with hydrofabric,
        # e.g., two different gages sharing the exact same divides)
        receivers = [cat for cat in receivers if cat not in donors]

        if len(receivers) > 0:
            cat_type = "snowy" if snowy else "non-snowy"
            logger.info(
                f"======= {len(receivers)} {cat_type}  receiver catchments ========"
            )
            logger.debug(f"{cat_type} receiver catchments: {receivers}")

        cgp = ClusterGroupPairer(
            donors,
            receivers,
            df_attr_reduced,
            processed_receivers_df,
            self.config,
            self.dist_spatial,
            self.df_attr_all,
            self._apply_algorithm,
        )
        return cgp.process_group()


class ClusterGroupPairer:
    """Cluster Group Pairer."""

    def __init__(
        self,
        donors: pd.DataFrame,
        receivers: pd.DataFrame,
        df_attr_reduced: pd.DataFrame,
        processed_receivers_df: pd.DataFrame,
        config: dict,
        dist_spatial: pd.DataFrame,
        df_attr_all: pd.DataFrame,
        _apply_algorithm,
    ):
        """Initialize Cluster Group Pairer."""
        self.donors = donors
        self.receivers = receivers
        self.df_attr_reduced = df_attr_reduced
        self.processed_receivers_df = processed_receivers_df
        self.config = config
        self.dist_spatial = dist_spatial
        self.df_attr_all = df_attr_all
        self._apply_algorithm = _apply_algorithm

    @property
    def receivers_to_be_processed_for_group(self) -> list:
        """Get receivers that need to be processed."""
        if len(self.processed_receivers_df) == 0:
            return self.receivers
        else:
            return [
                x
                for x in self.receivers
                if x not in self.processed_receivers_df["divide_id"].tolist()
            ]

    @property
    def initial_labels(self) -> np.array:
        """Get initial labels."""
        # define starting labels
        labels = np.zeros(
            len(self.df_attr_reduced)
        )  # start with a single cluster (label = 0)

        # for those already processed, assign "label_done"
        if self.processed_receivers_df.shape[0] > 0:
            labels[
                [
                    self.number_of_donors + self.receivers.index(x)
                    for x in self.receivers
                    if x in self.processed_receiver_ids
                ]
            ] = self.label_done  # label = -99 indicates donor identified
        return labels

    @property
    def processed_receiver_ids(self):
        """Ids of receivers that have already been processed."""
        return self.processed_receivers_df["divide_id"].to_list()

    @property
    def number_of_donors(self) -> int:
        """Number of donors for this grouping."""
        return len(self.donors)

    @property
    def label_done(self) -> int:
        """Label = -99 indicates donor identified."""
        return -99

    def get_receiver_label(self, labels: np.array) -> np.array:
        """Receiver_label."""
        receiver_label = np.unique(labels[self.number_of_donors :], return_counts=False)
        label1 = receiver_label[receiver_label != self.label_done]
        return label1

    def njob(self, labels) -> int:
        """Get number of jobs."""
        njob = self.config["njobs"]
        if njob > len(self.get_receiver_label(labels)):
            njob = len(self.get_receiver_label(labels))
        return njob

    def update_processed_receivers_and_labels(
        self,
        pairing_results: list,
        processed_receivers_for_group_df: pd.DataFrame,
        labels: np.array,
    ) -> tuple:
        """Update donors and labels."""
        for result, result_labels in pairing_results:
            processed_receivers_for_group_df = pd.concat(
                (processed_receivers_for_group_df, result), axis=0
            )

            # get unique labels from clustering results
            label_rec1 = np.unique(
                result_labels[self.number_of_donors :], return_counts=False
            )

            # for each unique label from clustering results update the final label list
            label_rec1 = label_rec1[label_rec1 != 0]
            for l1 in label_rec1:
                if l1 == self.label_done:
                    # if clustering results label is marked done update the final label list as done
                    labels = np.where(result_labels == l1, self.label_done, labels)
                else:
                    # if not done create new unique label value in final label list
                    labels = np.where(result_labels == l1, labels.max() + 1, labels)
        return processed_receivers_for_group_df, labels

    def update_iteration(
        self,
        iteration: int,
        processed_receivers_for_group_df: pd.DataFrame,
        number_of_receivers_with_donor: int,
    ) -> int:
        """Update the iteration based on number of receivers with donors and receivers that have already been processed."""
        if number_of_receivers_with_donor != processed_receivers_for_group_df.shape[0]:
            return 0
        else:
            return iteration + 1

    def check_convergence(
        self, iteration: int, number_of_receivers_with_donor: int
    ) -> bool:
        """Check for convergence.

        If the number of receivers with donors identified has not changed for a number of iterations,
        or if the number of receivers without donors identified becomes really small,
        consider the algorithm converging.
        """
        if (
            (iteration > 50)
            | (
                number_of_receivers_with_donor
                / len(self.receivers_to_be_processed_for_group)
                * 100
                > 98
            )
            | (len(self.receivers_to_be_processed_for_group) < 5)
        ):
            return True

    def get_receivers_for_proximity_algorithm(
        self,
        processed_receivers_for_group_df: pd.DataFrame,
    ) -> list:
        """Get receivers that did not converge (to be processed with the proximity algorithm)."""
        if processed_receivers_for_group_df.shape[0] == 0:
            return self.receivers_to_be_processed_for_group.copy()
        else:
            return [
                x
                for x in self.receivers_to_be_processed_for_group
                if x not in processed_receivers_for_group_df["divide_id"].tolist()
            ]

    def apply_proximity_algorithm(
        self,
        receivers_for_proximity_algorithm: pd.DataFrame,
        processed_receivers_for_group_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Apply proximity algorithm."""
        logger.info(
            f"Algorithm converged without donors identified for {len(receivers_for_proximity_algorithm)} receivers ... "
            f"use proximity for these receivers"
        )
        proximity_results = utils_algo.assign_donors(
            "proximity",
            self.donors,
            receivers_for_proximity_algorithm,
            self.config,
            None,
            self.dist_spatial,
            self.df_attr_all,
        )

        processed_receivers_for_group_df = pd.concat(
            [processed_receivers_for_group_df, proximity_results],
            axis=0,
        )

        return processed_receivers_for_group_df

    def process_group(
        self,
    ) -> pd.DataFrame:
        """Process a group of receivers.

        Iterate through all receivers to be processed for this group until all receivers in
        the group have been processed.
        """
        if len(self.receivers_to_be_processed_for_group) == 0:
            return self.processed_receivers_df

        # identify donors iteratively
        # data frame to hold donor table for the current snowy group
        processed_receivers_for_group_df = pd.DataFrame()
        iter1 = iter2 = 0
        number_of_receivers_with_donor = processed_receivers_for_group_df.shape[0]
        labels = self.initial_labels
        while len(processed_receivers_for_group_df) < len(
            self.receivers_to_be_processed_for_group
        ):
            iter1 += 1
            logger.debug(f"===== iter1= {iter1} ======")
            logger.debug(f"Using {self.njob(labels)} processors ...")

            # iterate through all clusters, break the cluster if necessary, or choose donors if the cluster is no longer breakable
            # each tuple in pairing_results is a result of cluster ll from the previous iteration being split into smaller clusters
            pairing_results = Parallel(n_jobs=self.njob(labels))(
                delayed(self.identify_donor_by_cluster)(
                    ll, labels, processed_receivers_for_group_df
                )
                for ll in self.get_receiver_label(labels)
            )

            # update donors and labels
            processed_receivers_for_group_df, labels = (
                self.update_processed_receivers_and_labels(
                    pairing_results, processed_receivers_for_group_df, labels
                )
            )

            # update iter2 as necessary
            iter2 = self.update_iteration(
                iter2, processed_receivers_for_group_df, number_of_receivers_with_donor
            )
            if iter2 != 0:
                # check convergence
                if self.check_convergence(iter2, number_of_receivers_with_donor):
                    # get receivers for proximity algorithm
                    receivers_for_proximity_algorithm = (
                        self.get_receivers_for_proximity_algorithm(
                            processed_receivers_for_group_df
                        )
                    )
                    if len(receivers_for_proximity_algorithm) > 0:
                        # apply proximity algorithm
                        processed_receivers_for_group_df = (
                            self.apply_proximity_algorithm(
                                receivers_for_proximity_algorithm,
                                processed_receivers_for_group_df,
                            )
                        )
                    # break

            # update progress
            self.update_progress(iter1, processed_receivers_for_group_df)

            # update number of receivers with donors identified
            number_of_receivers_with_donor = processed_receivers_for_group_df.shape[0]

        # add to the final donor table
        return pd.concat(
            (self.processed_receivers_df, processed_receivers_for_group_df), axis=0
        )

    def update_progress(
        self, iter1: int, processed_receivers_for_group_df: pd.DataFrame
    ) -> None:
        """Update progress on donor-receiver pairing."""
        if iter1 > 1:
            logger.info(
                f"iteration = {iter1 - 1}, "
                f"number of receivers with donors identified = {processed_receivers_for_group_df.shape[0]}"
            )
            if processed_receivers_for_group_df.shape[0] > 0:
                uniq, freq = np.unique(
                    processed_receivers_for_group_df["tag"], return_counts=True
                )
                logger.debug(dict(zip(uniq, freq)))

    def cluster_donors_receivers(self, receiver_label, labels: np.array):
        """Return the donors and receivers for the current cluster."""
        donors = [x for i, x in enumerate(self.donors) if labels[i] == receiver_label]
        receivers = [
            x
            for i, x in enumerate(self.receivers)
            if labels[i + len(self.donors)] == receiver_label
        ]
        return donors, receivers

    def get_receivers_to_be_processed(
        self, processed_receivers_for_group_df: pd.DataFrame, cluster_receivers: list
    ) -> list:
        """Receivers in the current cluster that still need to be processed."""
        if len(processed_receivers_for_group_df) == 0:
            if len(self.processed_receivers_df) == 0:
                processed_ids = []
            else:
                processed_ids = self.processed_receivers_df["divide_id"].tolist()
        else:
            if len(self.processed_receivers_df) == 0:
                processed_ids = processed_receivers_for_group_df["divide_id"].tolist()
            else:
                processed_ids = set(
                    processed_receivers_for_group_df["divide_id"].tolist()
                    + self.processed_receivers_df["divide_id"].tolist()
                )
        if len(processed_ids) > 0:
            return [x for x in cluster_receivers if x not in processed_ids]
        else:
            return cluster_receivers.copy()

    def get_cluster_df_attr_reduced(self, cluster_df_attr_reduced_index: list):
        """Get cluster df_attr_reduced."""
        return self.df_attr_reduced.iloc[cluster_df_attr_reduced_index]

    def get_cluster_df_attr_reduced_index(
        self, cluster_donors: list, cluster_receivers: list
    ):
        """Get cluster df_attr_reduced index."""
        idx1 = [self.donors.index(x) for x in cluster_donors]
        idx2 = [self.receivers.index(x) for x in cluster_receivers]
        return idx1 + [x + len(self.donors) for x in idx2]

    def update_fit_labels(self, fit):
        """Update fit labels."""
        fit.labels_ = (
            fit.labels_ + 2
        )  # add 2 to the cluster labels because hdbscan cluster starts with -1
        return fit

    def get_cluster_receiver_donor_labels(
        self, fit: KMeans | KMedoids | HDBSCAN | Birch, cluster_donors: list
    ):
        """Get cluster labels for receivers and donors."""
        cluster_receiver_labels = np.unique(
            fit.labels_[len(cluster_donors) :], return_counts=False
        )  # receiver clusters
        cluster_donor_labels = np.unique(
            fit.labels_[: len(cluster_donors)], return_counts=False
        )  # donor clusters
        return cluster_receiver_labels, cluster_donor_labels

    def apply_clustering(
        self, cluster_donors: list, cluster_receivers: list, cluster_labels: np.array
    ):
        """Apply clustering algorithm.

        1.  Apply clustering alogrithm.
        2.  Update labels for clusters.
        3.  Identinfy receivers that are in clusters with no donors.
        4.  Assign donorless receivers a donor from the parent cluster (from the previous iteration).
        5.  Update labels for this cluster iteration.
        """
        # apply clustering
        cluster_df_attr_reduced_index = self.get_cluster_df_attr_reduced_index(
            cluster_donors, cluster_receivers
        )
        cluster_df_attr_reduced = self.get_cluster_df_attr_reduced(
            cluster_df_attr_reduced_index
        )
        fit = self._apply_algorithm(
            cluster_df_attr_reduced, cluster_receivers, cluster_donors
        )

        # update labels
        fit = self.update_fit_labels(fit)
        cluster_labels[cluster_df_attr_reduced_index] = fit.labels_
        cluster_receiver_labels, cluster_donor_labels = (
            self.get_cluster_receiver_donor_labels(fit, cluster_donors)
        )

        # for receivers in clusters without donors, or clusters that cannot be subset further,
        # choose donors from those in the parent cluster (donors1)
        cluster_receiver_labels_with_no_donor_in_cluster = [
            x for x in cluster_receiver_labels if x not in cluster_donor_labels
        ]
        if (
            (len(cluster_receiver_labels) == 1)
            and (len(cluster_donor_labels) == 1)
            and (cluster_donor_labels[0] == cluster_receiver_labels[0])
        ):
            cluster_receiver_labels_with_no_donor_in_cluster = cluster_receiver_labels

        # get receivers with with no donor in cluster
        if len(cluster_receiver_labels_with_no_donor_in_cluster) > 0:
            recs3 = [
                x
                for ii, x in enumerate(cluster_receivers)
                if fit.labels_[len(cluster_donors) :][ii]
                in cluster_receiver_labels_with_no_donor_in_cluster
            ]

            cluster_labels[
                [self.receivers.index(x) + len(self.donors) for x in recs3]
            ] = self.label_done

            return utils_algo.assign_donors(
                "main",
                cluster_donors,
                recs3,
                self.config,
                None,
                self.dist_spatial,
                self.df_attr_all,
            ), cluster_labels
        else:
            return pd.DataFrame(), cluster_labels

    def identify_donor_by_cluster(
        self,
        receiver_label: int,
        labels: np.array,
        processed_receivers_for_group_df: pd.DataFrame,
    ):
        """Identify donor using clustering if possible, otherwise use spatial proximity.

        1.  Check if there are any donors in the cluster; if there are move to step 2.
            If there are no donors in the cluster choose from all donors based on spatial proximity

        2.  If number of donors in the cluster is larger than the defined 'nDonorMax',
            break the cluster into multiple clusters using the dimensionally reduced attributes.
            If the number of donors in the cluster is smaller than defined 'nDonorMax', do not
            perform further clustering; simply identify donors.
        """
        cluster_labels = np.zeros(self.df_attr_reduced.shape[0])

        # donors and receivers in the current cluster
        cluster_donors, cluster_receivers = self.cluster_donors_receivers(
            receiver_label, labels
        )

        # receivers in the current cluster that still need to be processed
        receivers_to_be_processed = self.get_receivers_to_be_processed(
            processed_receivers_for_group_df, cluster_receivers
        )

        # if there exist donors in the cluster
        if len(cluster_donors) > 0:
            # if number of donors in the cluster is larger than the defined 'nDonorMax', proceed to break the cluster further down
            if len(cluster_donors) > self.config["n_donor_max"]:
                return self.apply_clustering(
                    cluster_donors, cluster_receivers, cluster_labels
                )

            else:
                # for receivers in clusters with number of donors smaller than 'n_donor_max', no further clustering is needed
                # identify donors from the current cluster
                cluster_labels[labels == receiver_label] = self.label_done
                return utils_algo.assign_donors(
                    "main",
                    cluster_donors,
                    receivers_to_be_processed,
                    self.config,
                    None,
                    self.dist_spatial,
                    self.df_attr_all,
                ), cluster_labels
        # for receivers in clusters without donors, choose from all donors based on spatial proximity
        else:
            cluster_labels[labels == receiver_label] = self.label_done
            return utils_algo.assign_donors(
                "proximity",
                self.donors,
                receivers_to_be_processed,
                self.config,
                None,
                self.dist_spatial,
                self.df_attr_all,
            ), cluster_labels


class KmeansPairer(ClusterPairer):
    """Kmeans Pairer.

    A class for pairing donor-receiver catchments using sklearn's KMeans.
    https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans.fit
    """

    def pair(self):
        """Pair the donor-receiver using Kmeans."""
        logger.info("perform clustering using Kmeans approach ...")
        return self._pair()

    def _apply_algorithm(
        self, df_attr_reduced: pd.DataFrame, receivers: list, donors: list
    ) -> KMeans:
        """Apply Kmeans alogrithm."""
        return KMeans(
            init=self.config["init"],
            n_clusters=2,
            n_init=self.config["n_init"],
            max_iter=self.config["n_iter_max"],
            random_state=42,
        ).fit(df_attr_reduced)


class KmedoidsPairer(ClusterPairer):
    """KMedoids Pairer.

    A class for pairing donor-receiver catchments using sklearn_extra's KMedoids.
    https://scikit-learn-extra.readthedocs.io/en/stable/generated/sklearn_extra.cluster.KMedoids.html
    """

    def pair(self):
        """Pair the donor-receiver using KMedoids."""
        logger.info("perform clustering using KMedoids approach ...")
        return self._pair()

    def _apply_algorithm(
        self, df_attr_reduced: pd.DataFrame, receivers: list, donors: list
    ) -> KMedoids:
        """Apply KMedoids alogrithm."""
        return KMedoids(
            init=self.config["init"],
            n_clusters=2,
            max_iter=self.config["n_iter_max"],
            random_state=42,
        ).fit(df_attr_reduced)


class HDBSCANPairer(ClusterPairer):
    """HDBSCAN Pairer.

    A class for pairing donor-receiver catchments using hdbscan's HDBSCAN.
    https://hdbscan.readthedocs.io/en/latest/
    """

    def pair(self):
        """Pair the donor-receiver using HDBSCAN."""
        logger.info("perform clustering using HDBSCAN approach ...")
        return self._pair()

    def _apply_algorithm(
        self, df_attr_reduced: pd.DataFrame, receivers: list, donors: list
    ) -> HDBSCAN:
        """Apply HDBSCAN alogrithm."""
        return HDBSCAN(
            min_samples=11,
            min_cluster_size=self.config["min_cluster_size"],
            allow_single_cluster=False,
        ).fit(df_attr_reduced)


class BIRCHPairer(ClusterPairer):
    """BIRCH Pairer.

    A class for pairing donor-receiver catchments using sklearn's Birch.
    https://scikit-learn.org/stable/modules/generated/sklearn.cluster.Birch.html
    """

    def pair(self):
        """Pair the donor-receiver using BIRCH."""
        logger.info("perform clustering using BIRCH approach ...")
        return self._pair()

    def _apply_algorithm(
        self, df_attr_reduced: pd.DataFrame, receivers: list, donors: list
    ) -> Birch:
        """Apply BIRCH algorithm."""
        # explore a range of threshold values to identify a proper threshold parameter for BIRCH
        iteration_count = 0
        for thresh in np.arange(
            self.config["min_thresh"], self.config["max_thresh"] + 0.1, 0.1
        ):
            # shuffle the donor/receiver positions in the data to get optimal results, via resampling
            kk = 0
            while kk < self.config["max_resample"]:
                iteration_count += 1
                kk = kk + 1
                df_attr_reduced_reordered = df_attr_reduced.sample(
                    frac=1, random_state=iteration_count
                )  # reorder the data
                fit = Birch(
                    branching_factor=self.config["branching_factor"],
                    n_clusters=None,
                    threshold=thresh,
                ).fit(df_attr_reduced_reordered)
                fit.labels_ = fit.labels_[
                    [
                        df_attr_reduced_reordered.index.get_loc(x)
                        for x in df_attr_reduced.index
                    ]
                ]
                u1 = np.unique(fit.labels_[: len(donors)], return_counts=False)
                n_clust = len(np.unique(fit.labels_, return_counts=False))
                nrec_donor = sum(np.in1d(fit.labels_[len(donors) :], u1))

                # if a donor is identified for all receivers, quit the iteration loop
                if (n_clust > 1) and (nrec_donor == len(receivers)):
                    break

            if (n_clust > 1) and (nrec_donor == len(receivers)):
                break
        return fit
