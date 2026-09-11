"""Create NextGen catchment to attribute dataset subbasin crosswalk table and process attribute data.

Currently supported datasets: NGEN, HLR, HydroATLAS, NHDPlus/StreamCat.

The script creates a crosswalk table between NextGen catchments and the specified attribute dataset sub-basins
based on overlapping area percentage, and then computes area-weighted attributes for NextGen catchments based on
the crosswalk table.

The configuration is specified in a YAML file (attr_config.yaml), which includes paths to input/output files,
attribute dataset information, and processing options.

The script also requires a list of attributes to process for the specified attribute dataset,
which is provided in a separate CSV file via the `attr_list_file` parameter in the configuration.

Example usage:
    python process_cwt_attr.py attr_config.yaml

"""

import argparse
import gc
import os
from pathlib import Path
from typing import List, Optional, Union

import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from pydantic import BaseModel, model_validator
from shapely.geometry import box


class AttrConfig(BaseModel):
    """Attribute dataset configuration class."""

    hf_file: Optional[Union[Path, str]] = None
    layer: Optional[str] = None
    id_col: Optional[str] = None

    attr_list_file: Optional[Union[Path, str]] = None
    attr_data_dir: Optional[Union[Path, str]] = None


class ProcessAttrDataset(BaseModel):
    """Class to process attribute datasets for NextGen catchments."""

    hf_version: Optional[str] = "nhf"
    domain: Optional[str] = "conus"
    attr_dataset: str
    attr_list: Optional[List[str]] = None

    overlap_threshold_max: float = 99.0  # maximum cumulative overlap percentage threshold for including attribute sub-basins in the crosswalk table for each NextGen catchment; default to 99% to include all sub-basins with any overlap
    overlap_threshold_min: float = 20.0  # minimum cumulative overlap percentage threshold for including NextGen catchments in the crosswalk table; default to 20% to exclude catchments with very little overlap with attribute sub-basins

    base_dir: Union[Path, str]
    gpkg_dir: Union[Path, str]
    cwt_file: Union[Path, str]
    attr_file: Union[Path, str]

    process_cwt: bool = True
    process_attr: bool = True
    analyze_cwt: bool = True

    hlr: AttrConfig
    ngen: AttrConfig
    streamcat: AttrConfig
    hydroatlas: AttrConfig

    hf_file: Optional[Union[Path, str]] = None
    layer: Optional[str] = None
    id_col: Optional[str] = None
    attr_list_file: Optional[Union[Path, str]] = None
    attr_data_dir: Optional[Union[Path, str]] = None

    div_col: Optional[str] = None
    area_col: Optional[str] = None
    vpu_col: Optional[str] = None

    @model_validator(mode="after")
    def resolve_paths(self):
        """Resolve paths and placeholders in the configuration."""
        data = self.model_dump()

        def resolve(val):
            if isinstance(val, str):
                val = os.path.expanduser(val)
                try:
                    return val.format(**data)
                except KeyError:
                    return val
            elif isinstance(val, dict):
                return {k: resolve(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [resolve(v) for v in val]
            return val

        # Resolve multiple passes (handles nested dependencies)
        for _ in range(5):
            for field in data:
                data[field] = resolve(data[field])

        # Assign back (and coerce to Path where appropriate)
        for field, value in data.items():
            setattr(self, field, value)

        return self

    @model_validator(mode="after")
    def set_dataset_info(self):
        """Set dataset-specific information based on the specified attribute dataset."""
        dataset_map = {
            "hlr": self.hlr,
            "ngen": self.ngen,
            "streamcat": self.streamcat,
            "hydroatlas": self.hydroatlas,
        }

        cfg = dataset_map.get(self.attr_dataset.lower())
        if cfg is None:
            raise ValueError(f"Unknown dataset: {self.attr_dataset}")

        for field in AttrConfig.model_fields.keys():
            value = (
                cfg.get(field, None)
                if isinstance(cfg, dict)
                else getattr(cfg, field, None)
            )
            setattr(self, field, value)

        if self.hf_file:
            self.hf_file = Path(self.hf_file).expanduser()

        # div_col
        self.div_col = "divide_id" if self.hf_version == "v2.2" else "div_id"

        # area_col
        self.area_col = "areasqkm" if self.hf_version == "v2.2" else "area_sqkm"

        # vpu_col
        self.vpu_col = "vpuid" if self.hf_version == "v2.2" else "vpu_id"

        return self

    def get_nhdplus_shp_file_for_vpu(self, vpu: str) -> Path:
        """Get the NHDPlus shapefile for the specified VPU."""
        nhdplus_vpu = Path(str(self.hf_file).replace("{vpu}", vpu)).expanduser()
        if not nhdplus_vpu.exists():
            raise FileNotFoundError(
                f"NHDPlus shapefile not found for VPU {vpu}: {nhdplus_vpu}"
            )
        return nhdplus_vpu

    def create_cwt(
        self,
        shp1: gpd.GeoDataFrame,
        shp2: gpd.GeoDataFrame,
    ):
        """Create crosswalk table between two sets of polygons based on overlapping area percentage.

        For each polygon in shp2, find polygons in shp1 that overlap more than the specified threshold percentage.
        """
        # Convert to a projected CRS for accurate area calculations
        # projected_crs = "EPSG:3857" # Web Mercator; preserves shapes but distorts area, especially at high latitudes
        projected_crs = "EPSG:6933"  # Equal-area cylindrical projection; preserves area globally; alternative: "EPSG:5070" (Albers Equal Area) for CONUS only
        shp1 = shp1.to_crs(projected_crs)
        shp2 = shp2.to_crs(projected_crs)

        # filter both shapefiles to only include polygons
        shp2 = shp2[shp2.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
        shp1 = shp1[shp1.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]

        # Find overlapping areas with shp1
        overlap = gpd.overlay(shp2, shp1, how="intersection", keep_geom_type=True)
        # print(f"overlap: {overlap}")
        # overlap = overlap[overlap.geometry.geom_type.isin(["Polygon", "MultiPolygon"])] # caution: this filters out some valid overlaps

        # Compute area of each original polygon in shp2 (and convert to km^2)
        shp2["original_area"] = shp2.geometry.area / 1_000_000

        # Compute intersection area (and convert to km^2)
        overlap["overlap_area"] = overlap.geometry.area / 1_000_000
        overlap = overlap.drop(columns=self.area_col)

        # merge overlap with shp2 (to get original_area)
        overlap = overlap.merge(
            shp2.drop(columns="geometry"), on=self.div_col, how="left"
        )

        # Calculate percentage of each shp2 polygon that is covered by intersecting polygons in shp1
        overlap["overlap_percentage"] = (
            overlap["overlap_area"] / overlap["original_area"]
        ) * 100

        # sort by divide_id and descending overlap_percentage
        overlap = overlap.sort_values(
            by=[self.div_col, "overlap_percentage"], ascending=[True, False]
        )

        # compute cumulative overlap_percentage for each divide
        overlap["cum_percentage"] = overlap.groupby(self.div_col)[
            "overlap_percentage"
        ].cumsum()

        # filter out shp1 polygons when cumulative overlap_percentage reaches the max threshold requirement
        # (but always keep the first row)
        overlap["rank"] = overlap.groupby(self.div_col).cumcount()
        overlap = overlap[
            (overlap["rank"] == 0)
            | (overlap["cum_percentage"] <= self.overlap_threshold_max)
        ]

        # make sure (maximum) cumulative overlap percentage is greater than the minimum threshold
        # Find ids where max(cum_area) > threshold
        polys_matched = overlap.groupby(self.div_col)["cum_percentage"].max()
        polys_matched = polys_matched[polys_matched >= self.overlap_threshold_min].index
        overlap = overlap[overlap[self.div_col].isin(polys_matched)]

        # identify shp2 polygons not paired with a shp1 polygon
        polys = shp2[self.div_col].unique()
        polys_unmatched = [x for x in polys if x not in polys_matched]

        # drop columns that are no longer needed
        overlap = overlap.drop(
            columns=["overlap_area", "original_area", "cum_percentage", "rank"]
        )

        # Find the nearest shp1 polygon for each unmatched shp2 polygon
        nearest_matches = pd.DataFrame()
        if polys_unmatched:
            print(
                f"Number of polygons without sufficient overlap match (using nearest neighbor): {len(polys_unmatched)}"
            )
            nearest_matches = gpd.sjoin_nearest(
                shp2[shp2[self.div_col].isin(polys_unmatched)],
                shp1,
                how="left",
                distance_col="nearest_distance",
            )
            nearest_matches.rename(
                columns={"nearest_distance": "nearest_dist_m"}, inplace=True
            )
            nearest_matches = nearest_matches[[self.div_col, "id", "nearest_dist_m"]]

        # create the final shp2/shp1 crosswalk table
        cwt = pd.concat(
            [overlap.drop(columns="geometry"), nearest_matches],
            axis=0,
            ignore_index=True,
        )

        return cwt

    def get_vpu_list(self) -> list:
        """Get list of VPUs for the specified domain."""
        match self.domain.lower():
            case "conus":
                # fmt: off
                vpu_list = [
                    "01", "02", "03N", "03S", "03W", "04", "05", "06", "07", "08",
                    "09", "10L", "10U", "11", "12", "13", "14", "15", "16", "17", "18",
                ]
                # fmt: on
            case "ak":
                vpu_list = ["19"]
            case "hi":
                vpu_list = ["20"]
            case "prvi":
                vpu_list = ["21"]
            case _:
                raise Exception(f"Unsupported domain: {self.domain}")

        return vpu_list

    def get_vpu_gpd(self, vpu: str) -> gpd.GeoDataFrame:
        """Get GeoDataFrame for the specified VPU."""
        vpu_files = list(Path(self.gpkg_dir).expanduser().glob("*.gpkg"))
        vpu_file = [f for f in vpu_files if f"vpu_{vpu}" in f.name]
        if not vpu_file:
            print(f"Warning: vpu file not found for vpu {vpu}. Skipping...")
            return gpd.GeoDataFrame()
        elif len(vpu_file) > 1:
            print(f"Warning: multiple vpu files found for vpu {vpu}. Skipping...")
            return gpd.GeoDataFrame()
        else:
            vpu_file = vpu_file[0]

        print(f"Reading hydrofabric divides for vpu {vpu} from {vpu_file}...")
        shp_vpu = gpd.read_file(vpu_file, layer="divides")
        # shp_vpu = shp_vpu[[self.div_col, self.area_col, "geometry"]]

        return shp_vpu

    def process_cwt_by_vpu(self, vpu: str) -> pd.DataFrame:
        """Process crosswalk table creation for NextGen catchments for the specified VPU."""
        # read NextGen divides for the vpu
        shp_vpu = self.get_vpu_gpd(vpu)

        # read attribute dataset sub-basins given the vpu bounding box
        hf_file = self.get_nhdplus_shp_file_for_vpu(vpu)
        with fiona.open(hf_file) as src:
            crs_attr = src.crs
        bbox = shp_vpu.total_bounds
        bbox_geom = gpd.GeoSeries([box(*bbox)], crs=shp_vpu.crs)
        bbox_reprojected = bbox_geom.to_crs(crs_attr)
        bbox_bounds = bbox_reprojected.total_bounds
        bbox_geom1 = box(*bbox_bounds)
        shp_attr = gpd.read_file(hf_file, layer=self.layer, bbox=bbox_geom1)

        # rename id column for processing in create_cwt
        shp_attr.rename(columns={self.id_col: "id"}, inplace=True)
        shp_attr = shp_attr[["id", "geometry"]]

        if shp_attr.empty:
            print(f"Warning: no overlapping {self.layer} subbasins found for vpu {vpu}")
            return pd.DataFrame()

        # create crosswalk
        cwt1 = self.create_cwt(
            shp_attr, shp_vpu[[self.div_col, self.area_col, "geometry"]]
        )
        if cwt1.empty:
            print(f"Warning: no crosswalk created for vpu {vpu}")
            return pd.DataFrame()

        # reset id column back
        cwt1.rename(columns={"id": self.id_col}, inplace=True)

        # save cwt for the current vpu
        # Path(self.cwt_file).parent.mkdir(parents=True, exist_ok=True)
        # cwt1.to_parquet(self.cwt_file, engine="pyarrow")

        del shp_attr, shp_vpu
        gc.collect()

        return cwt1

    def process_crosswalk(self):
        """Process crosswalk table creation for NextGen catchments for the specified domain."""
        if Path(self.cwt_file).exists():
            print(
                f"CWT file for {self.domain} for {self.attr_dataset} already exists. Reading from {self.cwt_file}"
            )
            return

        # get the list of vpus for the domain
        vpu_list = self.get_vpu_list()

        # process cwt by vpu to reduce memory usage
        df_cwt = pd.DataFrame()
        for vpu in vpu_list:
            cwt = self.process_cwt_by_vpu(vpu)
            cwt[self.vpu_col] = vpu
            df_cwt = pd.concat([df_cwt, cwt])

            # free up memory
            del cwt
            gc.collect()

        # save the combined cwt
        if df_cwt.empty:
            print(
                f"WARNING: No crosswalk table created for {self.attr_dataset} for the {self.domain} domain."
            )
        else:
            print(
                f"Saving crosswalk table for {self.attr_dataset} to {self.cwt_file} ..."
            )
            Path(self.cwt_file).parent.mkdir(parents=True, exist_ok=True)
            df_cwt.to_parquet(
                self.cwt_file,
                engine="pyarrow",
                index=False,
            )

        return

    def analyze_cwt_results(self):
        """Analyze crosswalk table results and print summary statistics."""
        if not Path(self.cwt_file).exists():
            raise FileNotFoundError(f"CWT file not found at {self.cwt_file}")

        df_cwt = pd.read_parquet(self.cwt_file)

        cats_total = df_cwt[self.div_col].unique()
        print(
            f"\nAnalysis of CWT results for {self.attr_dataset.upper()} attributes for {self.domain.upper()}:"
        )
        print(f"Total number of catchments in {self.domain.upper()}: {len(cats_total)}")

        if "nearest_dist_m" in df_cwt.columns:
            df_cwt_unmatched = df_cwt[~df_cwt["nearest_dist_m"].isna()]
            cats_unmatched = df_cwt_unmatched[self.div_col].unique().tolist()
            subs_unmatched = df_cwt_unmatched[self.id_col].unique().tolist()
            subs_unmatched_vpus = df_cwt_unmatched[self.vpu_col].unique().tolist()
            df_cwt_matched = df_cwt[df_cwt["nearest_dist_m"].isna()]
        else:
            cats_unmatched = []
            df_cwt_matched = df_cwt.copy()

        counts = df_cwt_matched[self.div_col].value_counts()
        print(
            f"Number of catchments matched with nearest neighor (i.e., no overlapping): {len(cats_unmatched)}, {round(len(cats_unmatched) / len(cats_total) * 100, 2)}%"
        )
        for count in [1, 2, 3]:
            num_cats = (counts == count).sum()
            print(
                f"Number of catchments mapped to {count} {self.attr_dataset.upper()} subbasin(s): {num_cats}, {round(num_cats / len(cats_total) * 100, 2)}%"
            )
        cats_other = counts[counts > 3].index.unique()
        print(
            f"Number of catchments mapped to more than 3 {self.attr_dataset.upper()} subbains: {len(cats_other)}, {round(len(cats_other) / len(cats_total) * 100, 2)}%"
        )

        # Compute accumulated overlap for each divide_id
        accum_overlap = df_cwt_matched.groupby(self.div_col)["overlap_percentage"].sum()

        # Compute summary statistics on the accumulated values
        summary = accum_overlap.describe()

        # write summary statistics to file
        summary_file = Path(
            Path(self.cwt_file).parent,
            f"ngen_cwt_{self.attr_dataset}_summary_{self.domain.lower()}.txt",
        ).expanduser()
        with open(summary_file, "w") as f:
            f.write(str(summary))
        print(f"Summary statistics of overlap coverage saved to {summary_file}")

        # save nearest neighbor unmatched catchments and subbasins to file
        if len(cats_unmatched) > 0:
            unmatched_file = Path(
                Path(self.cwt_file).parent,
                f"ngen_catchments_nearest_{self.attr_dataset}_subbasins_{self.domain.lower()}.parquet",
            ).expanduser()
            print(
                f"\nSaving nearest neighbor unmatched catchments and subbasins to {unmatched_file}..."
            )
            df_cwt_unmatched.to_parquet(
                unmatched_file,
                engine="pyarrow",
                index=False,
            )

        # plot nearest neighbor matches
        if len(cats_unmatched) > 0:
            print(
                "\nPlotting nearest neighbor matched catchments and subbasins... "
                "Attributes will not be derived for these catchments due to insufficient overlap with attribute data coverage. "
            )
            self.plot_cats_subs(
                cats=cats_unmatched,
                subs=subs_unmatched,
                vpus=subs_unmatched_vpus,
            )

    def plot_cats_subs(self, cats: list, subs: list, vpus: list = None):
        """Plot NextGen catchments and corresponding attribute dataset subbasins."""
        if not cats:
            print("No catchments to plot.")
            return

        print(
            "Get corresponding NextGen catchments and attribute dataset sub-basins for plotting..."
        )
        gdf_cats = gpd.GeoDataFrame()
        gdf_subs = gpd.GeoDataFrame()
        for vpu in vpus:
            # get NextGen catchments for the vpu
            shp_vpu = self.get_vpu_gpd(vpu)
            shp_vpu = shp_vpu[[self.div_col, "geometry"]]
            shp_vpu = shp_vpu[shp_vpu[self.div_col].isin(set(cats))].copy()
            gdf_cats = pd.concat([gdf_cats, shp_vpu], ignore_index=True)
            del shp_vpu
            gc.collect()

            # get attribute dataset sub-basins for the vpu
            hf_file = self.get_nhdplus_shp_file_for_vpu(vpu)
            gdf_all = gpd.read_file(
                hf_file,
                layer=self.layer,
                columns=[self.id_col, "geometry"],
            )
            gdf_subs_vpu = gdf_all[gdf_all[self.id_col].isin(set(subs))].copy()
            gdf_subs = pd.concat([gdf_subs, gdf_subs_vpu], ignore_index=True)
            del gdf_all, gdf_subs_vpu
            gc.collect()

        if gdf_cats.empty:
            print("No NextGen catchments found for plotting.")
            return
        if gdf_subs.empty:
            print("No attribute dataset subbasins found for plotting.")
            return

        # plot
        fig, ax = plt.subplots(figsize=(12, 6))
        gdf_subs = gdf_subs.to_crs(epsg=4326)
        gdf_cats = gdf_cats.to_crs(epsg=4326)

        gdf_subs.plot(ax=ax, color="lightgray", edgecolor="black", linewidth=5.0)
        gdf_cats.plot(ax=ax, color="none", edgecolor="red", linewidth=1.0)
        plt.title(
            f"{self.domain.upper()} NextGen catchments (red) and corresponding nearest-neighbour "
            f"{self.attr_dataset.upper()} subbasins (black)"
        )

        # save plot
        plot_file = Path(
            Path(self.cwt_file).parent,
            f"ngen_catchments_nearest_{self.attr_dataset}_subbasins_{self.domain.lower()}.png",
        ).expanduser()
        plot_file.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(plot_file, dpi=300)
        plt.close()
        print(f"Plot saved to {plot_file}")

    def gather_streamcat_attrs(self) -> pd.DataFrame:
        """Gather StreamCat attribute dataframes and descriptions for NextGen catchments.

        Returns:
            DataFrame containing gathered StreamCat attributes

        """
        # Streamcat metrics metadata
        streamcat_dir = Path(self.attr_data_dir).expanduser()
        file_metrics = streamcat_dir / "StreamCatMetrics.csv"
        df_metrics = pd.read_csv(file_metrics, encoding="latin1")

        # check which streamcat attribute files exist in the lynker directory
        tables = df_metrics["final_table"].unique().tolist()
        files = [
            streamcat_dir / "lynker" / f"streamcat_{table}_cat.parquet"
            for table in tables
        ]
        existing_files = [f for f in files if f.is_file()]

        # loop through each existing file and gather attributes
        df_list = []
        for file in existing_files:
            print(f"Processing StreamCat attribute file: {file}")
            df_attr = pd.read_parquet(file)

            # get required attributes and descriptions from df_metrics
            table_name = file.stem.replace("streamcat_", "").replace("_cat", "")
            df_metric_table = df_metrics[df_metrics["final_table"] == table_name][
                ["metric_name", "metric_description"]
            ]
            df_metric_table["attr"] = df_metric_table["metric_name"]

            # remove "[AOI]" suffix if present in attr names
            df_metric_table["attr"] = df_metric_table["attr"].str.replace(
                "[AOI]", "", regex=False
            )

            # remove "8110" prefix if present
            df_metric_table["attr"] = df_metric_table["attr"].str.replace(
                "8110", "", regex=False
            )

            # remove "[Year]" suffix if present
            df_metric_table["attr"] = df_metric_table["attr"].str.replace(
                "[Year]", "", regex=False
            )

            # add "Cat" suffix to attr names in df_attr
            df_metric_table["attr"] = df_metric_table["attr"] + "Cat"

            attrs_needed = df_metric_table["attr"].tolist()
            print(f"Attributes needed from {file.name}: {attrs_needed}")
            # check if attributes exist in df_attr
            missing_attrs = [
                attr for attr in attrs_needed if attr not in df_attr.columns
            ]
            if missing_attrs:
                print(
                    f"Warning: The following attributes are missing in {file.name}: {missing_attrs}. "
                    f"Skipping these attributes."
                )

                # use attributes that exist in df_attr
                attrs_needed = [
                    attr for attr in attrs_needed if attr in df_attr.columns
                ]
                df_metric_table = df_metric_table[
                    df_metric_table["attr"].isin(attrs_needed)
                ]

            if not attrs_needed:
                print(f"No valid attributes found in {file.name}. Skipping this file.")
                continue

            df_attr = df_attr[["COMID"] + attrs_needed]
            df_list.append(df_attr)

        df_attr = self.process_streamcat_attrs(df_list)

        return df_attr

    def process_streamcat_attrs(self, df_list):
        """Process StreamCat attributes and merge with NextGen catchments.

        Args:
            df_list: List of DataFrames containing StreamCat attributes.

        """
        # merge all attribute dataframes on COMID
        df_attrs = df_list[0]
        for df in df_list[1:]:
            df_attrs = df_attrs.merge(df, on="COMID", how="outer")

        # remove "Cat" suffix from column names
        df_attrs.columns = [col.replace("Cat", "") for col in df_attrs.columns]

        # rename COMID to be consistent with crosswalk
        df_attrs.rename(columns={"COMID": "FEATUREID"}, inplace=True)

        return df_attrs

    def compute_weighted_attrs(
        self,
        df_attrs: pd.DataFrame,
        attrs: list,
    ):
        """Compute area-weighted StreamCat attributes for NextGen catchments.

        Args:
            df_attrs: DataFrame containing StreamCat attributes.
            attrs: List of StreamCat attributes to process.

        """
        # read the crosswalk file
        df_cwt = pd.read_parquet(self.cwt_file)

        # remove rows where no overlapping subbasin were found (hence the nearest subbasins were identified instead; not used here)
        if "nearest_dist_m" in df_cwt.columns:
            df_cwt = df_cwt[df_cwt["nearest_dist_m"].isna()]

        # merge attributes dataset with crosswalk
        df_attrs1 = df_attrs.merge(df_cwt, on=self.id_col, how="inner")

        # Multiply attribute values by weights (overlap percentage)
        weighted = (
            df_attrs1[attrs].multiply(df_attrs1["overlap_percentage"], axis=0).copy()
        )
        weighted[self.div_col] = df_attrs1[self.div_col].values

        # Group by catchment and compute sum
        weighted_sum = weighted.groupby(self.div_col).sum(min_count=1)

        # Divide by sum of weights per group to get weighted mean
        sum_weights = df_attrs1.groupby(self.div_col)["overlap_percentage"].sum()
        weighted_mean = (
            weighted_sum[attrs].div(sum_weights.replace(0, pd.NA), axis=0).reset_index()
        )

        return weighted_mean

    def gather_ngen_attrs(self) -> pd.DataFrame:
        """Gather NGEN attribute dataframes for NextGen catchments."""
        vpu_list = self.get_vpu_list()
        df_attrs = pd.DataFrame()
        for vpu in vpu_list:
            df_attr_vpu = self.get_vpu_gpd(vpu)
            df_attrs = pd.concat([df_attrs, df_attr_vpu], ignore_index=True)

        return df_attrs

    def filter_attrs_by_list(self, df_attrs: pd.DataFrame) -> pd.DataFrame:
        """Filter attributes based on the specified attribute list in the configuration."""
        if self.attr_list_file:
            attr_list = (
                pd.read_csv(
                    self.attr_list_file,
                    usecols=["attr_name"],
                    sep=",",
                    quotechar='"',
                    skipinitialspace=True,
                    on_bad_lines="skip",
                )["attr_name"]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

            if not attr_list or attr_list == [""]:
                print(
                    f"Warning: No attributes found in {self.attr_list_file}. All attributes will be processed."
                )
                return df_attrs

            if self.id_col not in df_attrs.columns:
                raise KeyError(
                    f"id_col '{self.id_col}' not found in DataFrame columns."
                )

            existing_attrs = [attr for attr in attr_list if attr in df_attrs.columns]
            missing_attrs = [attr for attr in attr_list if attr not in df_attrs.columns]
            if missing_attrs:
                print(
                    f"Warning: The following attributes are missing in {self.attr_file}: {missing_attrs}. "
                    f"Only existing attributes will be processed."
                )
            df_attrs = df_attrs[[self.id_col] + existing_attrs].copy()

        return df_attrs

    def gather_attrs(self) -> pd.DataFrame:
        """Gather attributes for NextGen catchments based on the specified attribute dataset."""
        # gather attributes for the attribute dataset
        if self.attr_dataset.lower() == "streamcat":
            df_attrs = self.gather_streamcat_attrs()
        elif self.attr_dataset.lower() in ["hlr", "hydroatlas"]:
            df_attrs = gpd.read_file(self.hf_file, layer=self.layer)
        elif self.attr_dataset.lower() == "ngen":
            df_attrs = self.gather_ngen_attrs()
        else:
            raise ValueError(f"Unsupported attribute dataset: {self.attr_dataset}")

        # filter attributes based on the specified attribute list in the configuration (if provided)
        df_attrs = self.filter_attrs_by_list(df_attrs)

        return df_attrs

    def derive_attrs(self):
        """Derive attributes for NextGen catchments based on the specified attribute dataset."""
        if Path(self.attr_file).exists():
            print(
                f"Attribute file for {self.attr_dataset} already exists at {self.attr_file}. "
                f"Remove existing file to re-run attribute processing if needed."
            )
            return

        # gather attributes for the attribute dataset
        df_attrs = self.gather_attrs()

        if self.attr_dataset.lower() != "ngen":
            # compute weighted attributes
            if not Path(self.cwt_file).exists():
                raise FileNotFoundError(f"CWT file not found at {self.cwt_file}")

            print(
                f"\nComputing weighted attributes for {self.attr_dataset.upper()} for {self.domain.upper()} NextGen catchments..."
            )

            attrs = df_attrs.columns.tolist()
            attrs.remove(self.id_col)
            # if len(attrs) > 100, break into chunks to reduce memory usage
            if len(attrs) > 100:
                print(
                    f"Number of attributes to process is large ({len(attrs)}). Processing in chunks to reduce memory usage..."
                )
                chunk_size = 50
                df_attrs_weighted = pd.DataFrame(index=df_attrs[self.id_col])

                chunks = []
                for i in range(0, len(attrs), chunk_size):
                    attrs_chunk = attrs[i : i + chunk_size]
                    df_chunk = self.compute_weighted_attrs(
                        df_attrs[[self.id_col] + attrs_chunk], attrs_chunk
                    )
                    df_chunk = df_chunk.set_index(self.div_col)
                    chunks.append(df_chunk)

                    del df_chunk
                    gc.collect()

                # concatenate all chunks together and reset index
                df_attrs_weighted = pd.concat(chunks, axis=1).reset_index()

            else:
                df_attrs_weighted = self.compute_weighted_attrs(df_attrs, attrs)
        else:
            # for NGEN attributes, just keep all attributes (no weighting needed since it's already at catchment level)
            df_attrs_weighted = df_attrs.copy()

        # make sure div_col column is string type
        df_attrs_weighted[self.div_col] = (
            df_attrs_weighted[self.div_col].astype("Int64").astype("string")
        )

        # save attr data to parquet file
        gc.collect()
        Path(self.attr_file).parent.mkdir(parents=True, exist_ok=True)
        df_attrs_weighted.to_parquet(self.attr_file, engine="pyarrow")
        print(f"Saved processed {self.attr_dataset} attributes to {self.attr_file}")

        return df_attrs_weighted


def main(config_file: Path):
    """Create crosswalk table and process attributes."""
    # read yaml config file
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # create ProcessAttrDataset instance
    proc = ProcessAttrDataset(**config)

    attr = proc.attr_dataset.upper()
    domain = proc.domain.upper()

    # create crosswalk table
    if proc.process_cwt:
        if attr.lower() == "ngen":
            print(
                f"CWT processing for {attr} attributes is not needed since {attr} attributes are already provided for NextGen catchments."
            )
        else:
            print(
                f"\n----------- Processing crosswalk for {attr}, {domain} -----------"
            )
            proc.process_crosswalk()

    # analyze crosswalk table results
    if proc.analyze_cwt:
        if attr.lower() == "ngen":
            print(
                f"CWT analysis for {attr} attributes is not needed since {attr} attributes are already provided for NextGen catchments."
            )
        else:
            print(f"\n----------- Analyzing crosswalk for {attr}, {domain} -----------")
            proc.analyze_cwt_results()

    # process attributes
    if proc.process_attr:
        print(f"\n---------- Processing attributes for {attr}, {domain} ----------")
        proc.derive_attrs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process attributes for NextGen catchments."
    )
    parser.add_argument(
        "config_file",
        type=Path,
        help="Path to the YAML configuration file.",
    )
    args = parser.parse_args()
    main(args.config_file)
