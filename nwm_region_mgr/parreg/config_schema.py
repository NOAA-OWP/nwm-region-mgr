"""Defines classes for validating the configuration."""

import logging
from pathlib import Path
from typing import Dict, List, Literal, get_args

import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, model_validator

from nwm_region_mgr.utils import BaseConfig, BaseGeneralConfig, read_table

logger = logging.getLogger(__name__)


class GeneralConfig(BaseGeneralConfig):
    """General configuration settings specific to parameter regionalization."""

    n_procs: int = Field(
        description="Number of processors to use for parallel processing. Set to -1 to use all available processors.",
        default=1,
        examples="-1",
    )

    attr_dataset_list: List[Literal["ngen", "hlr"]] = Field(
        description="List of attribute dataset names to use. Valid options include 'ngen', 'hlr'.",
        examples=["hlr"],
        default=[],
    )

    algorithm_list: List[
        Literal["gower", "urf", "kmeans", "kmedoids", "hdbscan", "birch"]
    ] = Field(
        description="Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch').",
        examples=["gower", "kmeans"],
        default=[],
    )

    manual_pairings_file: Path | str | None = Field(
        description="Path to the manual pairings file. If provided, this file will be used to specify manual donor-receiver pairings.",
        examples="pairs_kmeans_conus_vpu09.parquet",
        default=None,
    )

    # nested_gages: Optional[str] = "inner"
    # """How to handle nested gages in the calibration basin. Options: 'inner' (use inner gage), 'outer' (use outer gage)."""


class MetricEvalPeriod(BaseModel):
    """Configuration for the evaluation period of metrics to be used for screening donors."""

    col_name: str = Field(
        description="Name of the column in the donor stats file that contains the evaluation period.",
        examples="evalPeriod",
    )

    value: str = Field(
        description="Value of the evaluation period to filter the donor stats file.",
        examples="full",
    )


class MetricThreshold(BaseModel):
    """Configuration for the thresholds of metrics to be used for screening donors."""

    min: float | None = Field(
        description="Minimum threshold for the metric. If None, no minimum threshold is applied.",
        examples=0.4,
        default=None,
    )

    max: float | None = Field(
        description="Maximum threshold for the metric. If None, no maximum threshold is applied.",
        examples=0.9,
        default=None,
    )

    absolute: bool | None = Field(
        description="If True, apply the absolute value of the metric before applying the thresholds.",
        examples=False,
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
        description="Dictionary of metric thresholds to be used for screening donors.",
        examples={"cor": {"min": 0.4}},
        default=None,
    )

    def get_qualified_donors(
        self,
        config: BaseModel,
        # vpu: str = None,
        donors0: list = None,
        init_donor_df: pd.DataFrame = None,
        # stats_file: str | Path = None,
        # id_name: str = "divide_id",
    ) -> list:
        """Screen donors based on the metric thresholds and evaluation period."""
        divide_id_name = config.general.id_col.get("divide", "divide_id")
        gage_id_name = config.general.id_col.get("gage", "gage_id")

        # initial donors
        donors = [
            d for d in init_donor_df[gage_id_name].unique().tolist() if d in donors0
        ]
        donor_cats = (
            init_donor_df.loc[init_donor_df[gage_id_name].isin(donors), divide_id_name]
            .unique()
            .tolist()
        )

        # read the donor stats file
        stats_file = config.general.calval_stats_file
        df = read_table(stats_file, dtype={gage_id_name: str})

        # filter based on initial donors
        df = df[df[gage_id_name].isin(donors)]
        if df.empty:
            logger.warning(
                f"No matching gages found in {stats_file} for the initial donors. Returning the initial list."
            )
            return {gage_id_name: donors, divide_id_name: donor_cats}
        else:
            gages_stat = df[gage_id_name].unique().tolist()
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

        # filter based on metric thresholds
        for col, threshold in self.metric_threshold.items():
            if threshold.absolute:
                df[col] = df[col].abs()
            if threshold.min is not None:
                df = df[df[col] >= threshold.min]
            if threshold.max is not None:
                df = df[df[col] <= threshold.max]

        donors = df[gage_id_name].unique().tolist()
        donor_cats = (
            init_donor_df[init_donor_df[gage_id_name].isin(donors)][divide_id_name]
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

        return {gage_id_name: donors, divide_id_name: donor_cats}


class AttrDatasetConfig(BaseModel):
    """Configuration for attribute datasets used in the regionalization process."""

    attr_list: list | None = Field(
        description="List of attributes to use from this dataset.",
        examples=["attr1"],
        default=None,
    )
    attr_select_file: Path | str | None = Field(
        description="Path to file where attribute list may be found.",
        examples=["attr_selection_ngen.csv"],
        default=None,
    )
    attr_data_file: Path | str | None = Field(
        description="Path to file where attribute data may be found.",
        examples=["attr_ngen_{domain}.parquet"],
        default=None,
    )
    base_attr_list: list | None = Field(
        description="List of 'base' attributes to use from this dataset.",
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
        if self.attr_list:
            # make sure attr_list is valid
            attrs1 = [
                x
                for x in self.attr_list
                if x not in pq.ParquetFile(self.attr_data_file).schema.names
            ]
            if attrs1:
                msg = f"These attributes {attrs1} are not found in {self.attr_data_file}. Please check the configuration."
                logger.error(msg)
                raise ValueError(msg)
        else:
            attr_select_path = Path(self.attr_select_file)
            if not attr_select_path.exists():
                raise FileNotFoundError(
                    f"Select file not found: {self.attr_select_file}"
                )

            df_attrs = pd.read_csv(attr_select_path)

            if "select" not in df_attrs.columns or "attr_name" not in df_attrs.columns:
                raise ValueError(
                    f"Missing required columns 'select' and/or 'attr_name' in file: {self.attr_select_file}"
                )

            self.attr_list = df_attrs[df_attrs["select"] == 1]["attr_name"].to_list()

    def get_attr_data(self, id_name: str = "divide_id") -> pd.DataFrame:
        """Load attribute data filtered by selected attributes."""
        self._get_selected_attrs()

        if not self.attr_data_file:
            raise FileNotFoundError("No attr_data_file provided.")

        attr_data_path = Path(self.attr_data_file)
        if not attr_data_path.exists():
            raise FileNotFoundError(
                f"Attribute data file not found: {self.attr_data_file}"
            )

        suffix = attr_data_path.suffix.lower()
        if suffix == ".csv":
            df_data = pd.read_csv(attr_data_path)
        elif suffix == ".parquet":
            df_data = pd.read_parquet(attr_data_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

        missing_cols = set(self.attr_list) - set(df_data.columns)
        if missing_cols:
            raise ValueError(f"Missing attributes in data file: {missing_cols}")

        return df_data[[id_name] + self.attr_list]


class SnowCoverConfig(BaseModel):
    """Configuration for snow cover data."""

    consider_snowness: bool | None = Field(
        description="Whether to consider snow cover data in the regionalization process.",
        examples=False,
        default=False,
    )

    snow_cover_file: Path | str | dict[str, Path | str] | None = Field(
        description="Path to the snow cover data file, or a dictionary with VPU as keys and file paths as values.",
        examples="vpu{vpu_list}_snow_frac.parquet",
        default=None,
    )

    column: str | None = Field(
        description="Column name in the snow cover data file that contains the snow cover percentage.",
        examples="snow_pc_hydroatlas",
        default=None,
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
    """General algorithm class."""

    min_snow_frac: float
    max_spa_dist: float
    max_attr_diff: Dict[str, float]
    n_donor_max: int
    min_var_pca: float


class Gower(AlgoGeneral):
    """Gower algorithm class."""

    min_attr_dist: float
    max_attr_dist: float
    min_spa_dist: float
    n_donor_max: int
    zero_spa_dist: float


class URF(AlgoGeneral):
    """Unsupervised Rand Forest (URF) algorithm class."""

    pca: bool
    n_trees: int
    max_depth: int
    min_attr_dist: float
    max_attr_dist: float
    min_spa_dist: float
    n_donor_max: int
    zero_spa_dist: float


class KMeans(AlgoGeneral):
    """K-means algorithm class."""

    n_donor_max: int
    n_iter_max: int
    init: str
    n_init: int


class KMedoids(AlgoGeneral):
    """K-medoids algorithm class."""

    n_donor_max: int
    n_iter_max: int
    init: str


class HDBSCAN(AlgoGeneral):
    """Hierarchical Density Based Spatial Clustering of Applications with Noise (HDBSCAN) algorithm class."""

    n_donor_max: int
    min_cluster_size: int


class Birch(AlgoGeneral):
    """Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH) algorithm class."""

    n_donor_max: int
    branching_factor: int
    min_thresh: float
    max_thresh: float
    max_resample: int


class AlgorithmConfig(BaseModel):
    """Algorithm configuration class."""

    algo_general: AlgoGeneral = Field(
        description="Base config for all algorithms.",
        default_factory=AlgoGeneral,
    )
    gower: Gower | None = Field(default=None)
    urf: URF | None = Field(default=None)
    kmeans: KMeans | None = Field(default=None)
    kmedoids: KMedoids | None = Field(default=None)
    hdbscan: HDBSCAN | None = Field(default=None)
    birch: Birch | None = Field(default=None)

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
    attr_datasets: dict[
        Literal["hlr", "ngen", "hydroatlas", "streamcat", "nhdplus", "camels"],
        AttrDatasetConfig,
    ] = Field(
        description="Configuration for attribute datasets that can be used in the regionalization process.",
        examples={
            "ngen": {
                "attr_list": None,
                "attr_select_file": "attr_selection_ngen.csv",
                "attr_data_file": "attr_ngen_{domain}.parquet",
                "base_attr_list": ["elevation", "slope", "aspect"],
            }
        },
    )
    snow_cover: SnowCoverConfig = Field(
        description="Configuration for snow cover data.",
        default_factory=SnowCoverConfig,
    )
    algorithms: AlgorithmConfig = Field(
        description="Algorithm configuration class.  See specific algorithms for additional arguments.",
        default_factory=AlgorithmConfig,
    )

    @model_validator(mode="after")
    def check_required_algorithms_present(self):
        """Check if required algorithms are present."""
        required = set(self.general.algorithm_list)
        defined = set(self.algorithms.model_dump(exclude_unset=True).keys())

        missing = required - defined
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
