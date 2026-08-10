"""Defines classes for validating the configuration for parameter regionalization.

Classes:
    - GeneralConfig: General configuration settings specific to parameter regionalization.
    - DonorConfig: Configuration for donor selection.
    - AttrDatasetConfig: Configuration for attribute datasets used in the regionalization process.
    - AvailableAttrsConfig: Configuration for available attribute datasets for use in the regionalization process.
    - SnowCoverConfig: Configuration for snow cover data.
    - AlgorithmConfig: Algorithm configuration class.
    - ParameterOutputConfig: Configuration for parameter regionalization output.
    - Config: Top-level configuration class for parameter regionalization.
"""

import logging
from pathlib import Path
from typing import Dict, List, Literal, get_args

import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, model_validator

from nwm_region_mgr.utils import (
    BaseConfig,
    BaseGeneralConfig,
    BaseOutputConfig,
    read_table,
)

logger = logging.getLogger(__name__)


class GeneralConfig(BaseGeneralConfig):
    """General configuration settings specific to parameter regionalization."""

    attr_dataset_list: List[Literal["ngen", "hlr", "streamcat", "hydroatlas"]] = Field(
        description="List of attribute dataset names to use. Valid options include 'ngen', 'hlr', 'streamcat', 'hydroatlas'.",
        examples=["ngen", "streamcat"],
        default=["ngen"],
    )

    algorithm_list: List[
        Literal["gower", "urf", "kmeans", "kmedoids", "hdbscan", "birch", "proximity"]
    ] = Field(
        description="Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch', 'proximity').",
        examples=["gower", "kmeans"],
        default=["gower"],
    )

    manual_pairings_file: Path | str | Dict[str, Path] | Dict[str, str] | None = Field(
        description=(
            "Path to the manual pairings file. If provided, this file will be used to specify "
            "manual donor-receiver pairings, overriding the algorithmic selections."
        ),
        examples="{static_data_dir}/region/manual_pairings/manual_pairs_{vpu_list}.csv",
        default=None,
    )


class MetricEvalPeriod(BaseModel):
    """Configuration for the evaluation period of metrics to be used for screening donors."""

    col_name: str | None = Field(
        description=(
            "Name of the column in the donor stats file that contains the evaluation period. "
            "No filtering by evaluation period if None."
        ),
        examples="evalPeriod",
        default=None,
    )

    value: str | None = Field(
        description=(
            "Value of the evaluation period to filter donor stats. No filtering by evaluation period if None."
        ),
        examples="full",
        default=None,
    )


class MetricThreshold(BaseModel):
    """Configuration for the thresholds of metrics to be used for screening donors."""

    min: float | None = Field(
        description="Minimum threshold for the metric. If None, no minimum threshold is applied.",
        examples=None,
        default=None,
    )

    max: float | None = Field(
        description="Maximum threshold for the metric. If None, no maximum threshold is applied.",
        examples=None,
        default=None,
    )

    absolute: bool | None = Field(
        description="If True, apply the absolute value of the metric before applying the thresholds.",
        examples=None,
        default=False,
    )

    @model_validator(mode="after")
    def validate_either_field_exists(self):
        """Validate that at least one of 'min' or 'max' is provided."""
        if not self.min and not self.max:
            raise ValueError("At least one of 'min' or 'max' must be provided.")
        return self


class DonorConfig(BaseModel):
    """Configuration for donor selection."""

    buffer_km: float | None = Field(
        description="Size of buffer (in km) around current VPU to identify qualified donors.",
        examples=100.0,
        default=0.0,
    )

    metric_eval_period: MetricEvalPeriod | None = Field(
        description="Evaluation period of metrics to be used for screening donors.",
        examples={"col_name": "eval_period", "value": "full"},
        default=None,
    )

    metric_threshold: Dict[str, MetricThreshold] = Field(
        description=(
            "Dictionary of metric thresholds to be used for screening donors. Each key is a metric name, and "
            "metric names must match columns in the calibration/validation stats file (case sensitive). "
            "The value is a MetricThreshold object specifying the min, max, and absolute settings. "
            "Refer to schema of MetricThreshold for details."
        ),
        examples={
            "cor": {"min": 0.4, "max": None, "absolute": False},
            "kge": {"min": 0.2, "max": None, "absolute": False},
        },
        default=None,
    )

    def get_qualified_donors(
        self,
        config: BaseModel,
        donors0: list = None,
        init_donor_df: pd.DataFrame = None,
    ) -> list:
        """Screen donors based on the metric thresholds and evaluation period."""
        div_col = getattr(config.general.id_col, "divide", "div_id")
        gage_col = getattr(config.general.id_col, "gage", "gage_id")

        # initial donors
        donors = [d for d in init_donor_df[gage_col].unique().tolist() if d in donors0]
        donor_cats = (
            init_donor_df.loc[init_donor_df[gage_col].isin(donors), div_col]
            .unique()
            .tolist()
        )

        # read the donor stats file
        stats_file = config.general.calval_stats_file
        df = read_table(stats_file, dtype={gage_col: str})

        # filter based on initial donors
        df = df[df[gage_col].isin(donors)]
        if df.empty:
            logger.warning(
                f"No matching gages found in {stats_file} for the initial donors. Returning the initial list."
            )
            return {gage_col: donors, div_col: donor_cats}
        else:
            gages_stat = df[gage_col].unique().tolist()
            gages_missing = [g for g in donors if g not in gages_stat]
            if gages_missing:
                logger.warning(
                    f"Some gages in the initial list are not found in the stats file: {stats_file} "
                )
                logger.debug(f"Missing gages: {gages_missing}")

        # filter based on the evaluation period
        if self.metric_eval_period:
            periods = df[self.metric_eval_period.col_name].unique()
            if self.metric_eval_period.value not in periods:
                raise ValueError(
                    f"Column {self.metric_eval_period.value} not found in {stats_file}."
                )
            else:
                # Filter the DataFrame based on the evaluation period
                df = df[
                    df[self.metric_eval_period.col_name]
                    == self.metric_eval_period.value
                ]
        else:
            logger.warning(
                f"No evaluation period provided. Using all periods in {stats_file}."
            )

        # build mapping of lower-case column names to actual column names to allow case-insensitive matching of metric names
        col_map = {c.lower(): c for c in df.columns}

        # filter based on metric thresholds
        for col, threshold in self.metric_threshold.items():
            col_key = col.lower()

            if col_key not in col_map:
                raise KeyError(
                    f"Column '{col}' not found in {stats_file} (case-insensitive match failed)."
                )

            actual_col = col_map[col_key]

            if threshold.absolute:
                df[actual_col] = df[actual_col].abs()
            if threshold.min is not None:
                df = df[df[actual_col] >= threshold.min]
            if threshold.max is not None:
                df = df[df[actual_col] <= threshold.max]

        donors = df[gage_col].unique().tolist()
        donor_cats = (
            init_donor_df[init_donor_df[gage_col].isin(donors)][div_col]
            .unique()
            .tolist()
        )

        logger.info(
            f"Number of donors after filtering: {len(donors)} gages, {len(donor_cats)} catchments"
        )

        # check if any donors are left after filtering
        if not donors:
            logger.info(
                "No donors left after filtering. Check the metric thresholds and evaluation period."
            )

        return {gage_col: donors, div_col: donor_cats}


class AttrDatasetConfig(BaseModel):
    """Configuration for attribute datasets used in the regionalization process."""

    attr_list: list | None = Field(
        description=(
            "List of attributes to use from this dataset. If not provided, attributes will be determined "
            "from attr_select_file. Either this field or attr_select_file must be provided."
            "If both are provided, attr_list takes priority."
        ),
        examples=None,
        default=None,
    )
    attr_select_file: Path | str | None = Field(
        description="Path to file where selection of attributes to use during regionalization may be found.",
        examples=["attr_selection_ngen.csv"],
        default=None,
    )
    attr_data_file: Path | str | None = Field(
        description="Path to file where attribute data may be found.",
        examples=["attr_ngen_{domain}.parquet"],
        default=None,
    )
    base_attr_list: list | None = Field(
        description=(
            "Small list of basic attributes during a 2nd round of pairing if no donor is found using "
            "the full set of selected attributes during the first round."
        ),
        examples=["elevation", "slope", "aspect"],
        default=None,
    )

    @model_validator(mode="after")
    def validate_either_field_exists(self):
        """Validate that at least one of 'attr_list' or 'attr_select_file' is provided."""
        if not self.attr_list and not self.attr_select_file:
            raise ValueError(
                "At least one of 'attr_list' or 'attr_select_file' must be provided."
                " If both are provided, 'attr_list' takes priority."
            )
        return self

    def _get_selected_attrs(self):
        """Private method to load the list of selected attributes."""
        # determine list of attributes to use from either attr_list or attr_select_file
        # if both are provided, attr_list takes priority
        if not self.attr_list:
            attr_select_path = Path(self.attr_select_file)
            if not attr_select_path.exists():
                raise FileNotFoundError(
                    f"Select file not found: {self.attr_select_file}"
                )

            df_attrs = read_table(attr_select_path)

            if "select" not in df_attrs.columns or "attr_name" not in df_attrs.columns:
                raise ValueError(
                    f"Missing required columns 'select' and/or 'attr_name' in file: {self.attr_select_file}"
                )

            self.attr_list = df_attrs[df_attrs["select"] == 1]["attr_name"].to_list()

        # check if attrs in attr_list are present in the attr_data_file
        attrs1 = [
            x
            for x in self.attr_list
            if x not in pq.ParquetFile(self.attr_data_file).schema.names
        ]
        if attrs1:
            msg = f"The following attributes are not found in {self.attr_data_file} and will be ignored: {attrs1}"
            logger.warning(msg)

            self.attr_list = [x for x in self.attr_list if x not in attrs1]

        # if final attr_list is empty after filtering, raise an error
        if not self.attr_list:
            msg = (
                "No valid attributes found based on the following configurations:\n"
                f"attr_list: {self.attr_list}\n"
                f"attr_select_file: {self.attr_select_file}\n"
                f"attr_data_file: {self.attr_data_file}\n"
            )
            logger.error(msg)
            raise ValueError(msg)

    def get_attr_data(self, id_name: str = "div_id") -> pd.DataFrame:
        """Load attribute data filtered by selected attributes."""
        self._get_selected_attrs()

        if not self.attr_data_file:
            raise FileNotFoundError("No attr_data_file provided.")

        attr_data_path = Path(self.attr_data_file)
        if not attr_data_path.exists():
            raise FileNotFoundError(
                f"Attribute data file not found: {self.attr_data_file}"
            )
        df_data = read_table(attr_data_path)

        missing_cols = set(self.attr_list) - set(df_data.columns)
        if missing_cols:
            raise ValueError(f"Missing attributes in data file: {missing_cols}")

        return df_data[[id_name] + self.attr_list]


class AvailableAttrsConfig(BaseModel):
    """Configuration for available attribute datasets for use in the regionalization process."""

    ngen: AttrDatasetConfig = Field(
        description=(
            "Configuration for NGEN attribute dataset."
            "(https://lynker-spatial.s3-us-west-2.amazonaws.com/hydrofabric/v2.2/hfv2.2-data_model.html)."
        ),
        examples={
            "attr_list": None,
            "attr_select_file": "{static_data_dir}/inputs/attr_config/attr_selection_ngen.csv",
            "attr_data_file": "{static_data_dir}/inputs/attr_datasets/ngen/attr_ngen_{domain}.parquet",
            "base_attr_list": ["elevation", "slope", "aspect"],
        },
    )

    hlr: AttrDatasetConfig = Field(
        description=(
            "Configuration for Hydrologic Landscape Regions (HLR) attribute dataset "
            "(https://www.usgs.gov/publications/hydrologic-landscape-regions-united-states)."
        ),
        examples={
            "attr_list": None,
            "attr_select_file": "{static_data_dir}/inputs/attr_config/attr_selection_hlr.csv",
            "attr_data_file": "{static_data_dir}/inputs/attr_datasets/hlr/attr_hlr_{domain}.parquet",
            "base_attr_list": ["PPT", "SAND"],
        },
    )

    streamcat: AttrDatasetConfig = Field(
        description=(
            "Configuration for StreamCat attribute dataset "
            "(https://www.epa.gov/national-aquatic-resource-surveys/streamcat-dataset)."
        ),
        examples={
            "attr_list": None,
            "attr_select_file": "{static_data_dir}/inputs/attr_config/attr_selection_streamcat.csv",
            "attr_data_file": "{static_data_dir}/inputs/attr_datasets/streamcat/attr_streamcat_{domain}.parquet",
            "base_attr_list": ["Precip_Minus_EVT", "Elev", "BFI"],
        },
    )

    hydroatlas: AttrDatasetConfig = Field(
        description=(
            "Configuration for HydroATLAS attribute dataset "
            "(https://www.hydrosheds.org/hydroatlas)."
        ),
        examples={
            "attr_list": None,
            "attr_select_file": "{static_data_dir}/inputs/attr_config/attr_selection_hydroatlas.csv",
            "attr_data_file": "{static_data_dir}/inputs/attr_datasets/hydroatlas/attr_hydroatlas_{domain}.parquet",
            "base_attr_list": ["ele_mt_sav", "dis_m3_pyr", "run_mm_syr", "pre_mm_syr"],
        },
    )


class SnowCoverConfig(BaseModel):
    """Configuration for snow cover."""

    consider_snowness: bool | None = Field(
        description=(
            "Whether to consider snow driven and non-snow driven catchments separately "
            "in the regionalization process. If True, snow-driven receivers will only consider "
            "snow-driven donors and non-snow-driven receivers will only consider non-snow-driven donors."
        ),
        examples=True,
        default=True,
    )

    snow_cover_file: Path | str | dict[str, Path | str] | None = Field(
        description="Path to the snow cover data file, or a dictionary with VPU as keys and file paths as values.",
        examples="{base_dir}/inputs/attr_datasets/hydroatlas/attr_hydroatlas_{domain}.parquet",
        default=None,
    )

    column: str | None = Field(
        description="Column name in the snow cover data file that contains the snow cover percentage.",
        examples="snw_pc_syr",
        default="snw_pc_syr",
    )

    threshold: float | None = Field(
        description="Threshold value for snow cover percentage to determine if a catchment is considered snow-driven.",
        examples="20",
        default=None,
    )

    @model_validator(mode="after")
    def validate_snow_cover_config(self):
        """Validate the snow cover configuration."""
        if self.consider_snowness:
            if not self.snow_cover_file or not self.column or not self.threshold:
                raise ValueError(
                    "When 'consider_snowness' is True, 'snow_cover_file', 'column', and 'threshold' must be provided."
                )

        return self


class AlgoGeneral(BaseModel):
    """General configurations shared by all regionalization algorithms."""

    max_spa_dist: float | None = Field(
        default=1000.0,
        description="Maximum spatial distance (km) to consider a donor suitable",
        examples=1500.0,
    )

    n_donor_max: int | None = Field(
        default=3,
        description="Maximum number of donors to keep that satisfy all criteria",
        examples=3,
    )
    min_var_pca: float | None = Field(
        default=0.9,
        description="Minimum total variance explained by chosen PCA components",
        examples=0.8,
    )


class Gower(AlgoGeneral):
    """Configurations for the distance-based algorithm Gower."""

    min_attr_dist: float | None = Field(
        default=0.1,
        description=(
            "Minimum attribute distance. If one or more donors have a distance to receiver "
            "smaller than this threshold, stop searching."
        ),
        examples=0.1,
    )

    max_attr_dist: float | None = Field(
        default=0.20,
        description=(
            "Maximum attribute distance. Donors with distance to receiver larger than this value are discarded, "
            "unless no donor smaller than this threshold is available."
        ),
        examples=0.25,
    )

    min_spa_dist: float | None = Field(
        default=100.0,
        description="Starting distance (km) to iteratively search for donors in the neighborhood",
        examples=200.0,
    )

    zero_spa_dist: float | None = Field(
        default=1.0,
        description=(
            "Distance threshold (in km) where receiver adopts a donor directly "
            "(i.e., donor/receiver are considered overlapping each other)"
        ),
        examples=1.0,
    )


class URF(AlgoGeneral):
    """Unsupervised Random Forest (URF) algorithm class."""

    pca: bool | None = Field(
        default=False,
        description=(
            "Whether to perform PCA on the attribute data before building the forest. "
            "Preliminary testing indicates limited difference in results with/without PCA."
        ),
        examples=False,
    )

    n_trees: int | None = Field(
        default=500,
        description="Number of trees in the random forest.",
        examples=500,
    )

    max_depth: int | None = Field(
        default=3,
        description=(
            "Maximum depth of each tree. If None, nodes are expanded until all leaves are pure."
        ),
        examples=3,
    )

    min_attr_dist: float | None = Field(
        default=None,
        description=(
            "Minimum attribute distance. If one or more donors have a distance to "
            "receiver smaller than this threshold, stop searching."
        ),
        examples=0.1,
    )

    max_attr_dist: float | None = Field(
        default=None,
        description=(
            "Maximum attribute distance. Donors with distance to receiver larger than this value are discarded, "
            "unless no donor smaller than this threshold is available."
        ),
        examples=0.25,
    )

    min_spa_dist: float | None = Field(
        default=None,
        description="Starting distance (km) to iteratively search for donors in the neighborhood",
        examples=200.0,
    )

    zero_spa_dist: float | None = Field(
        default=None,
        description=(
            "Distance threshold (in km) where receiver adopts a donor directly "
            "(i.e., donor/receiver are considered overlapping each other)"
        ),
        examples=1.0,
    )


class KMeans(AlgoGeneral):
    """K-means algorithm class."""

    n_iter_max: int | None = Field(
        default=100,
        description="Maximum number of iterations for the algorithm.",
        examples=100,
    )

    init: Literal["k-means++", "random"] | None = Field(
        default="k-means++",
        description="Method for initialization.",
        examples="k-means++",
    )

    n_init: int | None = Field(
        default=None,
        description="Number of times the k-means algorithm will be run with different centroid seeds.",
        examples=3,
    )


class KMedoids(AlgoGeneral):
    """K-medoids algorithm class."""

    n_iter_max: int | None = Field(
        default=None,
        description="Maximum number of iterations for the algorithm.",
        examples=100,
    )

    init: Literal["random", "heuristic", "k-medoids++", "build"] | None = Field(
        default="heuristic",
        description="Method for initialization.",
        examples="heuristic",
    )


class HDBSCAN(AlgoGeneral):
    """Hierarchical Density Based Spatial Clustering of Applications with Noise (HDBSCAN) algorithm class."""

    n_donor_max: int | None = Field(
        default=20,
        description="Maximum number of donors to keep that satisfy all criteria.",
        examples=20,
    )

    min_cluster_size: int | None = Field(
        default=3,
        description="Minimum size of clusters (to avoid being considered noise)",
        examples=3,
    )


class Birch(AlgoGeneral):
    """Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH) algorithm class."""

    branching_factor: int | None = Field(
        default=50,
        description="Branching factor for the BIRCH algorithm.",
        examples=50,
    )

    min_thresh: float | None = Field(
        default=1.5,
        description=(
            "Minimum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds "
            "between min_thresh and max_thresh to identify a suitable threshold."
        ),
        examples=1.5,
    )
    max_thresh: float | None = Field(
        default=4.0,
        description=(
            "Maximum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds "
            "between min_thresh and max_thresh to identify a suitable threshold."
        ),
        examples=4.0,
    )
    max_resample: int | None = Field(
        default=20,
        description="Maximum number of resamples.",
        examples=20,
    )


class AlgorithmConfig(BaseModel):
    """Algorithm configuration class."""

    algo_general: AlgoGeneral = Field(
        description="General configurations shared by all regionalization algorithms.",
        default_factory=AlgoGeneral,
    )

    gower: Gower = Field(
        description="Configurations for the distance-based algorithm Gower.",
        default_factory=Gower,
    )

    urf: URF = Field(
        description="Configurations for the distance-based algorithm Unsupervised Random Forest (URF)",
        default_factory=URF,
    )

    kmeans: KMeans = Field(
        description="Configurations for the clustering algorithm K-means",
        default_factory=KMeans,
    )

    kmedoids: KMedoids = Field(
        description="Configurations for the clustering algorithm K-medoids",
        default_factory=KMedoids,
    )

    hdbscan: HDBSCAN = Field(
        description=(
            "Configurations for the clustering algorithm Hierarchical Density Based Spatial Clustering of Applications with Noise (HDBSCAN)",
        ),
        default_factory=HDBSCAN,
    )

    birch: Birch = Field(
        description=(
            "Configurations for the clustering algorithm Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH)",
        ),
        default_factory=Birch,
    )

    @model_validator(mode="before")
    @classmethod
    def merge_algo_general(cls, values: dict) -> dict:
        """Merge general algorithm parameters with specific algorithm parameters."""
        general = values.get("algo_general")
        if not general:
            return values

        # dynamically find all optional algorithm fields (excluding 'algo_general')
        algo_fields = [
            field
            for field, annotation in cls.__annotations__.items()
            if field != "algo_general"
            and (
                # either directly the class or Optional[class]
                isinstance(annotation, type)
                or (get_args(annotation) and isinstance(get_args(annotation)[0], type))
            )
        ]

        # merge general parameters into each algorithm's parameters
        for key in algo_fields:
            if key in values and values[key] is not None:
                values[key] = {**general, **values[key]}

        return values


class ParameterOutputConfig(BaseModel):
    """Configuration for parameter regionalization output."""

    pairs: BaseOutputConfig = Field(
        description="Configuration for saving donor-receiver pairs.",
        default_factory=BaseOutputConfig,
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/pairs",
            "stem": "pairs_{algorithm_list}_{domain}_vpu{vpu_list}",
            "stem_suffix": "_mswm",  # suffix for the pairs file to be used by MSWM
            "format": "parquet",
            "plots": {
                "spatial_map": True,
                "histogram": True,
                "columns_to_plot": ["distSpatial", "distAttr"],  # columns to plot
            },
            "plot_path": "{base_dir}/outputs/{run_name}/pairs/plots",
        },
    )

    params: BaseOutputConfig = Field(
        description="Configuration for saving regionalized parameters.",
        default_factory=BaseOutputConfig,
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/params",
            "stem": "formulation_params_{algorithm_list}_{domain}_vpu{vpu_list}",
            "format": "csv",
            "plots": {
                "spatial_map": True,
                "columns_to_plot": ["MP", "MFSNO", "uztwm", "uzfwm", "pxtemp", "plwhc"],
            },
            "plot_path": "{base_dir}/outputs/{run_name}/params/plots",
        },
    )

    attr_data_final: BaseOutputConfig = Field(
        description=(
            "Configuration for saving and plotting final attribute data used in regionalization. "
            "Note only selected attributes are saved, and attribute names are prefixed with "
            "the name of the corresponding attribute source (e.g., 'Elev' in StreamCat becomes 'streamcat_Elev')."
        ),
        default_factory=BaseOutputConfig,
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/attr_data_final",
            "stem": "attr_{domain}_vpu{vpu_list}",
            "format": "parquet",
            "plots": {
                "spatial_map": True,
                "histogram": True,
                "columns_to_plot": [
                    "streamcat_Elev",
                    "streamcat_BFI",
                    "streamcat_Precip_Minus_EVT",
                    "hlr_PMPE",
                    "hlr_SAND",
                    "hlr_TAVE",
                ],  # attributes to plot
            },
            "plot_path": "{base_dir}/outputs/{run_name}/attr_data_final/plots",
        },
    )

    config_final: BaseOutputConfig = Field(
        description="Configuration for saving final configuration file used in regionalization.",
        default_factory=BaseOutputConfig,
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/config_parreg_final.yaml",
        },
    )

    spatial_distance: BaseOutputConfig = Field(
        description="Configuration for saving spatial distance data.",
        default_factory=BaseOutputConfig,
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/spatial_distance",
            "format": "parquet",
        },
    )


class Config(BaseConfig):
    """Configuration class."""

    general: GeneralConfig = Field(
        description="General configuration settings specific to parameter regionalization.",
        default_factory=GeneralConfig,
    )
    donor: DonorConfig = Field(
        description="Configuration for donor selection.",
        default_factory=DonorConfig,
    )
    attr_datasets: AvailableAttrsConfig = Field(
        description="Configuration for attribute datasets available for use in regionalization.",
        default_factory=AvailableAttrsConfig,
    )
    snow_cover: SnowCoverConfig = Field(
        description="Configuration for snow cover data to be used in determining whether catchments are snow-driven.",
        default_factory=SnowCoverConfig,
    )
    algorithms: AlgorithmConfig = Field(
        description="Algorithm configuration class.  See specific algorithms for additional arguments.",
        default_factory=AlgorithmConfig,
    )

    output: ParameterOutputConfig = Field(
        description="Configuration for parameter regionalization output.",
        default_factory=ParameterOutputConfig,
    )

    @model_validator(mode="after")
    def check_required_algorithms_present(self):
        """Check if required algorithms are present."""
        required = set(self.general.algorithm_list)
        defined = set(self.algorithms.model_dump(exclude_unset=True).keys())

        missing = required - defined
        missing = {
            m for m in missing if m != "proximity"
        }  # "proximity" appproch does not need algorithm parameters

        if missing:
            raise ValueError(
                f"The following algorithms are listed in 'general.algorithm_list' "
                f"but missing from the 'algorithms' section: {missing}"
            )
        return self

    @model_validator(mode="after")
    def check_required_attr_datasets_present(self):
        """Check that the required attributes are present."""
        required = set(self.general.attr_dataset_list)
        defined = set(self.attr_datasets.model_dump(exclude_unset=True).keys())

        missing = required - defined
        if missing:
            raise ValueError(
                f"The following attribute datasets are listed in 'general.attr_dataset_list' "
                f"but missing from the 'attr_datasets' section: {missing}"
            )
        return self
