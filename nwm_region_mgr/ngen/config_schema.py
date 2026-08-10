"""Configuration schema for the NGEN simulation application.

config_schema.py defines the Pydantic models that represent the configuration

Classes:
    - Config: Top-level configuration for NGEN simulation.

"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Literal

from pydantic import BaseModel, Field, field_validator

from nwm_region_mgr.utils import (
    BaseConfig,
    BaseGeneralConfig,
    BaseOutputConfig,
)

logger = logging.getLogger(__name__)

TIMESTAMP_FMT = "%Y-%m-%dT%H:%M:%S"
TIMESTAMP_FMT1 = "%Y-%m-%d %H:%M:%S"


def validate_timestamp(value: str) -> str:
    """Validate that the given string is in the correct timestamp format."""
    try:
        datetime.strptime(value, TIMESTAMP_FMT)
    except ValueError:
        raise ValueError(
            f"Invalid timestamp '{value}'. Expected format {TIMESTAMP_FMT}"
        )
    return value


class NgenGeneralSettings(BaseGeneralConfig):
    """General settings for the NGEN simulation application."""

    start_time: str | Path = Field(
        description="Start time for the NGEN simulation in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).",
        examples="2022-10-01T00:00:00",
        default="2022-10-01T00:00:00",
    )
    end_time: str | Path = Field(
        description="End time for the NGEN simulation in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).",
        examples="2022-10-01T10:00:00",
        default="2022-10-02T00:00:00",
    )

    algorithm_list: List[
        Literal["gower", "urf", "kmeans", "kmedoids", "hdbscan", "birch", "proximity"]
    ] = Field(
        description="Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch', 'proximity').",
        examples=["gower", "kmeans"],
        default=["gower"],
    )

    par_file: Path | str | Dict[str, Path] | Dict[str, str] = Field(
        description="Path to the formulation parameters file for NGEN simulation.",
        examples="outputs/region/{run_name}/params/formulation_params_{algorithm_list}_conus_vpu{vpu_list}.csv",
    )
    pair_file: Path | str | Dict[str, Path] | Dict[str, str] = Field(
        description="Path to the pairing file for NGEN simulation.",
        examples="outputs/region/{run_name}/pairs/pairs_{algorithm_list}_conus_vpu{vpu_list}_mswm.csv",
    )

    config_template: Path | str = Field(
        description="Path to the MSWM configuration template file.",
        examples="ngen/mswm.config.template.docker",
    )

    # validate timestamp fields
    _validate_start = field_validator("start_time")(validate_timestamp)
    _validate_end = field_validator("end_time")(validate_timestamp)


class NgenOutputConfig(BaseModel):
    """Output configuration for formulation regionalization."""

    ngen: BaseOutputConfig = Field(
        description=(
            "Root directory for the NGEN simulation inputs and outputs, under which sub-directories "
            "'regionalization/{run_name}_{algorithm}/vpu_{vpu}/' will be created for each algorithm and VPU.",
        ),
        examples={
            "save": True,
            "path": "{base_dir}/outputs/ngen",
        },
    )

    config_final: BaseOutputConfig = Field(
        description=(
            "Output configuration for the final configuration file after processing, with placeholders resolved."
        ),
        examples={
            "save": True,
            "path": "{base_dir}/outputs/{run_name}/config_ngen_final.yaml",
        },
    )


class Config(BaseConfig):
    """Top-level configuration for formulation regionalization."""

    general: NgenGeneralSettings = Field(
        description="General settings for NGEN simulation",
        default_factory=NgenGeneralSettings,
    )

    output: NgenOutputConfig = Field(
        description="Output configuration for NGEN simulation.",
        default_factory=NgenOutputConfig,
    )
