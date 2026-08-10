"""Process configuration to perform parameter regionalization.

process_config.py

Functions:
- run_parreg_for_vpu: Run the parameter regionalization process for a given VPU.
- set_vpu: Set the VPU for processing.
- get_donors_receivers: Get the donors and receivers for a given VPU from the config.
- get_initial_donor_df: Get initial donor gage/catchment df (before screening with stats) for a specific VPU.
- donor_receiver_gdfs: Get the donor and receiver GeoDataFrames for a given VPU.
- update_spatial_distance_donors: Update existing dataframe for pairwise spatial distance to include new donors.
- update_spatial_distance_receivers: Update existing dataframe for pairwise spatial distance to include new receivers.
- compute_donor_receiver_spatial_distance: Compute spatial distance between donors and receivers.
- write_spatial_file: Save the spatial distance data.
- generate_pairing: Generate pairings based on the spatial distance and attributes.
- process_attr_data: Process attribute data for donors and receivers.
- set_snow_flag: Set the snow flag in the attribute data.
- build_hydrofabric_path: Build hydrofabric path for a given VPU.
- donors_df: Get the donors DataFrame.
- donors_gdf: Get the donors GeoDataFrame.
- hydrofabric_gdf: Get the hydrofabric GeoDataFrame.
- hydrofabric_gdf_3857: Get the hydrofabric GeoDataFrame projected to EPSG:3857.
- donor_gdf_3857: Get the donors GeoDataFrame projected to EPSG:3857.
- combined_geom: Get the combined geometry of the hydrofabric.
- hydrofabric_buffered_polygon: Get the buffered hydrofabric polygon.
- donor_basins: Get the donor basins for a given VPU.
- donor_basins_all: Get all donor basins from the calibration parameter file.
- donors: Get the list of donor IDs.
- receivers: Get the list of receiver IDs.
- number_of_donors: Get the number of donors.
- number_of_receiver: Get the number of receivers.
- dist_file: Build the path for the spatial distance file.
- dist_spatial: Get the spatial distance DataFrame.
- set_formulation_dict: Set the {formulation: catchments} dictionary.
- get_base_attr_list_all: Get the base attribute list from all datasets.
- df_attrs_all: Get the DataFrame containing all attributes.
- datasets: Get the list of datasets from the config.

"""

import logging
import time
from functools import cached_property, lru_cache, reduce
from pathlib import Path
from typing import Any, Tuple

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Point, Polygon

from nwm_region_mgr.formreg.process_config import (
    FormulationRegionalizationProcessor as FRP,
)
from nwm_region_mgr.parreg import plot_outputs as po
from nwm_region_mgr.parreg import utils_algo
from nwm_region_mgr.parreg.funcs_clust import (
    BIRCHPairer,
    HDBSCANPairer,
    KmeansPairer,
    KmedoidsPairer,
)
from nwm_region_mgr.parreg.funcs_dist import GowerPairer, ProximityPairer, URFPairer
from nwm_region_mgr.utils import BaseConfigProcessor, read_table, save_data

logger = logging.getLogger(__name__)


class ParameterRegionalizationProcessor(BaseConfigProcessor):
    """Regionalization Processor."""

    def set_vpu(self, vpu: str):
        """Set the vpu."""
        self.vpu = vpu
        self.donor_receiver_gdfs.cache_clear()
        if "formulation_dict" in self.__dict__:
            del self.__dict__["formulation_dict"]

    def run_parreg_for_vpu(self, vpu: str, frp: FRP) -> None:
        """Run the parameter regionalization process for a given VPU."""
        # set the VPU for processing
        self.set_vpu(vpu)

        # if pair files already exist for all pairing algorithms, skip the process
        co = getattr(self.config.output, "pairs", None)
        if co is None:
            logger.warning("No 'pairs' section found in output config.")
            return

        all_exist = True  # Assume all exist until proven otherwise
        for pairer_name in self.pairer_names:
            outfile = co.get_file_path(vpu=self.vpu, algorithm=pairer_name)
            if not outfile.exists():
                all_exist = False
                logger.info(
                    f"Missing pair file for VPU {self.vpu}, algorithm {pairer_name}. Will proceed."
                )
                break  # No need to check further, we know not all exist

        if all_exist:
            logger.info(
                f"All pair files already exist for VPU {self.vpu}, skipping parameter regionalization."
            )
            return

        logger.info(
            f"========= Processing parameter regionalization for VPU: {vpu} ========="
        )

        # get donors and receivers
        with self.timing_block("get_donors_receivers"):
            self.get_donors_receivers()

        # run formulation regionalization for all donor VPUs
        for vpu1 in self.donor_vpus:
            frp.expand_config_for_vpu(vpu1)
            formulation_file = frp.get_output_file_path(
                "formulation",
                vpu1,
                use_stem_suffix=True,
            )
            frp.run_formreg_for_vpu(vpu1, formulation_file)

        # process attribute data
        with self.timing_block("process_attr_data"):
            self.process_attr_data()

        # set snow flag
        snow_file = self.config.snow_cover.snow_cover_file.get(self.vpu, None)
        df_attr_all = self.set_snow_flag(self.sorted_df_attrs_all, snow_file)

        # generate pairings
        with self.timing_block("generate_pairing"):
            self.generate_pairing(df_attr_all, self.dist_spatial, frp)

        logger.info(f"Parameter regionalization for VPU {vpu} completed.")

    @property
    @lru_cache
    def donors_df(self) -> pd.DataFrame:
        """Donors."""
        gage_file = self.donor_gage_file
        donors = self.donor_gages
        if donors.empty:
            raise ValueError(f"No donors found in the donor gage file: {gage_file}")
        if "longitude" not in donors.columns or "latitude" not in donors.columns:
            raise ValueError(
                f"Donor gage file must contain 'longitude' and 'latitude' columns: {gage_file}"
            )
        if "gage_id" not in donors.columns:
            raise ValueError(
                f"Donor gage file must contain 'gage_id' column: {gage_file}"
            )
        return donors

    @property
    @lru_cache
    def donors_gdf(self) -> gpd.GeoDataFrame:
        """Create a GeoDataFrame of donors with geometry as points."""
        return gpd.GeoDataFrame(
            self.donors_df,
            geometry=[
                Point(xy)
                for xy in zip(self.donors_df["longitude"], self.donors_df["latitude"])
            ],
            crs="EPSG:4326",
        )

    @property
    def hydrofabric_gdf(self) -> gpd.GeoDataFrame:
        """Hydrofabric geodataframe with only valid geometries."""
        gdf = gpd.read_file(
            self.config.general.ngen_hydrofabric_file[self.vpu], layer="divides"
        )
        gdf["geometry"] = gdf.geometry.make_valid()
        return gdf

    @property
    @lru_cache
    def donor_gdf_3857(self):
        """Create a GeoDataFrame of donors with geometry as points projected to 3857."""
        return self.donors_gdf.to_crs(3857)

    @property
    def hydrofabric_gdf_3857(self):
        """Hydrofabric geodataframe with only valid geometries projected to 3857."""
        gdf = self.hydrofabric_gdf.to_crs(3857)

        # Fix invalid geometries using buffer(0)
        if not gdf.is_valid.all():
            n_invalid = (~gdf.is_valid).sum()
            logger.debug(
                f"Fixing {n_invalid} invalid geometries in hydrofabric_gdf_3857."
            )
            gdf["geometry"] = gdf.buffer(0)

        # Drop any remaining invalid geometries just in case
        gdf = gdf[gdf.is_valid].copy()
        # gdf["geometry"] = gdf.geometry.make_valid()

        return gdf

    @property
    def combined_geom(self):
        """Dissolve all polygons into one before buffering."""
        try:
            geom = self.hydrofabric_gdf_3857.union_all()
        except AttributeError as e:
            geom = self.hydrofabric_gdf_3857.unary_union
        polygons = []
        if isinstance(geom, MultiPolygon):
            for polygon in geom.geoms:
                polygons.append(Polygon(polygon.exterior))
            return MultiPolygon(polygons)
        elif isinstance(geom, Polygon):
            return geom
        else:
            raise TypeError(f"Expected Polygon or MultiPolygon, got {type(geom)}")

    @property
    def hydrofabric_buffered_polygon(self):
        """Buffered hydrofabric Polygon."""
        return self.combined_geom.buffer(self.config.donor.buffer_km * 1000)

    @property
    def donor_basins_all(self) -> list:
        """All donor basins from the calibration parameter file."""
        return (
            read_table(
                self.config.general.calib_param_file, dtype={self.gage_id_name: str}
            )[self.gage_id_name]
            .unique()
            .tolist()
        )

    @property
    def donor_basins(self) -> list:
        """Get the donor basins for a given VPU from the config.

        Returns:
            donor_basins: list of donor basins (gage_ids) within the buffered VPU polygon

        """
        # Find donors in the buffered VPU
        donor_basins = self.donor_gdf_3857[
            self.donor_gdf_3857.geometry.within(self.hydrofabric_buffered_polygon)
        ]["gage_id"].tolist()

        if not donor_basins:
            logger.warning(
                "No donor basins found. Please check the donor gage file and hydrofabric file."
            )

        return donor_basins

    def update_spatial_distance_donors(
        self,
        id_name: str,
        donors_gdf: gpd.GeoDataFrame,
        receivers_gdf: gpd.GeoDataFrame,
        dist_df: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, bool]:
        """Update existing dataframe for pairwise spatial distance to include new donors (if any).

        Args:
            id_name: the name of the identifier column in the GeoDataFrames
            donors_gdf: GeoDataFrame of new donors
            receivers_gdf: GeoDataFrame of receivers
            dist_df: existing pairwise spatial distance dataframe between donors and receivers

        Returns:
            df_spatial_dist: new dataframe of pairwise spatial distances with new donors (if any) included
            file_changed: boolean indicating whether the file has been changed

        """
        # get new donor list
        new_donor_ids = set(donors_gdf[id_name].values)

        # filter existing distance dataframe columns to keep only new donors
        filtered_df = dist_df.loc[:, dist_df.columns.intersection(new_donor_ids)]

        # find donor IDs missing in the existing dataframe
        missing_donors = new_donor_ids - set(filtered_df.columns)

        if missing_donors:
            # Subset new donors GeoDataFrame to only missing donors
            missing_donors_gdf = donors_gdf[
                donors_gdf["divide_id"].isin(missing_donors)
            ]

            # Compute distances for missing donors
            missing_distances_df = utils_algo.compute_pairwise_centroid_distances(
                missing_donors_gdf, receivers_gdf, id_name, id_name
            )

            # Horizontally concatenate missing donor columns to filtered dataframe
            updated_df = pd.concat([filtered_df, missing_distances_df], axis=1)
        else:
            updated_df = filtered_df

        # Check if the updated dataframe has changed
        file_changed = not updated_df.equals(dist_df)

        return updated_df, file_changed

    def update_spatial_distance_receivers(
        self,
        id_name: str,
        donors_gdf: gpd.GeoDataFrame,
        receivers_gdf: gpd.GeoDataFrame,
        dist_df: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, bool]:
        """Update existing dataframe for pairwise spatial distance to include new receivers (if any).

        Args:
            id_name: the name of the identifier column in the GeoDataFrames
            donors_gdf: GeoDataFrame of donors
            receivers_gdf: GeoDataFrame of receivers
            dist_df: existing pairwise spatial distance dataframe between donors and receivers

        Returns:
            df_spatial_dist: new dataframe of pairwise spatial distances with new donors (if any) included
            file_changed: boolean indicating whether the file has been changed.

        """
        # get new receiver list
        new_receiver_ids = set(receivers_gdf[id_name].values)

        # filter existing distance dataframe columns to keep only new receivers
        filtered_df = dist_df.loc[dist_df.index.intersection(new_receiver_ids), :]

        # find receiver IDs missing in the existing dataframe
        missing_receivers = new_receiver_ids - set(filtered_df.index)

        if missing_receivers:
            # Subset new receivers GeoDataFrame to only missing receivers
            missing_receivers_gdf = receivers_gdf[
                receivers_gdf["divide_id"].isin(missing_receivers)
            ]

            # Compute distances for missing receivers
            missing_distances_df = utils_algo.compute_pairwise_centroid_distances(
                donors_gdf, missing_receivers_gdf, id_name, id_name
            )

            # Vertically concatenate missing receiver rows to filtered dataframe
            updated_df = pd.concat([filtered_df, missing_distances_df], axis=0)
        else:
            updated_df = filtered_df

        # Check if the updated dataframe has changed
        file_changed = not updated_df.equals(dist_df)

        return updated_df, file_changed

    @property
    @lru_cache
    def donor_vpus(self):
        """Determine the VPUs of the donor basins."""
        df_cwt = self.gage_crosswalk
        return (
            df_cwt[df_cwt["gage_id"].isin(self.donor_basins)]["vpuid"].unique().tolist()
        )

    def build_hydrofabric_path(self, vpu1):
        """Build hydrofabric path."""
        file1 = self.config.general.ngen_hydrofabric_file[self.vpu]
        if vpu1 != self.vpu:
            # rename the hydrofabric file to match the current VPU
            file1 = self.config.general.ngen_hydrofabric_file[self.vpu].replace(
                "vpu_" + self.vpu, "vpu_" + vpu1
            )
            # make sure the file exists
            if not Path(file1).is_file():
                raise FileNotFoundError(
                    f"Hydrofabric file for VPU {vpu1} not found: {file1}"
                )
        return file1

    def get_initial_donor_df(self, vpu: str) -> pd.DataFrame:
        """Get initial donor gage/catchment df (before screening with stats) for a specific VPU."""
        # determine initial donor gages
        df_cwt = self.gage_crosswalk
        if self.donor_gage_file:
            logger.info(f"Initial donors based on all gages in {self.donor_gage_file}")
            donors = self.donor_gages[self.gage_id_name].unique().tolist()
        else:
            logger.info(
                f"Initial donors based on all gages in {self.gage_crosswalk_file}"
            )
            donors = df_cwt[self.gage_id_name].unique().tolist()

        # initial donor catchments
        donor_cats = (
            df_cwt[df_cwt[self.divide_id_name].isin(donors)][self.divide_id_name]
            .unique()
            .tolist()
        )

        # filter by vpu
        if "vpuid" in df_cwt.columns:
            df_cwt = df_cwt[df_cwt["vpuid"] == vpu]
            donors = df_cwt[self.gage_id_name].unique().tolist()

            # further filter donors to those that are in the donor_basins_all list
            donors = list(set(donors) & set(self.donor_basins_all))

            # get corresponding donor catchments
            donor_cats = (
                df_cwt.loc[
                    df_cwt[self.gage_id_name].isin(set(donors)), self.divide_id_name
                ]
                .unique()
                .tolist()
            )

            logger.info(
                f"Number of initial donors for VPU {vpu}: {len(donors)} gages, {len(donor_cats)} catchments"
            )
        else:
            raise ValueError(
                f"Column 'vpuid' not found in {self.config.general.gage_divide_cwt_file}. Cannot filter by VPU."
            )

        if not donors:
            logger.warning(
                f"No initial donors found for VPU {vpu}. Please check gage_divide_cwt_file and donor_gage_file."
            )

        donor_df = df_cwt.loc[
            df_cwt[self.divide_id_name].isin(donor_cats),
            [self.divide_id_name, self.gage_id_name],
        ]

        return donor_df.drop_duplicates().reset_index(drop=True)

    @lru_cache
    def donor_receiver_gdfs(self):
        """Get valid donor and receiver geodataframes."""
        # loop through the VPUs of the donor basins to get donor & receiver catchments
        # note that the donor basins may be from multiple VPUs, but receivers are only from the current VPU
        gdf_donors = gpd.GeoDataFrame()
        gdf_receivers = gpd.GeoDataFrame()
        donor_basin_all = []
        for vpu1 in self.donor_vpus:
            # get the initial donors for the current VPU
            init_donor_df = self.get_initial_donor_df(vpu1)

            # get the qualified donors
            donor_dict = self.config.donor.get_qualified_donors(
                self.config, self.donor_basins, init_donor_df
            )
            donors0 = donor_dict[self.divide_id_name]
            donor_basin_all.extend(donor_dict[self.gage_id_name])

            file1 = self.build_hydrofabric_path(vpu1)
            gdf = gpd.read_file(
                file1, layer=getattr(self.config.general.layer_name, "ngen", "divides")
            )
            gdf1 = gdf[gdf[self.divide_id_name].isin(donors0)]
            donors = gdf1[self.divide_id_name].tolist()

            # check if all donors are in the hydrofabric
            donors_missing = set(donors0) - set(donors)
            if len(donors_missing) > 0:
                logger.warning(f"Missing donors in hydrofabric: {donors_missing}")

            # gather donors and receivers in GeoDataFrame
            gdf_donors = pd.concat([gdf_donors, gdf1])
            if vpu1 == self.vpu:
                gdf_receivers = gdf[~gdf[self.divide_id_name].isin(donors)]
                if self.config.general.approach_calib_basins == "summary_score":
                    # if using summary score (rather than regionalization) to assign formulations for calibrated basins,
                    # exclude these calibrated catchments from receivers
                    init_donor_cats = (
                        init_donor_df[self.divide_id_name].unique().tolist()
                    )
                    gdf_receivers = gdf_receivers[
                        ~gdf_receivers[self.divide_id_name].isin(init_donor_cats)
                    ]
            else:
                continue
            if gdf_receivers.empty:
                raise ValueError(
                    f"No receivers found in VPU {self.vpu}. Please check the hydrofabric file and donor gage file."
                )

        logger.info(
            f"Total number of donor basins in VPU {self.vpu}: {len(donor_basin_all)}"
        )

        return gdf_receivers, gdf_donors, donor_basin_all

    @property
    def gdf_receivers(self) -> gpd.GeoDataFrame:
        """Geodataframe of receivers."""
        gdf_receivers, _, _ = self.donor_receiver_gdfs()
        if self.sample_size is not None:
            gdf_receivers = gdf_receivers.sample(
                n=self.sample_size, replace=False, random_state=50
            )  # randomly sample a small number of receivers for testing
        return gdf_receivers

    @property
    def gdf_donors(self) -> gpd.GeoDataFrame:
        """Geodataframe of donors."""
        _, gdf_donors, _ = self.donor_receiver_gdfs()
        # if self.sample_size is not None:  #sample_size should not be applied to donors
        #     gdf_donors = gdf_donors.sample(
        #         n=self.sample_size, replace=False, random_state=50
        #     )  # randomly sample a small number of receivers for testing
        return gdf_donors

    @property
    def final_donor_basins(self) -> list:
        """Final donor basins."""
        _, _, donor_basin_all = self.donor_receiver_gdfs()
        return donor_basin_all

    @property
    def receivers(self) -> list:
        """Receivers."""
        return self.gdf_receivers[self.divide_id_name].tolist()

    @property
    def donors(self) -> list:
        """Donors."""
        return self.gdf_donors[self.divide_id_name].tolist()

    @property
    def number_of_donors(self):
        """Number of donors."""
        return len(self.donors)

    @property
    def number_of_receiver(self):
        """Number of receivers."""
        return len(self.receivers)

    @property
    def dist_file(self) -> Path:
        """Build dist file path."""
        out = getattr(self.config.output, "spatial_distance", None)
        return Path(
            out.path,
            f"donor_receiver_dist_{self.config.general.domain}_vpu{self.vpu}.{out.format}",
        )

    def set_formulation_dict(self, frp: FRP):
        """Get the formulation lookup table."""
        df_form_all = pd.DataFrame()
        for vpu in self.donor_vpus:
            formulation_file = frp.get_output_file_path(
                "formulation",
                vpu,
                use_stem_suffix=False,
            )

            if not formulation_file:
                msg = f"No formulation file found for VPU {vpu}. Exiting ..."
                logger.error(msg)
                raise FileNotFoundError(msg)

            if not Path(formulation_file).is_file():
                msg = f"Formulation file not found: {formulation_file}. Exiting ..."
                logger.error(msg)
                raise FileNotFoundError(msg)

            df_form = read_table(formulation_file, dtype={self.divide_id_name: str})
            df_form_all = pd.concat([df_form_all, df_form])

        # filter df_form_all to only include donors and receivers
        df_form_all = df_form_all[
            df_form_all[self.divide_id_name].isin(self.donors + self.receivers)
        ]

        # formulation dictionary
        form_dict = (
            df_form_all.groupby("formulation")["divide_id"].apply(list).to_dict()
        )

        # check if all donors and receivers have a formulation
        donors_missing = set(self.donors) - set(df_form_all[self.divide_id_name].values)
        if donors_missing:
            logger.warning(
                f"{len(donors_missing)} donors are missing formulations: "
                f"{sorted(donors_missing)[:3]}... "
                f"These donors will not be used in the pairing"
            )

        # check if all receivers have a formulation
        receivers_missing = set(self.receivers) - set(
            df_form_all[self.divide_id_name].values
        )
        if receivers_missing:
            logger.warning(
                f"{len(receivers_missing)} receivers are missing formulations: "
                f"{sorted(receivers_missing)[:3]}... "
                f"These receivers will be paired with donors without considering formulations."
            )

        # add donors and receivers with missing formulation to form_dict, assigning formulation as 'unknown'
        if donors_missing or receivers_missing:
            form_dict["unknown"] = list(donors_missing) + list(receivers_missing)
            logger.info(
                "Assigning 'unknown' formulation to donors and receivers with missing formulations"
            )

        self.formulation_dict = form_dict

    def compute_donor_receiver_spatial_distance(self):
        """Compute spatial distance."""
        if self.dist_file.exists():
            logger.info(f"Spatial distance file already exists: {self.dist_file}")
            df_spatial_dist = read_table(self.dist_file)

            # check if the spatial distance data includes all donors and receivers
            # if not, identify the missing donors and receivers, compute the distance for them and add to the existing dataframe
            logger.info(
                "Updating existing spatial distance file (if needed) to include all donors and receivers ..."
            )
            df_spatial_dist, file_changed1 = self.update_spatial_distance_donors(
                self.divide_id_name,
                self.gdf_donors,
                self.gdf_receivers,
                df_spatial_dist,
            )
            df_spatial_dist, file_changed2 = self.update_spatial_distance_receivers(
                self.divide_id_name,
                self.gdf_donors,
                self.gdf_receivers,
                df_spatial_dist,
            )
            file_changed = file_changed1 or file_changed2

        else:
            logger.info("Compute donor-receiver spatial distance...")
            start_time = time.time()
            df_spatial_dist = utils_algo.compute_pairwise_centroid_distances(
                self.gdf_donors,
                self.gdf_receivers,
                self.divide_id_name,
                self.divide_id_name,
            )
            end_time = time.time()
            logger.info(
                f"Spatial distance computed in {end_time - start_time:.4f} seconds"
            )
            file_changed = True
        return df_spatial_dist, file_changed

    def write_spatial_file(self, df_spatial_dist: pd.DataFrame, file_changed: bool):
        """Save the spatial distance data."""
        sd = getattr(self.config.output, "spatial_distance", None)
        if sd and sd.save and file_changed:
            if not self.dist_file.parent.is_dir():
                self.dist_file.parent.mkdir(parents=True, exist_ok=True)

            # if the file already exists, make a backup
            if self.dist_file.is_file():
                backup_file = self.dist_file.with_suffix(".bak")
                self.dist_file.rename(backup_file)
                logger.info(
                    f"Backup of existing spatial distance file created: {backup_file}"
                )

            # save the spatial distance data
            save_data(df_spatial_dist, self.dist_file, index=True)
            logger.info(f"Spatial distance data saved to {self.dist_file}")

    def get_donors_receivers(self):
        """Get the donors and receivers for a given VPU from the config."""
        logger.info(
            f"Total number of donor catchments in VPU {self.vpu}: {len(self.donors)}"
        )
        logger.info(
            f"Total number of receiver catchments in VPU {self.vpu}: {len(self.receivers)}"
        )

        # compute spatial distance file
        df_spatial_dist, file_changed = self.compute_donor_receiver_spatial_distance()

        # save spatial distance file
        self.write_spatial_file(df_spatial_dist, file_changed)

        # plot donor basin spatial map
        po.plot_donor_spatial_map(
            self.config,
            self.vpu,
            self.donor_basins,
            self.final_donor_basins,
            self.hydrofabric_buffered_polygon,
            self.combined_geom,
        )

        self.dist_spatial = df_spatial_dist

    @property
    def datasets(self) -> list:
        """List of datasets."""
        return self.config.general.attr_dataset_list

    @property
    @lru_cache
    def df_attrs_all(self) -> pd.DataFrame:
        """Dataframe containing all attributes."""
        df_attrs_all = []
        for dataset_name in self.datasets:
            dataset = getattr(self.config.attr_datasets, dataset_name)
            df_attrs = dataset.get_attr_data()

            df_attrs = df_attrs.rename(
                columns=lambda x: x
                if x == self.divide_id_name
                else f"{dataset_name}_{x}"
            )

            # subset the attribute data to only include donors and receivers for the current VPU
            df_attrs = df_attrs[
                df_attrs[self.divide_id_name].isin(self.donors + self.receivers)
            ]
            df_attrs_all.append(df_attrs)

        # Merge all attribute data frames column-wise, based on divide_id
        df_attrs_all = reduce(
            lambda left, right: pd.merge(
                left, right, on=self.divide_id_name, how="outer"
            ),
            df_attrs_all,
        )

        # add a column to indicate whether the divide_id is a donor or receiver
        df_attrs_all["is_donor"] = df_attrs_all[self.divide_id_name].isin(self.donors)
        # move the is_donor column to be the second column
        return df_attrs_all[
            [self.divide_id_name, "is_donor"]
            + [
                col
                for col in df_attrs_all.columns
                if col not in [self.divide_id_name, "is_donor"]
            ]
        ]

    @cached_property
    def get_base_attr_list_all(self) -> list:
        """Get the base attribute list from all datasets."""
        base_attr_list = []
        for dataset_name in self.datasets:
            attrs = getattr(self.config.attr_datasets, dataset_name).base_attr_list
            if attrs is not None:
                base_attr_list.extend([dataset_name + "_" + x for x in attrs])

        return list(set(base_attr_list))

    def check_missing_attrs(self, ids: list, list_type: str):
        """Check for missing attributes."""
        if list_type not in ["donors", "receivers"]:
            raise TypeError(
                f"Expected either 'donors' or 'receivers'; received '{list_type}'"
            )

        if not set(ids).issubset(self.df_attrs_all[self.divide_id_name]):
            logger.warning(
                f"Not all {list_type} are included in the attribute data for VPU {self.vpu}."
            )
            missing_ids = [
                x for x in ids if x not in self.df_attrs_all[self.divide_id_name].values
            ]
            logger.debug(f"Missing {list_type}: {missing_ids}")

    @property
    def donors_w_attrs(self):
        """Donors with attributes."""
        return self.df_attrs_all[self.df_attrs_all["is_donor"]][
            self.divide_id_name
        ].tolist()

    @property
    def receivers_w_attrs(self):
        """Receivers with attributes."""
        return self.df_attrs_all[~self.df_attrs_all["is_donor"]][
            self.divide_id_name
        ].tolist()

    @property
    def number_of_receivers_w_attrs(self):
        """Number of receivers with attributes."""
        return len(self.receivers_w_attrs)

    @property
    def number_of_donors_w_attrs(self):
        """Number of donors with attributes."""
        return len(self.donors_w_attrs)

    def check_attrs_in_spatial_distance_data(
        self, ids: list, list_type: str, df_spatial_dist: pd.DataFrame
    ):
        """Check if all donors in attribute data are included in the columns of the spatial distance data."""
        if list_type not in ["donors", "receivers"]:
            raise TypeError(
                f"Expected either 'donors' or 'receivers'; received '{list_type}'"
            )

        if not set(ids).issubset(df_spatial_dist.columns):
            logger.warning(
                f"Not all {list_type} in the attribute data are present in the spatial distance data for VPU {self.vpu}."
            )
            missing_donor_ids = [x for x in ids if x not in df_spatial_dist.columns]
            logger.debug(f"Missing {list_type}: {missing_donor_ids}")

    @property
    def sorted_df_attrs_all(self):
        """Df_attrs_all sorted by is_donor, _missing_count, and divide_id."""
        # add column to count missing values per row
        df_sorted = self.df_attrs_all.copy()
        df_sorted["_missing_count"] = df_sorted.isnull().sum(axis=1)

        # sort the DataFrame by is_donor, _missing_count, and divide_id
        df_sorted = df_sorted.sort_values(
            by=["is_donor", "_missing_count", self.divide_id_name],
            ascending=[False, True, True],
        )

        # drop '_missing_count' column
        df_sorted = df_sorted.drop(columns=["_missing_count"])

        return df_sorted

    def check_percent_missing(self):
        """Check percentage of missing data."""
        df_missing = self.sorted_df_attrs_all.isna().mean() * 100
        if df_missing.sum() > 0:
            logger.warning(
                f"There are missing data for attributes in vpu {self.vpu}. "
                f"Check the missing attribute counts plot given below."
            )
            logger.debug(
                f"Missing data percentage for each attribute:\n{df_missing.loc[df_missing > 0]}"
            )
            # plot the missing attribute counts
            po.plot_missing_attr_counts(self.config, self.vpu, self.df_attrs_all)

    def save_attribute_data(self):
        """Save the attribute data."""
        out = getattr(self.config.output, "attr_data_final", None)
        if out is not None:
            out.save_to_file(
                self.sorted_df_attrs_all,
                vpu=self.vpu,
                data_str=f"Final Attribute Data (VPU {self.vpu})",
                use_stem_suffix=False,
            )

    def plot_attribute_data(self):
        """Plot attribute data."""
        out = getattr(self.config.output, "attr_data_final", None)
        if out is None:
            logger.info(
                "No output configuration found for attr_data_final. Skipping plot."
            )
            return

        columns_to_plot = out.plots.get("columns_to_plot", None)
        if out.plots.get("spatial_map", False) or out.plots.get("histogram", False):
            if columns_to_plot is None:
                msg = "No columns to plot specified in the config for attr_data_final. Skipping plot."
                logger.warning(msg)
            else:
                df_attr = self.sorted_df_attrs_all.copy()
                if out.plots.get("spatial_map", False):
                    # merge geometry with attribute DataFrame
                    divide_id_col = self.divide_id_name
                    df_attr = df_attr.merge(
                        self.get_vpu_gdf()[[divide_id_col, "geometry"]],
                        on=divide_id_col,
                        how="right",
                    )
                    df_attr = gpd.GeoDataFrame(
                        df_attr, geometry="geometry", crs=self.get_vpu_gdf().crs
                    )

                plot_dict = {
                    "vpu": self.vpu,
                    "var_str": "Attribute Data",
                    "columns": columns_to_plot,
                    "ncols": 3,
                }
                out.plot_data(df_attr, plot_dict)

    def process_attr_data(self):
        """Process the attribute data for a given VPU from the config."""
        logger.info(
            f"Processing attribute data for VPU {self.vpu} ... datasets: {self.datasets}"
        )

        # check if all donors/receivers have attributes
        self.check_missing_attrs(self.donors, "donors")
        self.check_missing_attrs(self.receivers, "receivers")

        # plot spatial map of attribute data
        self.plot_attribute_data()

        logger.info(
            f"Number of donors with attribute data: {self.number_of_donors_w_attrs}"
        )
        logger.info(
            f"Number of receivers with attribute data: {self.number_of_receivers_w_attrs}"
        )

        self.check_attrs_in_spatial_distance_data(
            self.donors_w_attrs, "donors", self.dist_spatial
        )
        self.check_attrs_in_spatial_distance_data(
            self.receivers_w_attrs, "receivers", self.dist_spatial
        )

        # check percent missing
        self.check_percent_missing()

        # save attribute data
        self.save_attribute_data()

    def set_snow_flag(
        self, df_attrs: pd.DataFrame, snow_file: str | Path
    ) -> pd.DataFrame:
        """Set a boolean flag to indicate whether a catchment is snow-driven.

        Add a boolean 'snowy' column to existing attributes dataframe to indicate whether
        a catchment is snow-driven or not.

        Args:
            df_attrs: DataFrame of attributes for donors and receivers
            snow_file: Path to the snow fraction file for the VPU

        Returns:
            New DataFrame of attributes with a new boolean column added to indicate whether the catchment is snow-driven

        """
        if self.config.snow_cover.consider_snowness is False:
            # if snow_cover is not considered, set all catchments to non-snowy
            df_attrs["snowy"] = False
            logger.info(
                "Snowness is not considered in the pairing. All catchments are set to non-snowy."
            )

        else:
            logger.info(
                "Setting snowy flag for catchments based on snow_cover configuration."
            )
            df_snow = read_table(Path(snow_file), dtype={self.divide_id_name: str})
            snow_col = self.config.snow_cover.column
            df_snow["snowy"] = df_snow[snow_col].apply(
                lambda x: True if x >= self.config.snow_cover.threshold else False
            )

            # merge the snow data with the attribute data
            df_attrs = df_attrs.merge(
                df_snow[[self.divide_id_name, "snowy"]],
                on=self.divide_id_name,
                how="left",
            )

        return df_attrs

    @property
    def pairers(self) -> dict:
        """Pairing/regionalization algorithms."""
        return {
            "proximity": ProximityPairer,
            "gower": GowerPairer,
            "urf": URFPairer,
            "kmeans": KmeansPairer,
            "kmedoids": KmedoidsPairer,
            "hdbscan": HDBSCANPairer,
            "birch": BIRCHPairer,
        }

    @property
    def pairer_names(self) -> list:
        """Run only those algorithms specified to run in the config file."""
        return [
            x for x in self.pairers.keys() if x in self.config.general.algorithm_list
        ]

    # def construct_output_filepath(self, pairer_name: str) -> Path:
    #     """Construct output filepath."""
    #     return getattr(self.config.output, "pairs", None).get_file_path(
    #         vpu=self.vpu, algorithm=pairer_name
    #     )
    # return self.config.output.pairs._get_file_path(self.vpu)

    def update_algorithm_config(
        self, pairer_name: str, df_attrs_all: pd.DataFrame
    ) -> dict:
        """Update the algorithm config."""
        id_name = self.divide_id_name
        config = self.config.model_dump()

        if pairer_name in config["algorithms"]:
            algorithm_config = config["algorithms"][pairer_name]
        else:  # if the pairer is not in the config (e.g., proximity), use the general algorithm config
            algorithm_config = config["algorithms"]["algo_general"].copy()

        algorithm_config["max_spa_dist"] = config["algorithms"]["algo_general"][
            "max_spa_dist"
        ]
        algorithm_config["njobs"] = config["general"]["n_procs"]
        algorithm_config["non_attr_cols"] = [id_name, "is_donor", "snowy"]

        # add attributes to algorithm_config
        main_attrs = [
            x
            for x in df_attrs_all.columns
            if x not in algorithm_config["non_attr_cols"]
        ]
        base_attrs = self.get_base_attr_list_all
        # make sure base_attrs are in main_attrs
        missed_base_attrs = set(base_attrs) - set(main_attrs)
        if missed_base_attrs:
            logger.warning(
                f"Base attributes {missed_base_attrs} are not present in the main attributes. "
                "They will not be used in the pairing."
            )
        # filter base_attrs to only include those that are in main_attrs
        base_attrs = [x for x in base_attrs if x in main_attrs]

        algorithm_config["attrs"] = {
            "main": main_attrs,
            "base": base_attrs,
        }

        return algorithm_config

    def plot_pairing_outputs(
        self, algorithm: str, df_pairs: pd.DataFrame = None, d1: dict = None
    ) -> None:
        """Plot the donor-receiver distances for the given algorithm.

        Args:
            algorithm: algorithm name
            df_pairs: DataFrame containing the donor-receiver pairs
            d1: dictionary containing additional parameters for plotting

        """
        # output config for pairs
        co = getattr(self.config.output, "pairs", None)

        # read the pairing results from file if df_pairs is not provided
        if df_pairs is None or df_pairs.empty:
            outfile = co.get_file_path(vpu=self.vpu, algorithm=algorithm)
            if not outfile.exists():
                msg = f"Pairing results file does not exist: {outfile}. Please run the pairing first."
                logger.error(msg)
                raise FileNotFoundError(msg)
            else:
                logger.info(f"Loading processed pairing data from file: {outfile}")
                df_pairs = read_table(outfile)

        columns_to_plot = co.plots.get("columns_to_plot", ["distSpatial", "distAttr"])
        plot_dict = {
            "vpu": self.vpu,
            "algorithm": algorithm,
            "var_str": "Donor-Receiver Distances",
            "columns": columns_to_plot,
            "ncols": min(3, len(columns_to_plot)),
        }

        # convert df_pairs to GeoDataFrame to plot spatial map
        if co.plots and co.plots.get("spatial_map", False):
            # if "geometry" not in df_pairs.columns:
            id_col = self.divide_id_name

            # merge df_pairs with the VPU geodataframe to get the geometry
            gdf = self.get_vpu_gdf()

            df_pairs = df_pairs.merge(gdf, on=id_col, how="right")
            df_pairs = gpd.GeoDataFrame(df_pairs, geometry="geometry", crs=gdf.crs)

        co.plot_data(df_pairs, plot_dict)

    def supplementary_pairing(
        self,
        pairer_name: str,
        df_attr_all: pd.DataFrame,
        dist_spatial: pd.DataFrame,
        processed_receivers_df: pd.DataFrame = None,
        receivers_tobe_processed: list = None,
    ) -> pd.DataFrame:
        """Conduct supplementary donor-receiver pairing.

        Currently only pairing via spatial proximity is supported.

        Args:
            pairer_name: name of the pairing algorithm to use (e.g., "proximity")
            df_attr_all: dataframe containing the full attribute data for all receivers and donors
            dist_spatial: dataframe containing the pair-wise spatial distance between donors and receivers
            processed_receivers_df: dataframe containing the already processed receivers
            receivers_tobe_processed: list of receivers to be processed

        Returns:
            processed_receivers_df: dataframe containing the updated receiver-donor pairs.

        """
        if receivers_tobe_processed is None:
            return processed_receivers_df

        # determine the receivers to be processed
        if processed_receivers_df is not None:
            receivers_processed = processed_receivers_df[self.divide_id_name].tolist()
            receivers_tobe_processed = list(
                set(receivers_tobe_processed) - set(receivers_processed)
            )

        new_receivers_df = processed_receivers_df.copy()
        if receivers_tobe_processed:
            logger.info(
                f"Processing {len(receivers_tobe_processed)} receivers using {pairer_name} algorithm."
            )

            # initialize the pairer
            if pairer_name not in self.pairers or pairer_name != "proximity":
                raise ValueError(
                    f"Pairer {pairer_name} is not supported or not selected in the configuration."
                )

            algorithm_config = self.update_algorithm_config(pairer_name, df_attr_all)
            pairer = self.pairers[pairer_name](
                config=algorithm_config,
                df_attr_all=df_attr_all,
                dist_spatial=dist_spatial,
            )

            # conduct pairing for the remaining receivers
            df_new = pairer.pair(receivers=receivers_tobe_processed)
            new_receivers_df = pd.concat([new_receivers_df, df_new])

        return new_receivers_df

    def add_donors_to_pair_results(self, df_pairs: pd.DataFrame) -> pd.DataFrame:
        """Add donors without attributes to the pairing results.

        Args:
            df_pairs: DataFrame containing the donor-receiver pairs

        Returns:
            df_pairs: DataFrame containing the updated donor-receiver pairs

        """
        # identify catchments that are missing from the pairing results for the current VPU
        init_donor_df = self.get_initial_donor_df(self.vpu)
        existing_ids = set(df_pairs[self.divide_id_name])
        cats_missing = [
            d for d in init_donor_df[self.divide_id_name] if d not in existing_ids
        ]

        # assuming all missing catchments are calibrated catchments,
        # regardless of whether they are used as donors or not
        if cats_missing:
            logger.info(
                "Add donor catchments to the pairing results with zero distances."
            )
            df_donors = pd.DataFrame(
                {
                    self.divide_id_name: cats_missing,
                    "donor": cats_missing,
                }
            )
            # add donors to the pairing results, and set distances to zero
            if "distSpatial" in df_pairs.columns:
                df_donors["distSpatial"] = 0
            if "distAttr" in df_pairs.columns:
                df_donors["distAttr"] = 0
            if "tag" in df_pairs.columns:
                df_donors["tag"] = "donor"

            df_pairs = pd.concat([df_pairs, df_donors], ignore_index=True)

        # sort the pairing results by divide_id
        df_pairs = df_pairs.sort_values(by=[self.divide_id_name], ascending=True)
        return df_pairs

    def save_pairing_results(
        self, df_pairs: pd.DataFrame, pairer_name: str
    ) -> pd.DataFrame:
        """Save the pairing results to file."""
        # output config for pairs
        co = getattr(self.config.output, "pairs", None)
        if co is None:
            logger.warning("No output configuration found for pairs. Skipping save.")
            return

        # save donor receiver pairing to csv file
        co.save_to_file(
            df_pairs,
            vpu=self.vpu,
            algorithm=pairer_name,
            data_str=f"Pairing results (VPU {self.vpu}, algorithm = {pairer_name})",
            use_stem_suffix=False,
        )

        # get donors by gage for use by MSWM
        df_pairs_gage = df_pairs[[self.divide_id_name, self.donor_id_name]].copy()
        df_pairs_gage = df_pairs_gage.merge(
            self.gage_crosswalk[[self.divide_id_name, self.gage_id_name]],
            left_on=self.donor_id_name,
            right_on=self.divide_id_name,
            how="left",
        )

        # make sure the divide_id_name column is present
        if self.divide_id_name not in df_pairs_gage.columns:
            if self.divide_id_name + "_x" in df_pairs_gage.columns:
                df_pairs_gage = df_pairs_gage.rename(
                    columns={self.divide_id_name + "_x": self.divide_id_name}
                )
            else:
                msg = f"{self.divide_id_name} not found in the gage crosswalk file or the donor-receiver pairing results."
                logger.error(msg)
                raise KeyError(msg)

        df_pairs_gage = (
            df_pairs_gage[[self.gage_id_name, self.divide_id_name]]
            .drop_duplicates()
            .sort_values(by=[self.gage_id_name])
        )

        # save the gage-donor pairs to a separate file (MSWM requires csv format)
        format0 = co.format
        co.format = "csv"
        co.save_to_file(
            df_pairs_gage,
            vpu=self.vpu,
            algorithm=pairer_name,
            data_str=f"Pairing results (VPU {self.vpu}, algorithm = {pairer_name})",
            use_stem_suffix=True,
        )
        co.format = format0

        return df_pairs_gage

    def get_donors_receivers_by_form(self, form_key: str, form_values: list) -> tuple:
        """Get the donors and receivers for a given formulation.

        Args:
            form_key: formulation key
            form_values: list of divide_ids in the formulation

        Returns:
            donors_in_form: list of donors in the formulation
            receivers_in_form: list of receivers in the formulation

        """
        donors_in_form = list(set(self.donors) & set(form_values))
        receivers_in_form = list(set(self.receivers) & set(form_values))

        form_no = list(self.formulation_dict).index(form_key) + 1
        if not receivers_in_form:
            logger.warning(
                f"No receivers found for formulation #{form_no} ['{form_key}'] in VPU {self.vpu}. "
                f"Skipping this formulation."
            )
            return [], []

        # use all donors if no donors in the current formulation
        if receivers_in_form and not donors_in_form:
            msg = f"No donors found for formulation #{form_no} ['{form_key}'] in VPU {self.vpu}. "
            msg += f"Formulation will not be used for pairing for these receivers ({len(receivers_in_form)})."
            logger.warning(msg)
            donors_in_form = self.donors

        logger.info(
            f"Processing formulation #{form_no}: "
            f"[{form_key.upper()}], with {len(donors_in_form)} donors and "
            f"{len(receivers_in_form)} receivers."
        )

        return donors_in_form, receivers_in_form

    def create_formulation_parameter_file(
        self, form_config: Any, pairer: str
    ) -> pd.DataFrame:
        """Create formulation parameter file.

        Create a formulation parameter file that lists the gage_id, formulation, and the calibrated parameters.

        Args:
            form_config: configuration object containing the settings for formulation regionalization output
            pairer: name of the pairing algorithm used

        """
        # read parameter file from formulation regionalization for all donor VPUs
        param_files = [
            form_config.get_file_path(vpu=vpu, use_stem_suffix=True)
            for vpu in self.donor_vpus
        ]
        df_param_all = pd.DataFrame()
        for param_file in param_files:
            if not param_file.exists():
                msg = f"Formulation parameter file does not exist: {param_file}. "
                msg += "Please run the formulation regionalization first."
                logger.error(msg)
                raise FileNotFoundError(msg)
            else:
                logger.info(
                    f"Loading formulation parameter data from file: {param_file}"
                )
                df_param = read_table(param_file, dtype={self.gage_id_name: str})
                df_param_all = pd.concat([df_param_all, df_param], ignore_index=True)

        # read gage-receiver pairing results for the current algorithm and VPU
        co = getattr(self.config.output, "pairs", None)
        if co is None:
            logger.warning(
                "No output configuration found for pairs. Skipping creating formulation parameter file."
            )
            return

        pair_file = co.get_file_path(
            vpu=self.vpu, algorithm=pairer, use_stem_suffix=True
        )

        # replace file suffix with .csv (MSWM requirement)
        if pair_file.suffix != ".csv":
            pair_file = pair_file.with_suffix(".csv")

        # read the pairing results to get the list of donor gages
        if not pair_file.exists():
            msg = f"Pairing results file does not exist: {pair_file}. Please run the pairing first."
            logger.error(msg)
            raise FileNotFoundError(msg)
        else:
            df_pairs = read_table(
                pair_file, dtype={self.gage_id_name: str, self.divide_id_name: str}
            )
            donor_gages = df_pairs[self.gage_id_name].unique().tolist()

        # filter the parameter data to only include donors for the current algorithm and VPU
        df_param_all = df_param_all[df_param_all[self.gage_id_name].isin(donor_gages)]

        if df_param_all.empty:
            msg = "No formulation parameter data found. Please run the formulation regionalization first."
            logger.error(msg)
            raise ValueError(msg)
        else:
            # save the formulation parameter file
            out = getattr(self.config.output, "params", None)
            if out is None:
                logger.warning(
                    "No output configuration found for params. Skipping save."
                )
                return
            out.save_to_file(
                df_param_all,
                vpu=self.vpu,
                algorithm=pairer,
                data_str=f"Formulation Parameter Data (VPU {self.vpu}, algorithm = {pairer})",
                use_stem_suffix=False,
            )

        return df_param_all

    def plot_parameter_outputs(
        self, pairer_name: str, df_pairs_gage: pd.DataFrame, df_param_all: pd.DataFrame
    ) -> None:
        """Plot the formulation parameter outputs.

        Args:
            pairer_name: name of the pairing algorithm used
            df_pairs_gage: DataFrame containing the gage-receiver pairs
            df_param_all: DataFrame containing the formulation parameters

        """
        # output config for params
        co = getattr(self.config.output, "params", None)
        if co is None or not co.plots or co.plots.get("columns_to_plot", None) is None:
            return

        if df_param_all is None or df_param_all.empty:
            msg = "No formulation parameter data found. Skipping params plot"
            logger.error(msg)

        if df_pairs_gage is None or df_pairs_gage.empty:
            msg = "No gage-receiver pairing data found. Skipping params plot"
            logger.error(msg)

        # merge df_param_all with df_pairs_gage to get the formulation parameters for all receivers in the current VPU
        df_params = df_pairs_gage.merge(
            df_param_all,
            on=self.gage_id_name,
            how="left",
        )

        columns_to_plot = co.plots.get("columns_to_plot", [])
        plot_dict = {
            "vpu": self.vpu,
            "var_str": "Regionalized Parameters",
            "columns": columns_to_plot,
            "ncols": min(3, len(columns_to_plot)),
        }

        # convert df_pairs to GeoDataFrame to plot spatial map
        if co.plots and co.plots.get("spatial_map", False):
            # merge df_pairs with the VPU geodataframe to get the geometry
            gdf = self.get_vpu_gdf()
            df_params = df_params.merge(gdf, on=self.divide_id_name, how="right")
            df_params = gpd.GeoDataFrame(df_params, geometry="geometry", crs=gdf.crs)

        co.plot_data(df_params, plot_dict)

    def generate_pairing(
        self, df_attr_all: pd.DataFrame, dist_spatial: pd.DataFrame, frp: FRP
    ):
        """Conduct donor-receiver pairing for a given VPU based on the configuration.

        For a given VPU, generate donor-receiver pairing results for each algorithm selected in the configuration,
        based on the attributes and spatial distance DataFrame.

        Args:
            df_attr_all: dataframe containing the full attribute data for all receivers and donors
            dist_spatial: dataframe containing the pair-wise spatial distance between donors and receivers
            frp: FRP object containing the settings for formulation regionalization

        Returns:
            None, but saves the pairing results to a file.

        """
        logger.info(f"Algorithms to run: {self.pairer_names}")

        # output config for pairs
        co = getattr(self.config.output, "pairs", None)
        if co is None:
            logger.warning(
                "No output configuration found for pairs. Skipping pairing generation."
            )
            return

        # loop through regionalization algorithms to generate donor-receiver pairings for each algorithm/scenario combination
        for pairer_name in self.pairer_names:
            # outfile = self.construct_output_filepath(pairer_name)
            outfile = co.get_file_path(vpu=self.vpu, algorithm=pairer_name)
            processed_receivers_df = pd.DataFrame()
            if outfile.exists():
                logger.info(f"Pair file already exist: {outfile}")
                logger.info(f"Skip the current pairing run: {pairer_name}")
            else:
                logger.info(
                    f"*************** Identify donors for VPU {self.vpu} using: {pairer_name} **************"
                )
                start_time = time.time()

                algorithm_config = self.update_algorithm_config(
                    pairer_name, df_attr_all
                )

                # loop through formulations to conduct pairing separately for each formulation
                df_pairs_all = pd.DataFrame()
                self.set_formulation_dict(frp)
                for form_key, form_values in self.formulation_dict.items():
                    # identify donors and receivers for the current formulation
                    donors_in_form, receivers_in_form = (
                        self.get_donors_receivers_by_form(form_key, form_values)
                    )
                    if not receivers_in_form:
                        continue

                    # filter the attribute data to only include donors and receivers in the current formulation
                    df_attr_form = df_attr_all[
                        df_attr_all[self.divide_id_name].isin(
                            donors_in_form + receivers_in_form
                        )
                    ]
                    # order df_attr_form by is_donor and divide_id
                    df_attr_form = df_attr_form.sort_values(
                        by=["is_donor", self.divide_id_name], ascending=[False, True]
                    )

                    # execute pairing function
                    pairer = self.pairers[pairer_name](
                        config=algorithm_config,
                        df_attr_all=df_attr_form,
                        dist_spatial=dist_spatial.loc[
                            receivers_in_form, donors_in_form
                        ],
                    )
                    processed_receivers_df = pairer.pair()

                    # supplementary pairing if needed
                    processed_receivers_df = self.supplementary_pairing(
                        "proximity",
                        df_attr_all,
                        dist_spatial,
                        processed_receivers_df,
                        receivers_in_form,
                    )

                    # check if all receivers have been processed
                    missed_receivers = set(receivers_in_form) - set(
                        processed_receivers_df[self.divide_id_name].tolist()
                    )
                    if missed_receivers:
                        logger.warning(
                            f"{len(missed_receivers)} receivers were not successfully processed: {missed_receivers} \n"
                        )
                    else:
                        logger.info(
                            f"All {len(receivers_in_form)} receivers were successfully processed for the current "
                            f"formulation.\n"
                        )

                    df_pairs_all = pd.concat([df_pairs_all, processed_receivers_df])

                # add donors to the pairing results
                df_pairs_all = self.add_donors_to_pair_results(df_pairs_all)

                # save the pairing results to file
                df_pairs_gage = self.save_pairing_results(df_pairs_all, pairer_name)

                # plot the pairing results
                self.plot_pairing_outputs(pairer_name, df_pairs_all)

                # create formulation parameter file
                df_param_all = self.create_formulation_parameter_file(
                    getattr(frp.config.output, "formulation", None), pairer_name
                )

                # plot parameter outputs
                self.plot_parameter_outputs(pairer_name, df_pairs_gage, df_param_all)

                end_time = time.time()
                logger.info(f"Execution time: {end_time - start_time:.4f} seconds")

            logger.info(
                f"*************** End of pairing using: {pairer_name} **************\n"
            )
