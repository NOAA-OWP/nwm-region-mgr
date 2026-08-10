"""Compute summary scores for formulation regionalization.

This module provides functions to load, validate, and process the configuration for formulation regionalization.

Functions:
- process_config: Load and process the configuration file.
- get_formulations_from_stats: Extract formulation names from calibration and validation statistics file names.
- formulation_summary_score: Compute the summary score for each row in the DataFrame based on the configuration.
- compute_summary_score: Compute summary scores for each formulation from calibration and validation statistics.

"""

import glob
import logging
import re
from pathlib import Path
from typing import Dict

import geopandas as gpd
import numpy as np
import pandas as pd

from nwm_region_mgr.formreg import config_schema as cs
from nwm_region_mgr.utils import read_table

logger = logging.getLogger(__name__)


def get_formulations_from_stats(config: cs.Config) -> dict[str, Path]:
    """Extract formulation names from the calibration and validation statistics file names.

    Args:
        config: The configuration object.

    Returns:
        dict[str, Path]: A dictionary mapping formulation names to their statistics file paths.

    """
    # Find all statistics files (parquet or csv) for the given VPU
    dir_stats = Path(config.general.calval_stats_dir)

    # domain stats files (csv or parquet)
    stats_files = glob.glob(
        f"{dir_stats}/stat_calval_*_{config.general.domain}.parquet"
    ) + glob.glob(f"{dir_stats}/stat_calval_*_{config.general.domain}.csv")

    if not stats_files:
        msg = f"No statistics files found for {config.general.domain} in {dir_stats}. Please check the configuration."
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Extract unique formulation names from the file names
    formulations = set()
    for file in stats_files:
        match = re.search(r"stat_calval_(.*?)_", file)
        if match:
            formulations.add(match.group(1))

    # narrow down to formulation_to_include (if provided in the config)
    forms1 = config.general.formulation_to_include
    if forms1:
        formulations = {form for form in formulations if form in forms1}
        forms_missing = forms1 - formulations
        if forms_missing:
            logger.warning(
                f"Formulations {', '.join(forms_missing)} not found in statistics files. Not using them."
            )

    # exclude formulations_to_exclude (if provided in the config)
    if config.general.formulation_to_exclude:
        formulations = {
            form
            for form in formulations
            if form not in config.general.formulation_to_exclude
        }

    if not formulations:
        msg = (
            f"No valid formulations found in statistics files in {dir_stats}. "
            "Please ensure the formulation names are included in the names of the statistics files with the convention "
            "'stat_calval_<formulation>_<domain>.<extension>', e.g., 'stat_calval_nom-cfex_conus.parquet'."
        )
        logger.error(msg)
        raise ValueError(msg)

    # Convert formulations to a dictionary mapping to their statistics file paths
    dict_form = {
        form: Path(
            [file for file in stats_files if form in file][0]
        )  # Get the first matching file path
        for form in formulations
    }

    return dict_form


def formulation_summary_score(
    df: pd.DataFrame, dict_metrics: Dict[str, cs.MetricConfig]
) -> None:
    """Compute the summary score for each row in the DataFrame based on the configuration.

    Args:
        df: DataFrame containing the metrics to compute the summary score.
        dict_metrics: Dictionary containing metric configurations.

    """
    # Check if the metrics dictionary is empty
    if not dict_metrics:
        msg = "No metrics defined in the configuration for summary score computation."
        logger.warning(msg)
        return

    # weights and orientations
    weights = {name: metric.weight for name, metric in dict_metrics.items()}
    orientations = {name: metric.orientation for name, metric in dict_metrics.items()}

    # Make sure weights sum to 1
    assert abs(sum(weights.values()) - 1.0) < 1e-6

    # Select the metric columns
    metrics = list(weights.keys())
    df_metrics = df[metrics].copy()

    # remove rows with NaN values in any of the metric columns
    df_metrics.dropna(subset=metrics, inplace=True)
    if df_metrics.empty:
        logger.warning(
            "No valid data found after removing rows with NaN values in metric columns."
        )
        return

    # Normalize each column based on orientation
    for col in metrics:
        values = df_metrics[col]

        # take absolute values if specified
        if dict_metrics[col].absolute:
            values = values.abs()

        # determine min and max values for normalization
        min_val, max_val = values.min(), values.max()

        # replace min and max with lower and upper bounds if provided
        if dict_metrics[col].lower is not None:
            min_val = dict_metrics[col].lower
        if dict_metrics[col].upper is not None:
            max_val = dict_metrics[col].upper

        # rescale the values to range [min_val, max_val]
        values = values.clip(lower=min_val, upper=max_val)

        if max_val == min_val:
            # Avoid division by zero
            df_metrics[col + "_norm"] = 0.0
            logger.warning(
                f"Column '{col}' has constant value {max_val}. Normalization will result in zero for all rows."
            )
        else:
            norm = (values - min_val) / (max_val - min_val)
            if orientations[col] == "negative":
                norm = 1 - norm
            df_metrics[col + "_norm"] = norm

    # Compute weighted average based on normalized metrics
    normalized_cols = [f"{m}_norm" for m in metrics]
    weight_array = np.array([weights[m] for m in metrics])
    df["summary_score"] = df_metrics[normalized_cols].dot(weight_array)

    return df


def _compute_summary_score_all_gages(
    config: cs.Config, gage_id_col: str
) -> pd.DataFrame:
    """Compute summary scores for all gages in the domain.

    Args:
        config: The configuration object.
        gage_id_col: The gage ID column name.

    Returns:
        pd.DataFrame: DataFrame containing summary scores for all gages in the domain.

    """
    # read statistics (all gages and all formulations)
    df_stats = read_table(config.general.calval_stats_file, dtype={gage_id_col: str})

    # narrow down to the evaluation period (case-insensitive)
    ss = config.summary_score
    p1 = ss.metric_eval_period
    df_stats = df_stats[df_stats[p1.col_name].str.lower() == p1.value.lower()]

    # keep only the required columns
    required_columns = [
        gage_id_col,
        "formulation",
        ss.metric_eval_period.col_name,
    ] + list(ss.metrics.keys())
    df_stats = df_stats[required_columns]

    if not df_stats.empty:
        # compute the summary score for the formulation
        df_score = formulation_summary_score(df_stats, ss.metrics)
        df_score = df_score[[gage_id_col, "formulation", "summary_score"]].copy()

    # remove duplicated rows
    df_score = df_score.drop_duplicates(
        subset=[gage_id_col, "formulation", "summary_score"]
    )

    # remove rows with NaN summary scores
    df_score = df_score.dropna(subset=["summary_score"])

    # Save the summary score DataFrame for all gages in the domain
    cc = getattr(config.output, "summary_score", None)
    if cc is not None:
        cc.save_to_file(
            df_score,
            vpu=None,
            data_str="Summary Score (for all gages)",
            use_stem_suffix=True,
        )

    return df_score


def compute_summary_score(config: cs.Config, vpu: str) -> None:
    """Compute summary scores for each formulation from calibration and validation statistics.

    Args:
        config: The configuration object.
        vpu: The VPU identifier.

    """
    # Get the VPU ID column name
    id_cols = config.general.id_col
    gage_id_col = getattr(id_cols, "gage", "gage_id")
    divide_id_col = getattr(id_cols, "divide", "divide_id")
    vpu_id_col = getattr(id_cols, "vpu", "vpuid")

    cc = getattr(config.output, "summary_score", None)
    if cc is None:
        return

    filepath = cc.get_file_path(None, use_stem_suffix=True)

    # compute summary scores for all gages in the domain only if this is the first VPU
    if not filepath.exists():
        df_score_all = _compute_summary_score_all_gages(config, gage_id_col)
    else:
        # read the summary score DataFrame for all gages in the domain
        df_score_all = cc.read_from_file(
            vpu=None,
            use_stem_suffix=True,
            data_str="Summary Score (for all gages)",
            data_type={vpu_id_col: str, divide_id_col: str, gage_id_col: str},
        )

    # get VPU from gage_divide crosswalk file
    cwt_file = Path(config.general.gage_divide_cwt_file)
    df_cwt = read_table(
        cwt_file, dtype={gage_id_col: str, divide_id_col: str, vpu_id_col: str}
    )
    df_score_vpu = df_score_all.merge(
        df_cwt[[gage_id_col, divide_id_col, vpu_id_col]],
        on=gage_id_col,
        how="left",
    )

    # narrow down to the VPU
    df_score_vpu = df_score_vpu[df_score_vpu[vpu_id_col] == vpu].copy()

    if df_score_vpu.empty:
        msg = (
            f"No summary scores found for VPU {vpu}. Please check the statistics files."
        )
        logger.error(msg)
        raise ValueError(msg)

    # drop vpu_id_col and divide_id_col
    df_score_vpu = df_score_vpu.drop(
        columns=[vpu_id_col, divide_id_col], errors="ignore"
    )

    # remove duplicated rows
    df_score_vpu = df_score_vpu.drop_duplicates(
        subset=[gage_id_col, "formulation", "summary_score"]
    )

    # Save the summary score DataFrame for the specific VPU
    cc = getattr(config.output, "summary_score", None)
    if cc is not None:
        cc.save_to_file(
            df_score_vpu,
            vpu=vpu,
            data_str=f"Summary Score (VPU {vpu})",
            use_stem_suffix=False,
        )

    # plot the summary score
    if cc is not None and any(cc.plots.values()):
        # create wide-format DataFrame for plotting
        df_score_wide = df_score_vpu.pivot(
            index=gage_id_col, columns="formulation", values="summary_score"
        ).reset_index()
        df_score_wide.columns.name = None

        if cc.plots.get("spatial_map", False):
            # read the crosswalk file
            cwt_file = Path(config.general.gage_divide_cwt_file).resolve(strict=True)
            if not cwt_file.exists():
                logger.warning(
                    f"Crosswalk file {cwt_file} does not exist. Skipping spatial map plot."
                )
                return
            cwt_df = read_table(cwt_file, dtype={gage_id_col: str, divide_id_col: str})
            if cwt_df.empty:
                logger.warning(
                    f"Crosswalk file {cwt_file} is empty. Skipping spatial map plot."
                )
                return
            # merge with summary score DataFrame
            df_score_wide = df_score_wide.merge(
                cwt_df[[gage_id_col, divide_id_col]],
                on=gage_id_col,
                how="left",
            )
            # read the geometry file
            geo_file = Path(config.general.ngen_hydrofabric_file[vpu])
            gdf = gpd.read_file(geo_file, layer=config.general.layer_name.ngen)

            # merge geometry with summary score DataFrame
            df_score_wide = df_score_wide.merge(
                gdf[[divide_id_col, "geometry"]], on=divide_id_col, how="right"
            )
            df_score_wide = gpd.GeoDataFrame(
                df_score_wide, geometry="geometry", crs=gdf.crs
            )

        # plot the summary score
        plot_dict = {
            "vpu": vpu,
            "var_str": "Summary Score",
            "columns": df_score_vpu["formulation"].unique().tolist(),
            "ncols": 3,
        }
        cc.plot_data(df_score_wide, plot_dict)

    return df_score_all
