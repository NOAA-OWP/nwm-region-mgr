"""Utility functions for loading and validating configuration files using Pydantic and YAML.

config_utils.py

Classes/Functions:
    - LoggingConfig: Pydantic model for logging configuration.
    - BaseGeneralConfig: Pydantic model for general settings of the application.
    - BaseOutputConfig: Pydantic model for output settings of the application.
    - BaseConfig: Pydantic model for the base configuration of the application.
    - BaseConfigProcessor: base class for processing and validating configurations
    - _deep_merge_configs: Recursively merge two dictionaries, with values from dict #2 overwriting those in dict #1.
    - _load_and_validate_config: Load a YAML file, validate its structure using Pydantic
    - _substitute_placeholders: Substitute placeholders in the config with actual values.
    - load_and_process_config: Load, validate, process, and save the configuration files.
    - _validate_paths: Validate that all file and directory paths exist.
    - _assemble_file_paths: Assemble file paths from the configuration.
    - _required_columns_calval_stats: Return a set of required columns for calibration/validation statistics.
    - _file_required_column_map: Return a dictionary mapping files to required columns.
    - PydanticDictLike: Stand-in for dictionary-like behavior when you want specificity of a pydantic model.
    - FieldCrosswalk: Mapping of column names for unique identifiers in all require files for regionalization.
    - LayerCrosswalk: Dictionary mapping layer names for hydrofabric files.

"""

import logging
import os
import re
from contextlib import contextmanager
from functools import lru_cache, reduce
from pathlib import Path
from time import time
from typing import Any, Dict, Iterator, List, Literal, Optional, Tuple, Union

import geopandas as gpd
import pandas as pd
import yaml
from pydantic import BaseModel, Field, ValidationError, model_validator

from nwm_region_mgr.utils.dict_utils import flatten_dict
from nwm_region_mgr.utils.io_utils import read_table, save_data
from nwm_region_mgr.utils.plot_utils import plot_histogram, plot_spatial_map
from nwm_region_mgr.utils.string_utils import recursive_substitute
from nwm_region_mgr.utils.validation_utils import (
    check_columns_dataframe,
    check_columns_hydrofabric,
    check_options,
)

logger = logging.getLogger(__name__)


class LoggingConfig(BaseModel):
    """Logging configuration for the application."""

    level: Literal["debug", "info", "warning", "error", "critical"] = Field(
        description="Logging level.", examples="debug", default="info"
    )

    log_to_file: bool = Field(
        description=(
            "Whether to log to a file. If set to True, logging messages will be written to "
            "the specified log file, in addition to the console."
        ),
        default=False,
        examples=False,
    )

    file: str | None = Field(
        description="Path to the log file. If not provided, logging will be written to console only.",
        examples="logfile.log",
        default=None,
    )

    @model_validator(mode="after")
    def check_log_level(self) -> "LoggingConfig":
        """Ensure that the log level is valid."""
        valid_levels = [
            "DEBUG",
            "INFO",
            "WARNING",
            "SEVERE",
            "FATAL",
        ]  # use standard Python log levels
        check_options(self.level.upper(), valid_levels, "log level")
        return self

    @model_validator(mode="after")
    def check_log_file(self) -> "LoggingConfig":
        """Ensure that the log file path is valid if logging to a file."""
        if self.log_to_file and not self.file:
            logger.error("If 'log_to_file' is True, 'file' must be specified.")

        return self


class PydanticDictLike(BaseModel):
    """Stand-in for dictionary-like behavior when you want specificity of a pydantic model."""

    @property
    def as_dict(self) -> dict[str, Any]:
        """Return the model as a dictionary."""
        return self.model_dump()

    def get(self, key: str, default=None):
        """Get a value from the model by key, with an optional default."""
        return getattr(self, key, default)

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Return an iterator over the model's (key, value) pairs."""
        return self.model_dump().items()

    def keys(self) -> Iterator[str]:
        """Return an iterator over the model's keys."""
        return self.model_dump().keys()

    def values(self) -> Iterator[Any]:
        """Return an iterator over the model's values."""
        return self.model_dump().values()

    def lower_case(self) -> "PydanticDictLike":
        """Return a new instance with all string fields lowercased."""
        data = {
            k: (v.lower() if isinstance(v, str) else v)
            for k, v in self.model_dump().items()
        }
        return self.__class__(**data)


class FieldCrosswalk(PydanticDictLike):
    """Mapping of column names for unique identifiers in all require files for regionalization."""

    divide: str = Field(
        description="Column name for divide (catchment) ID.", default="div_id"
    )

    gage: str = Field(description="Column name for gage (basin) ID.", default="gage_id")

    huc12: str = Field(description="Column name for HUC12 ID.", default="huc_12")

    vpu: str = Field(description="Column name for VPU ID.", default="vpu_id")

    drainage_area: str = Field(
        description="Column name for drainage area.", default="area_sqkm"
    )


class LayerCrosswalk(PydanticDictLike):
    """Dictionary mapping layer names for hydrofabric files."""

    huc12: str = Field(
        description="Layer name for HUC12 hydrofabric file.",
        default="WBDSnapshot_National",
    )

    ngen: str = Field(
        description="Layer name for NextGen hydrofabric file.", default="divides"
    )


class BaseGeneralConfig(BaseModel):
    """Base general settings for the formulation regionalization application."""

    run_name: str = Field(
        description="Name of the run, used to create output folders and files.",
        examples="test",
        default="test",
    )

    domain: Literal["conus", "ak", "hi", "prvi"] = Field(
        description="Which National Water Model Domain this run uses.",
        examples="conus",
        default="conus",
    )

    vpu: str = Field(
        description=(
            "Vector processing unit (VPU) to be processed within the domain. "
            "Valid VPUs for conus include 01,02,03N,03S,03W,04,05,06,07,08,09,10L,10U,11,12,13,14,15,16,17,18. "
            "Valid VPUs for ak, hi, prvi are 19, 20, 21, respectively."
        ),
        examples="03S",
        default="03S",
    )

    n_procs: int = Field(
        description="Number of processors to use for parallel processing. Set to -1 to use all available processors.",
        examples=2,
        default=-1,
    )

    base_dir: str = Field(
        description="Path to base directory for input/output files.",
        examples="~/run_region",
        default=None,
    )

    static_data_dir: str = Field(
        description="Path to static data directory containing hydrofabric and other static input files.",
        examples="/ngencerf-app/nwm-region-mgr/data/inputs",
        default=None,
    )

    ngen_hydrofabric_file: Path | str | Dict[str, Path] | Dict[str, str] = Field(
        description=(
            "Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' "
            "or 2) a dictionary mapping VPU strings to file paths, e.g., {'01': 'vpu_01.gpkg'}."
            "If providing a string with placeholders like {vpu}, they will be substituted accordingly and "
            "expanded to a dictionary mapping each VPU to its corresponding file."
            " This file must include columns 'div_id', 'vpu_id' and 'geometry'."
        ),
        examples="{static_data_dir}/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg",
        default=None,
    )

    gage_divide_cwt_file: Path | str = Field(
        description="Path to CSV or parquet file with gage divide CWTs, with columns 'div_id' and 'gage_id'.",
        examples=[
            "{static_data_dir}/region/cwt_divide_gage/calib_gage_divide_{domain}.parquet"
        ],
        default=None,
    )

    donor_gage_file: Path | str = Field(
        description="Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'.",
        examples="{static_data_dir}/region/gages_nwm4_calib_all.csv",
        default=None,
    )

    calval_stats_file: Path | str = Field(
        description=(
            "Path to CSV or parquet file with calibration/validation statistics for all calibration gages "
            "and formulations, e.g., 'stat_calval_all_conus.parquet', 'stat_calval_all_conus.csv'. "
            "Must include columns for 'gage_id', 'formulation', and relevant metrics to be used for formulation "
            "and parameter regionalization."
        ),
        examples="{static_data_dir}/region/calval_stats/stat_calval_all_{domain}.parquet",
        default=None,
    )

    calib_param_file: Path | str = Field(
        description=(
            "Path to CSV or parquet file containing calibrated parameters for all calibration gages "
            "and formulations in the domain. Must include columns for 'gage_id', 'formulation', and "
            "calibrated parameters."
        ),
        examples="{static_data_dir}/region/pseudo_calib_params/sampled_params_{domain}.csv",
        default=None,
    )

    approach_calib_basins: Literal["regionalization", "summary_score"] = Field(
        description=(
            "Strategy for assigning formulations to calibrated basins. Valid options are 'regionalization' "
            "(assign the formulation chosen for the region) or 'summary_score' (assign based on formulation "
            "summary scores for the calibrated basin)."
        ),
        examples="summary_score",
        default="summary_score",
    )

    id_col: FieldCrosswalk = Field(
        description="Dictionary mapping column names for unique identifiers in all applicable files.",
        examples={
            "divide": "div_id",
            "gage": "gage_id",
            "huc12": "huc_12",
            "vpu": "vpu_id",
            "drainage_area": "area_sqkm",
        },
        default_factory=FieldCrosswalk,
    )

    layer_name: LayerCrosswalk = Field(
        description=(
            "Dictionary mapping layer names for hydrofabric files. "
            "Identifies the layer in each hydrofabric file to be used during regionalization."
        ),
        examples={
            "huc12": "WBDSnapshot_National",
            "ngen": "divides",
        },
        default_factory=LayerCrosswalk,
    )

    logging: LoggingConfig = Field(
        description="Logging configuration for the application.",
        examples={
            "level": "info",
            "log_to_file": True,
            "file": "logs/{run_name}.log",
        },
        default_factory=LoggingConfig,
    )

    @model_validator(mode="after")
    def normalize_hydrofabric_file(self) -> "BaseGeneralConfig":
        """Normalize the hydrofabric file path to a dictionary mapping VPU to file paths."""
        if isinstance(self.ngen_hydrofabric_file, (str, Path)):
            # If it's a single path, create a dictionary with the current VPU
            self.ngen_hydrofabric_file = {self.vpu: str(self.ngen_hydrofabric_file)}
        elif isinstance(self.ngen_hydrofabric_file, dict):
            # If it's a dict, ensure all keys are strings and values are strings
            self.ngen_hydrofabric_file = {
                str(k): str(v) for k, v in self.ngen_hydrofabric_file.items()
            }
        else:
            raise ValueError(
                "ngen_hydrofabric_file must be a string, Path, or dictionary mapping VPU to file paths."
            )
        return self

    @model_validator(mode="after")
    def lower_case_ids(self) -> "BaseGeneralConfig":
        """Ensure that all ID columns are in lower case."""
        if self.id_col:
            self.id_col = self.id_col.lower_case()

        if self.layer_name:
            self.layer_name = self.layer_name.lower_case()
        return self

    @model_validator(mode="after")
    def check_vpu(self) -> "BaseGeneralConfig":
        """Ensure that the VPU is valid."""
        # fmt: off
        valid_vpus = {
            "conus": [
                "01", "02", "03N", "03S", "03W", "04", "05", "06", "07", "08", "09",
                "10L", "10U", "11", "12", "13", "14", "15", "16", "17", "18",
            ],
            "ak": ["19"],
            "hi": ["20"],
            "prvi": ["21"],
        }
        # fmt: on

        if self.vpu not in valid_vpus[self.domain]:
            msg = f"Invalid VPU '{self.vpu}' for domain '{self.domain}'. Valid options are: {valid_vpus[self.domain]}"
            logger.error(msg)
            raise ValueError(msg)

        return self


class BaseOutputConfig(BaseModel):
    """Base Output Manager."""

    save: bool = Field(
        description="Whether to save output files",
        default=True,
        examples=True,
    )
    path: Path | str = Field(
        description="Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.",
        examples=None,
        default=None,
    )
    stem: Optional[str | Dict[str, str]] = Field(
        description="File stem for output files, used to create unique file names based on the path.",
        default=None,
        examples=None,
    )
    stem_suffix: Optional[str] = Field(
        description="Suffix for the file stem, used to create unique file names based on the path for specific needs.",
        default=None,
        examples=None,
    )
    format: Optional[str] = Field(
        description="File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.",
        default=None,
        examples=None,
    )
    plots: Optional[Dict[str, Any]] = Field(
        description="Configuration for output plots, if applicable.",
        default=None,
        examples=None,
    )
    plot_path: Optional[str] = Field(
        description=(
            "Path to save output plots, if applicable. If not specified, plots will be saved "
            "in a subfolder 'plots' in the defined output path."
        ),
        default=None,
        examples=None,
    )

    @model_validator(mode="after")
    def check_plot_path(cls, values):
        """Check if plot path is valid."""
        if not values.plot_path:
            values.plot_path = f"{values.path}/plots"
            logger.debug(f"Plot path not specified, using default: {values.plot_path}")

        return values

    @model_validator(mode="after")
    def check_plot_config(cls, values):
        """Check if plot configuration is valid."""
        if values.plots is not None:
            if not isinstance(values.plots, dict):
                msg = f"'plots' must be a dictionary, got {type(values.plots)}"
                logger.error(msg)
                raise ValueError(msg)
            # only "histogram" and "spatial_map" are supported, currently
            check_options(
                list(values.plots.keys()),
                ["histogram", "spatial_map", "columns_to_plot"],
                "plot keys",
            )

        return values

    def get_file_path(
        self,
        vpu: str = None,
        algorithm: str = None,
        plot_type: str = None,
        use_stem_suffix: bool = False,
    ) -> Path:
        """Get the file path for saving the output."""
        file_path = Path(self.path) if plot_type is None else Path(self.plot_path)

        # If the path is a directory, construct the file name using 'stem' and 'format'
        if not file_path.suffix:
            if not self.stem or not self.format:
                msg = f"File 'stem' and 'format' must be specified if 'path' is a directory: {file_path}"
                logger.error(msg)
                raise ValueError(msg)

            if isinstance(self.stem, dict):
                # if stem is a dict (for different algorithms or vpus), find the stem for current algorithm and/or vpu
                if vpu and not algorithm:
                    file_stem = self.stem.get(f"{vpu}")
                elif vpu and algorithm:
                    file_stem = self.stem.get(f"{vpu}_{algorithm}")
                elif algorithm and not vpu:
                    file_stem = self.stem.get(f"{algorithm}")
                else:
                    file_stem = next(iter(self.stem.values()))
            elif isinstance(self.stem, str):
                file_stem = self.stem
            else:
                msg = f"Invalid 'stem' type: {type(self.stem)}. Must be str or dict."
                logger.error(msg)
                raise ValueError(msg)

            if not file_stem:
                msg = f"File stem not found for VPU {vpu}: {self.stem}"
                logger.error(msg)
                raise ValueError(msg)

            if use_stem_suffix:
                if not self.stem_suffix:
                    msg = f"File stem suffix not specified: {self.stem_suffix}"
                    logger.error(msg)
                    raise ValueError(msg)
                else:
                    file_stem += self.stem_suffix

            # make sure plot_type is supported
            if plot_type not in [None, "map", "hist"]:
                msg = f"Unsupported plot type: {plot_type}. Supported types are None, 'map', 'hist'."
                logger.error(msg)
                raise ValueError(msg)

            file_format = self.format if plot_type is None else "png"
            file_prefix = "" if plot_type is None else f"{plot_type}_"

            # Construct the full file path
            file_path = file_path / f"{file_prefix}{file_stem}.{file_format}"

        # create the directory if it does not exist
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)

        return file_path

    def save_to_file(
        self,
        data: Any,
        vpu: str = None,
        algorithm: str = None,
        data_str: str = None,
        use_stem_suffix: bool = False,
    ) -> None:
        """Save output data to the specified path and format.

        Args:
            data: Data to save, can be a DataFrame or Pydantic model.
            vpu: VPU identifier for the output file name.
            algorithm: Algorithm identifier for the output file name.
            data_str: String representation of the data being saved.
            use_stem_suffix: Whether to use the stem suffix for the file name.

        Raises:
            ValueError: If the output path is a directory and no file name is provided.

        """
        if not self.save:
            return

        # get the file path to save the output
        filepath = self.get_file_path(
            vpu, algorithm=algorithm, use_stem_suffix=use_stem_suffix
        )

        # save the output data
        save_data(data, filepath)
        if data_str is None:
            logger.info(f"Saved output to {filepath}")
        else:
            logger.info(f"Saved {data_str} output to {filepath}")

    def read_from_file(
        self,
        vpu: str = None,
        algorithm: str = None,
        use_stem_suffix: bool = False,
        data_str: str = None,
        data_type: dict[str, Any] = None,
    ) -> pd.DataFrame | gpd.GeoDataFrame:
        """Read output data from the specified path and format.

        Args:
            vpu: VPU identifier for the output file name.
            algorithm: Algorithm identifier for the output file name.
            use_stem_suffix: Whether to use the stem suffix for the file name.
            data_str: String representation of the data being read.
            data_type: Optional dictionary specifying the data types for specific columns.

        Returns:
            DataFrame or GeoDataFrame containing the loaded data.

        Raises:
            FileNotFoundError: If the file does not exist.

        """
        # get the file path to read the output
        filepath = self.get_file_path(
            vpu, algorithm=algorithm, use_stem_suffix=use_stem_suffix
        )

        # read the output data
        data = read_table(filepath, dtype=data_type)

        if data_str is None:
            logger.info(f"Read output from {filepath}")
        else:
            logger.info(f"Read {data_str} output from {filepath}")

        return data

    def get_valid_columns(
        self, data: pd.DataFrame | gpd.GeoDataFrame, columns: List[str]
    ) -> List[str]:
        """Get the list of valid columns that exist and are not entirely NaN in the data for plotting.

        Args:
            data: DataFrame or GeoDataFrame containing the data to plot.
            columns: List of columns specified for plotting.
        Returns:
            List of valid columns that exist in the data for plotting.
        """
        cols_exist = [col for col in columns if col in data.columns]
        cols_missing = set(columns) - set(cols_exist)
        if cols_missing:
            logger.warning(f"Excluding missing columns: {cols_missing} from plotting.")

        cols_non_nan = [col for col in cols_exist if not data[col].isna().all()]
        cols_all_nan = set(cols_exist) - set(cols_non_nan)
        if cols_all_nan:
            logger.warning(
                f"Excluding columns with all NaN values: {cols_all_nan} from plotting."
            )

        return cols_non_nan

    def plot_data(
        self,
        data: pd.DataFrame | gpd.GeoDataFrame,
        plot_dict: Dict[str, Any],
    ) -> None:
        """Plot the data and save png to the specified path.

        Args:
            data: DataFrame or GeoDataFrame containing the data to plot.
            plot_dict: Dictionary containing plot configuration, including:
                var_str: String representation of the variable being plotted.
                columns: list of columns in the data to plot.
                vpu: VPU identifier for the output file name.
                plot_type: Type of plot being saved (e.g., 'map', 'hist').

        """
        # if columns_to_plot is specified by the user, use it
        if self.plots and self.plots.get("columns_to_plot", None) is not None:
            plot_dict["columns"] = self.plots["columns_to_plot"]

        plot_dict["columns"] = self.get_valid_columns(
            data, plot_dict.get("columns", [])
        )
        if not plot_dict["columns"]:
            logger.warning(
                "No valid columns to plot after validation. Skipping plotting."
            )
            return

        # replace "noah-owp-modular" in formulation column to "NOM" for better readability in plots
        if "formulation" in plot_dict["columns"]:
            data["formulation"] = data["formulation"].str.replace(
                "noah-owp-modular", "NOM", regex=False
            )

        # additionally replace "noah-owp-modular" in column names (required for plotting) to "NOM"
        plot_dict["columns"] = [
            c1.replace("noah-owp-modular", "NOM") if isinstance(c1, str) else c1
            for c1 in plot_dict["columns"]
        ]

        # correspondingly replace "noah-owp-modular" in data.columns to "NOM"
        data.columns = [
            c1.replace("noah-owp-modular", "NOM") if isinstance(c1, str) else c1
            for c1 in data.columns
        ]

        vpu_dict = plot_dict.get("vpu", None)
        vpu_file = None
        if (
            self.stem
            and isinstance(self.stem, dict)
            and vpu_dict
            and vpu_dict in self.stem
        ):
            vpu_file = vpu_dict

        if self.plots and self.plots.get("histogram", False):
            path1 = self.get_file_path(
                vpu_file,
                algorithm=plot_dict.get("algorithm"),
                plot_type="hist",
            )
            plot_dict1 = plot_dict.copy()
            plot_dict1["outfile"] = path1

            # remove non-numeric columns from data from histogram plotting
            numeric_columns = data.select_dtypes(include=["number"]).columns.tolist()
            plot_dict1["columns"] = [
                col for col in plot_dict1.get("columns", []) if col in numeric_columns
            ]

            plot_histogram(data, plot_dict1)

        if self.plots and self.plots.get("spatial_map", False):
            path2 = self.get_file_path(
                vpu_file,
                algorithm=plot_dict.get("algorithm"),
                plot_type="map",
            )
            plot_dict2 = plot_dict.copy()
            plot_dict2["outfile"] = path2
            plot_spatial_map(data, plot_dict2)


class BaseConfig(BaseModel):
    """Base configuration for the application."""

    general: BaseGeneralConfig
    """Base general settings for the regionalization application."""

    output: dict[str, BaseOutputConfig]
    """Base output settings for the regionalization application."""


class BaseConfigProcessor:
    """Base configuration processor."""

    def __init__(
        self,
        config_file: str | Path | list[str] | list[Path],
        config_schema: BaseModel = Field(...),
        sample_size: int = None,
    ):
        """Initialize regionalization processor."""
        if isinstance(config_file, (str, Path)):
            self.config_file = [config_file]
        else:
            self.config_file = config_file
        self.config_schema = config_schema
        self.config = self.load_and_process_config
        self.sample_size = sample_size
        self._expand_user_file_paths(self.config)

        self.validate_files()

    def _deep_merge_configs(self, a: dict, b: dict) -> dict:
        """Recursively merge two configuration dictionaries, with values from `b` overwriting those in `a`.

        Args:
            a: The base dictionary.
            b: The dictionary whose values will overwrite those in `a`.

        Returns:
            A new dictionary that is the result of merging `a` and `b`.

        """
        result = a.copy()
        for key, value in b.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def _load_and_validate_config(
        self, config_paths: list[str], config_schema: BaseModel = Field(...)
    ) -> BaseModel:
        """Load a YAML file, validate its structure using Pydantic, and substitute placeholders in the config.

        Args:
            config_paths: list of paths to the config files
            config_schema: Pydantic model to validate the config structure

        Returns:
            Config object with validated structure

        """
        try:
            configs = []
            for p in config_paths:
                with open(p, "r") as f:
                    configs.append(yaml.safe_load(f))
            merged_config = reduce(self._deep_merge_configs, configs)
            config = config_schema(**merged_config)

            return config

        except ValidationError as e:
            logger.exception(f"Validation Error: {e}")
            raise
        except Exception as e:
            logger.exception(f"Error loading YAML file: {e}")
            raise

    def _recursive_substitute_until_fixed(self, config, context, max_iter=5):
        for _ in range(max_iter):
            new_config = recursive_substitute(config, context)
            if new_config == config:
                break
            config = new_config
        return config

    def _substitute_placeholders(self, config: BaseModel) -> BaseModel:
        """Substitute placeholders in the config with actual values.

        Args:
            config: Config object with placeholders

        Returns:
            Config object with placeholders substituted

        """
        # Create a context dictionary with general config parameters
        context = {
            "domain": config.general.domain
            if hasattr(config.general, "domain")
            else None,
            "run_name": config.general.run_name
            if hasattr(config.general, "run_name")
            else None,
            "static_data_dir": config.general.static_data_dir
            if hasattr(config.general, "static_data_dir")
            else None,
            "base_dir": config.general.base_dir
            if hasattr(config.general, "base_dir")
            else None,
            "vpu": config.general.vpu if hasattr(config.general, "vpu") else None,
            "algorithm_list": config.general.algorithm_list
            if hasattr(config.general, "algorithm_list")
            else None,
        }

        # remove items with None values from context
        context = {k: v for k, v in context.items() if v is not None}

        # substitute placeholders in the config
        config = self._recursive_substitute_until_fixed(config, context)

        return config

    def _expand_user(self, val: str | Path) -> Path:
        """Expand user home directory and environment variables in a file path."""
        s = str(val)

        user = os.environ.get("LOGNAME") or os.environ.get("USER")
        if user:
            user = user.split("@", 1)[0]
            s = re.sub(r"\$USER\b", user, s)

        s = os.path.expandvars(s)
        s = os.path.expanduser(s)

        return str(s)

    def _expand_user_file_paths(self, obj) -> None:
        if isinstance(obj, BaseModel):
            for name in obj.__class__.model_fields:
                val = getattr(obj, name)
                new_val = self._expand_user_file_paths(val)
                if new_val is not val:
                    setattr(obj, name, new_val)

        elif isinstance(obj, dict):
            for k, v in obj.items():
                new_v = self._expand_user_file_paths(v)
                if new_v is not v:
                    obj[k] = new_v

        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_v = self._expand_user_file_paths(v)
                if new_v is not v:
                    obj[i] = new_v

        elif isinstance(obj, tuple):
            return tuple(self._expand_user_file_paths(v) for v in obj)

        elif isinstance(obj, (str, Path)):
            s = str(obj)
            if any(x in s for x in ("~", "$")):
                return self._expand_user(s)

        return obj

    def _required_columns_calval_stats(self, config) -> set[str]:
        """Return a set of required columns for calibration/validation statistics."""
        required_fields = {self.gage_col, "formulation"}

        # required fields for summary score configuration (for formulation regionalization)
        sc = getattr(config, "summary_score", None)
        if sc:
            mp = getattr(sc, "metric_eval_period", None)
            eval_col = getattr(mp, "col_name", None) if mp else None
            if eval_col:
                required_fields.add(eval_col)

            metrics = getattr(sc, "metrics", None)
            if isinstance(metrics, dict):
                required_fields.update(metrics)

        # required fields for parameter regionalization
        donor = getattr(config, "donor", None)
        if donor:
            eval_pd = getattr(donor, "metric_eval_period", None)
            if eval_pd:
                eval_col = getattr(eval_pd, "col_name", None)
                if eval_col:
                    required_fields.add(eval_col)
            metrics = getattr(donor, "metric_threshold", None)
            if isinstance(metrics, dict):
                required_fields.update(metrics)

        return required_fields

    def _file_required_column_map(self, config) -> Dict[str, str]:
        """Return a dictionary mapping files to required columns."""
        file_dict = {
            "gage_divide_cwt_file": {self.div_col, self.gage_col},
            "donor_gage_file": {self.gage_col, "longitude", "latitude"},
            "calval_stats_file": self._required_columns_calval_stats(config),
            "calib_param_file": {self.gage_col, "formulation"},
            "ngen_hydrofabric_file": {
                self.div_col,
                self.vpu_col,
                "geometry",
            },
            "huc12_hydrofabric_file": {self.huc12_col, "geometry"},
            "divide_huc12_cwt_file": {self.div_col, self.huc12_col},
            "formulation_file": {self.div_col, "formulation"},
        }

        # add snow cover file if it exists in the config
        from nwm_region_mgr.parreg import config_schema as pcs

        if isinstance(config, pcs.Config) and hasattr(config, "snow_cover"):
            if config.snow_cover.consider_snowness:
                snow_cover_file = getattr(config.snow_cover, "snow_cover_file", None)
                snow_frac_col = getattr(config.snow_cover, "column", None)
                if snow_cover_file and snow_frac_col:
                    file_dict["snow_cover_file"] = {self.div_col, snow_frac_col}

        return file_dict

    def _assemble_file_paths(
        self, config: BaseModel, exclude: set[str] = None, include: set[str] = None
    ) -> dict[str, Path]:
        """Assemble file paths from the configuration.

        Args:
            config: The configuration object.
            exclude: Optional set of fields to exclude from the list of paths.
            include: Optional set of fields to include in the list of paths.

        Returns:
            Dictionary mapping path names to their Path objects.

        """
        # all input file paths to be checked in the config
        path_fields = self._file_required_column_map(config)

        if exclude:
            # exclude specified fields from the list
            path_fields = [field for field in path_fields if field not in exclude]

        if include:
            # include specified fields in the list
            path_fields = [field for field in path_fields if field in include]

        # create a dictionary to hold the paths
        paths = {}
        for path1 in path_fields:
            val = getattr(config.general, path1, None) or getattr(
                getattr(config, "snow_cover", None), path1, None
            )
            if val is not None:
                if isinstance(val, (str, Path)):
                    paths[path1] = Path(val)
                elif isinstance(val, dict):
                    paths[path1] = {
                        k: Path(v).expanduser()
                        for k, v in val.items()
                        if isinstance(v, (str, Path))
                    }
                else:
                    logger.warning(f"Unsupported type for {path1}: {type(val)}")

        # Remove any None values and return the paths dictionary
        return {k: v for k, v in paths.items() if v is not None}

    def _validate_paths(
        self, paths: str | Path | list[str | Path] | dict[str, str | Path]
    ) -> None:
        """Validate that all file and directory paths exist.

        Args:
            paths: A string, Path, list, or dict of strings/Paths to validate.

        Raises:
            FileNotFoundError: If any path does not exist.

        """
        if isinstance(paths, (str, Path)):
            paths = [paths]
        elif isinstance(paths, dict):
            paths = list(flatten_dict(paths).values())

        missing_paths = [p for p in paths if not Path(p).exists()]
        if missing_paths:
            msg = f"Missing paths: {missing_paths}"
            logger.error(msg)
            raise FileNotFoundError(msg)

    def _check_file_columns(
        self,
        config: BaseModel,
        dict_path: Dict[str, str | Path | dict[str, str | Path]] = None,
    ) -> None:
        """Check if the required columns are present in the files in the configuration.

        Args:
            config: The configuration object to check.
            dict_path: Optional dictionary of file paths to check.

        Raises:
            ValueError: If any required columns are missing in the files.

        """
        if dict_path is None:
            msg = "No file paths provided for checking columns."
            logger.error(msg)
            raise ValueError(msg)

        dict_cols = self._file_required_column_map(config)
        logger.debug("Required columns for files: %s", dict_cols)

        # loop through the required files and check their columns
        for file_key, file_path in dict_path.items():
            if file_key not in dict_cols:
                logger.warning(
                    f"No required columns defined for {file_key}. Skipping column check."
                )
                continue

            if isinstance(file_path, (str, Path)):
                file_path = [
                    Path(file_path)
                ]  # Ensure file_path is a list of Path objects
            elif isinstance(file_path, dict):
                file_path = [Path(v) for v in file_path.values()]
            else:
                msg = f"Invalid type for file path '{file_key}': {type(file_path)}. Must be str, Path, or dict."
                logger.error(msg)
                raise ValueError(msg)

            required_columns = dict_cols[file_key]
            if not required_columns:
                logger.warning(
                    f"No required columns defined for {file_key}. Skipping column check."
                )
                continue

            for file in file_path:
                if "geometry" in required_columns:
                    layer = (
                        getattr(config.general.layer_name, "ngen", None)
                        if "ngen" in file_key
                        else getattr(config.general.layer_name, "huc12", None)
                    )
                    check_columns_hydrofabric(
                        file, required_columns, layer_name=layer, case_sensitive=False
                    )
                else:
                    check_columns_dataframe(file, required_columns, case_sensitive=True)

    @property
    @lru_cache
    def load_and_process_config(self) -> BaseModel:
        """Load, validate, and process the configuration files.

        Returns:
            Config object with validated structure and substituted placeholders.

        """
        # Load and validate the configuration
        config = self._load_and_validate_config(self.config_file, self.config_schema)

        # Substitute placeholders in the configuration
        config = self._substitute_placeholders(config)

        return config

    def validate_files(self):
        """Validate that all file paths exist and required columns are present in the files."""
        # Assemble file paths from the configuration
        paths = self._assemble_file_paths(self.config, exclude={"formulation_file"})
        logger.debug("Input file paths from configuration: %s", paths)

        # Validate that all file paths exist
        self._validate_paths(paths)

        # Check if the required columns are present in the files
        self._check_file_columns(self.config, paths)

        logger.info("Successfully validated and processed the configurations.")

        # Save the final configuration
        cc = getattr(self.config.output, "config_final", None)
        if cc is not None:
            cc.save_to_file(self.config, data_str="Final Configuration")

    def set_vpu(self, vpu: str):
        """Set the vpu."""
        self.vpu = vpu
        if hasattr(self, "vpu_gdf"):
            delattr(self, "vpu_gdf")

    def set_vpu_gdf(self) -> gpd.GeoDataFrame:
        """Set the GeoDataFrame for the current vpu."""
        layer_name = getattr(self.config.general.layer_name, "ngen", "divides")
        gdf = gpd.read_file(
            Path(self.config.general.ngen_hydrofabric_file[self.vpu]),
            layer=layer_name,
        )
        gdf = gdf[[self.div_col.lower(), "geometry"]]

        # ensure div_col is always string
        gdf[self.div_col] = gdf[self.div_col].astype("string")

        self.vpu_gdf = gdf.copy()

    def get_vpu_gdf(self) -> gpd.GeoDataFrame:
        """Get the GeoDataFrame for the current vpu."""
        if not hasattr(self, "vpu_gdf"):
            self.set_vpu_gdf()
        return self.vpu_gdf

    @contextmanager
    def timing_block(self, step_str: str):
        """Context manager for timing code execution.

        Args:
            step_str: Description of the step being timed.

        """
        start = time()
        yield
        end = time()
        logger.info(f"  Execution time for {step_str}: {end - start} seconds")

    @property
    def div_col(self):
        """Id_name for divide from the config."""
        return getattr(self.config.general.id_col, "divide", "div_id")

    @property
    def gage_col(self):
        """Id_name for gage from the config."""
        return getattr(self.config.general.id_col, "gage", "gage_id")

    @property
    def drainage_area_name(self):
        """Id_name for drainage_area from the config."""
        return getattr(self.config.general.id_col, "drainage_area", "area_sqkm")

    @property
    def huc12_col(self):
        """Id_name for huc12 from the config."""
        return getattr(self.config.general.id_col, "huc12", "huc_12")

    @property
    def vpu_col(self):
        """Id_name for vpu from the config."""
        return getattr(self.config.general.id_col, "vpu", "vpu_id")

    @property
    def donor_col(self):
        """Id_name for donor gage from the config."""
        return getattr(self.config.general.id_col, "donor", "donor")

    @property
    def gage_crosswalk_file(self):
        """Get the gage crosswalk file path from the configuration."""
        return self.config.general.gage_divide_cwt_file

    @property
    def gage_crosswalk(self):
        """Get the gage crosswalk DataFrame."""
        return read_table(self.gage_crosswalk_file, dtype={self.gage_col: str})

    @property
    def donor_gage_file(self):
        """Get the donor gage file path from the configuration."""
        return self.config.general.donor_gage_file

    @property
    def donor_gages(self):
        """Get the donor gage DataFrame."""
        return read_table(self.donor_gage_file, dtype={self.gage_col: str})

    def expand_config_for_vpu(self, vpu: str):
        """Expand the config to include VPUs (e.g., needed for all donors).

        Some donors may come from nearby VPUs, so we need to make sure that the
        configuration includes all donor VPUs.

        For example, if the current VPU '03S' uses donor gages from '03W','03N', and '06', then
        this function will expand the config to include those VPUs as well for the ngen_hydrofabric_file
        and output files.

        --- Before expansion---
        ngen_hydrofabric_file:
            '03S': '/path/to/ngen_hydro_03S.gpkg'

        --- After expansion---
        ngen_hydrofabric_file:
            '03S': '/path/to/ngen_hydro_03S.gpkg'
            '03W': '/path/to/ngen_hydro_03W.gpkg'
            '03N': '/path/to/ngen_hydro_03N.gpkg'
            '06':  '/path/to/ngen_hydro_06.gpkg'

        """

        def add_entry_if_missing(d: dict, vpu_key: str) -> dict:
            if vpu_key not in d:
                first_key = next(iter(d))
                d[vpu_key] = d[first_key].replace(first_key, vpu_key)

        add_entry_if_missing(self.config.general.ngen_hydrofabric_file, vpu)

        # expand the output configuration for summary_score and formulation because the results from neighboring VPUs
        # may be needed for the current VPU
        co = getattr(self.config.output, "summary_score", None)
        if co is not None:
            if not isinstance(co.stem, dict):
                co.stem = {self.config.general.vpu: co.stem}
            add_entry_if_missing(co.stem, vpu)

        co = getattr(self.config.output, "formulation", None)
        if co is not None:
            if not isinstance(co.stem, dict):
                co.stem = {self.config.general.vpu: co.stem}
            add_entry_if_missing(co.stem, vpu)

        # save the expanded configuration
        if hasattr(self.config.output, "config_final"):
            getattr(self.config.output, "config_final").save_to_file(
                self.config, data_str="final configuration"
            )

    def get_output_file_path(
        self,
        output_section: str,
        vpu: str = None,
        algorithm: str = None,
        use_stem_suffix: bool = False,
    ):
        """Get the output file name from the output configuration."""
        output_config = getattr(self.config.output, output_section, None)
        if output_config is None:
            msg = f"Output section '{output_section}' not found in configuration for {self.__class__.__name__}."
            logger.error(msg)
            raise ValueError(msg)

        return output_config.get_file_path(
            vpu, algorithm=algorithm, use_stem_suffix=use_stem_suffix
        )
