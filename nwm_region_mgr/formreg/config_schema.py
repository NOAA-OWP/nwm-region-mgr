"""Configuration schema for the formulation regionalization application."""

import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Union

from pydantic import BaseModel, Field, model_validator

from nwm_region_mgr.utils import (
    BaseConfig,
    BaseGeneralConfig,
    check_options,
)

logger = logging.getLogger(__name__)


class FormulationGeneralSettings(BaseGeneralConfig):
    """General settings for the formulation regionalization application."""

    huc12_hydrofabric_file: Union[str, Path] | None = Field(
        description="Path to HUC12 hydrofabric file containing HUC12 polygons for spatial discretization.",
        examples="NationalWBDSnapshot.gdb",
        default=None,
    )

    divide_huc12_cwt_file: str | None = Field(
        description="Path to crosswalk file between HUC12 basins and NextGen catchments, with columns 'divide_id' and 'huc_12'.",
        examples="cwt_divide_huc12_{domain}.csv",
        default=None,
    )

    calib_basins_only: bool = Field(
        description="Whether to run formulation selection only for calibrated basins (based on summary score).",
        examples=False,
        default=False,
    )

    formulation_to_include: List[str] | None = Field(
        description="List of formulations to consider. If None, all formulations are included.  If 'all', all formulations are included.",
        examples=["noah-owp-modular cfe-s t-route"],
        default=None,
    )

    formulation_to_exclude: List[str] | None = Field(
        description="List of formulations to exclude. If None, no formulations are excluded.",
        examples=["noah-owp-modular cfe-s t-route"],
        default=None,
    )

    consider_cost: bool = Field(
        description="Whether to consider computational costs of formulations in the regionalization process.",
        examples=False,
        default=False,
    )

    @model_validator(mode="after")
    def check_approach_calib_basins(self) -> "FormulationGeneralSettings":
        """Ensure that the approach for assigning formulation to calibrated basins is valid."""
        valid_approaches = ["regionalization", "summary_score"]
        check_options(
            self.approach_calib_basins, valid_approaches, "approach_calib_basins"
        )

        return self


class BestFormulation(BaseModel):
    """Configuration for determining the best formulation for each spatial unit."""

    method: Literal["total_score", "total_count"] = Field(
        description="Method to determine the best formulation, options: 'total_score', 'total_count'.",
        examples="total_score",
    )

    type: Literal["basin", "divide"] = Field(
        description="Type of spatial unit for best formulation, options: 'basin', 'divide'.",
        examples="basin",
    )

    tolerance: float = Field(
        description="Score tolerance as a fraction of the best score, must be between 0.0 and 1.0.",
        examples=0.05,
        default=0.05,
        ge=0.0,
        le=1.0,
    )


class FormulationSpatialUnitConfig(BaseModel):
    """Spatial discretization settings for formulation regionalization."""

    huc_level: Literal["huc-2", "huc-4", "huc-6", "huc-8", "huc-10", "huc-12"] = Field(
        description="USGS HUC level used for discretization, e.g., 'huc-8'.",
        examples="huc-12",
        default="huc-8",
    )

    nmin_calib_basin: int = Field(
        description="Minimum number of calibration basins required per spatial unit to consider it valid.",
        examples=5,
        default=5,
    )

    basin_fill_method: Literal["upscaling", "nearest-neighbor"] = Field(
        description="Method to handle units with too few calibration basins. Options: 'upscaling', 'nearest-neighbor'.",
        examples="upscaling",
        default="upscaling",
    )

    best_formulation: BestFormulation = Field(
        description="Strategy to determine the best formulation for each spatial unit.",
        examples={"method": "total_score", "type": "divide", "tolerance": 0.05},
        default_factory=BestFormulation,
    )


class Orientation(str, Enum):
    """Orientation for metrics: 'positive' means higher is better, 'negative' means lower is better."""

    positive = "positive"
    negative = "negative"


class MetricConfig(BaseModel):
    """Configuration for an individual metric used in summary scoring."""

    upper: float | None = Field(
        description="Upper bound for scaling and normalization, must be greater than lower bound.",
        examples=1,
        default=None,
    )

    lower: float | None = Field(
        description="Lower bound for scaling and normalization, must be less than upper bound.",
        examples=0,
        default=None,
    )

    orientation: Literal["positive", "negative"] = Field(
        description="Orientation of the metric, either 'positive' or 'negative'.",
        examples=0,
        default="positive",
    )

    weight: float = Field(
        description="Weight of the metric in the summary score, must be between 0.0 and 1.0.",
        examples=0.25,
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    absolute: bool = Field(
        description="Whether to use the absolute value of the metric for normalization.",
        examples=False,
        default=False,
    )


class MetricEvalPeriod(BaseModel):
    """Configuration for the evaluation period of metrics to be used for screening donors."""

    col_name: str = Field(
        description="Name of the column in the donor stats file that contains the evaluation period.",
        examples="evalPeriod",
    )

    value: str = Field(
        description="Value of the evaluation period to filter the donor stats file.",
        examples="valid",
    )


class FormulationSummaryScoreConfig(BaseModel):
    """Configuration for computing a summary score for formulation as a weighted average of normalized metrics."""

    metric_eval_period: MetricEvalPeriod | None = Field(
        description="Evaluation period of metrics to be used for screening donors.",
        examples={"col_name": "evalPeriod", "value": "valid"},
        default=None,
    )

    metrics: Dict[str, MetricConfig] = Field(
        description="Dictionary of metrics used in the summary score, keyed by metric name.",
        examples={
            "cor": {
                "upper": 1,
                "lower": -0.5,
                "orientation": "positive",
                "weight": 0.25,
            }
        },
    )

    @model_validator(mode="after")
    def remove_zero_weighted_metrics(self) -> "FormulationSummaryScoreConfig":
        """Remove metrics with a weight of 0.0 from the configuration.

        Returns:
            A new FormulationSummaryScoreConfig instance with zero-weighted metrics removed.

        """
        active_metrics = {
            name: metric for name, metric in self.metrics.items() if metric.weight > 0.0
        }
        missing_metrics = set(self.metrics) - set(active_metrics)
        if missing_metrics:
            logger.debug(
                f"Removed metrics with zero weight: {', '.join(missing_metrics)}. "
                "These metrics will not contribute to the summary score."
            )

        self.metrics = active_metrics

        return self

    @model_validator(mode="after")
    def validate_all_metrics(self) -> "FormulationSummaryScoreConfig":
        """Ensure that all metrics have valid bounds and weights."""
        for name, metric in self.metrics.items():
            if (
                metric.upper is not None
                and metric.lower is not None
                and metric.upper <= metric.lower
            ):
                msg = f"Invalid bounds for metric '{name}': upper={metric.upper}, lower={metric.lower}"
                logger.error(msg)
                raise ValueError(msg)

            if metric.weight is not None and (
                metric.weight < 0.0 or metric.weight > 1.0
            ):
                msg = f"Invalid weight for metric '{name}': {metric.weight}. Must be between 0.0 and 1.0."
                logger.error(msg)
                raise ValueError(msg)

        return self

    @model_validator(mode="after")
    def check_weights_sum_to_one(self) -> "FormulationSummaryScoreConfig":
        """Ensure that the sum of all metric weights equals 1.0."""
        total_weight = sum(metric.weight for metric in self.metrics.values())
        if abs(total_weight - 1.0) > 1e-6:
            msg = (
                f"The sum of all metric weights must equal 1.0, but got {total_weight}"
            )
            logger.error(msg)
            raise ValueError(msg)
        return self


class FormulationCostConfig(BaseModel):
    """Computational cost of each formulation."""

    file: str | None = Field(
        description="Path to CSV file with formulation costs. If provided, costs will be read from this file.",
        examples="formulation_costs_secs_per_catchment.csv",
        default=None,
    )

    costs: Dict[str, float] | None = Field(
        description="Dictionary of formulation costs, keyed by formulation name. If `file` is provided, this is ignored.",
        examples={"noah-owp-modular ueb cfe-x t-route": 10},
        default=None,
    )


class Config(BaseConfig):
    """Top-level configuration for formulation regionalization."""

    general: FormulationGeneralSettings = Field(
        description="General settings for the formulation regionalization application.",
        default_factory=FormulationGeneralSettings,
    )

    spatial_unit: FormulationSpatialUnitConfig = Field(
        description="Spatial discretization settings for the application.",
        default_factory=FormulationSpatialUnitConfig,
    )

    summary_score: FormulationSummaryScoreConfig = Field(
        description="Summary score computation configuration for the application.",
        default_factory=FormulationSummaryScoreConfig,
    )

    formulation_cost: FormulationCostConfig = Field(
        description="Computational cost configuration for each formulation.",
        default_factory=FormulationCostConfig,
    )
