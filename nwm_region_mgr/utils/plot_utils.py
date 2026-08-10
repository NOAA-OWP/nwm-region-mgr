"""Utility functions for plotting spatial maps and histograms etc.

plot_utils.py

Functions:
- _plot_columns_by_dtype: Plot multiple columns of a GeoDataFrame based on their data types.
- plot_spatial_map: Generate a spatial map plot for the given data.
- plot_histogram: Generate histogram plot for the spatial or attribute distance between donors and receivers.
- plot_point_map: Plot the spatial distribution of locations as points on a base layer map.

"""

import logging
import math
from itertools import cycle, islice

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# from matplotlib.lines import Line2D
from shapely.ops import unary_union

logger = logging.getLogger(__name__)


def _plot_columns_by_dtype(
    gdf: gpd.GeoDataFrame,
    columns: list[str],
    fillna_value=None,
    num_bins: int = None,
    cmap_numeric: str = "viridis",
    cmap_categorical: str = "Set3",
    figsize=(10, 6),
    ncols: int = 3,
    antialiased: bool = False,
):
    """Plot multiple GeoDataFrame columns in subplots based on data type.

    Args:
        gdf: GeoDataFrame to plot
        columns: list of column names to plot
        fillna_value: value to fill NaNs
        num_bins: number of bins for numeric columns (optional)
        cmap_numeric: colormap for numeric values
        cmap_categorical: colormap for categorical values
        figsize: figure size
        ncols: number of columns in the subplot grid (default is 3)
        antialiased: whether to disable antialiasing for the plots

    """
    n = len(columns)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = np.array(axes).reshape(-1)  # Flatten in case of 2D grid

    # get the outer boundary of the GeoDataFrame
    combined_polygon = unary_union(gdf.geometry)
    boundary = combined_polygon.boundary

    for i, column in enumerate(columns):
        ax = axes[i]
        dtype = gdf[column].dtype

        # Copy gdf to avoid modifying original
        gdf_plot = gdf.copy()
        if fillna_value is not None:
            gdf_plot[column] = gdf_plot[column].fillna(fillna_value)

        if pd.api.types.is_numeric_dtype(dtype):
            if num_bins is not None:
                gdf_plot["__binned__"] = pd.cut(gdf_plot[column], bins=num_bins)
                gdf_plot.plot(
                    ax=ax,
                    column="__binned__",
                    cmap=cmap_numeric,
                    legend=True,
                    edgecolor="none",
                    linewidth=0,
                )
            else:
                gdf_plot.plot(
                    ax=ax,
                    column=column,
                    cmap=cmap_numeric,
                    legend=True,
                    edgecolor="none",
                    linewidth=0,
                )

        elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(
            dtype
        ):
            gdf_plot[column] = gdf_plot[column].astype("category")
            gdf_plot.plot(
                ax=ax,
                column=column,
                cmap=cmap_categorical,
                legend=True,
                edgecolor="none",
                linewidth=0,
            )
        else:
            ax.set_title(f"Unsupported dtype: {column}")
            ax.axis("off")
            continue

        # Even when edgecolor="none" and linewidth=0, antialiasing can cause matplotlib to blend edges
        # between adjacent polygons, resulting in faint grey or black lines. Disable antialiasing if needed.
        for coll in ax.collections:
            coll.set_antialiased(antialiased)

        # plot outer boundary
        gpd.GeoSeries(boundary).plot(ax=ax, color="black", linewidth=0.5)

        ax.set_title(column)
        ax.set_axis_off()

        # make sure legend is outside the plot if it exists
        legend = ax.get_legend()
        if legend is not None:
            # legend.set_bbox_to_anchor((1.05, 1))
            legend.set_bbox_to_anchor((0.5, -0.20))  # bottom center
            legend.set_loc("lower center")
            legend.set_frame_on(True)

    # Turn off any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    return fig, axes[: i + 1]  # Return only used axes


def plot_spatial_map(gdf: gpd.GeoDataFrame, d1: dict) -> None:
    """Generate a spatial map plot for the given data.

    Args:
        gdf : gpd.GeoDataFrame
            GeoDataFrame containing the data to be plotted.
        d1: dict
            Information needed for creating the plot

    """
    # check if the required column exists, allow case insensitivity
    cols_exist = [c for c in d1["columns"] if c.lower() in gdf.columns.str.lower()]
    cols_missing = set(d1["columns"]) - set(gdf.columns)
    if not cols_exist:
        logger.warning(
            f"Columns {cols_missing} not found in gdf. Cannot create spatial map plot."
        )
        return
    if cols_missing:
        logger.warning(
            f"Excluding missing columns {cols_missing} from spatial map plot."
        )

    _, ax = plt.subplots(figsize=(8, 6))

    # create spatial map
    fig, axes = _plot_columns_by_dtype(
        gdf,
        columns=cols_exist,
        fillna_value=d1.get("fillna_value", None),
        num_bins=d1.get("num_bins", None),
        cmap_numeric=d1.get("cmap_numeric", "viridis"),
        cmap_categorical=d1.get("cmap_categorical", "Set3"),
        ncols=d1.get("ncols", 3),
    )
    # gdf.plot(ax=ax, column=d1["column"], cmap="viridis", legend=True, edgecolor=None)

    d1["title"] = d1.get("title", f"Spatial Map of {d1['var_str']}: VPU {d1['vpu']}")
    if algorithm := d1.get("algorithm", None):
        d1["title"] += f" (Algorithm: {algorithm})"
    fig.suptitle(d1["title"], fontsize=16, fontweight="bold")
    plt.tight_layout(
        rect=[0, 0.03, 1, 0.95]
    )  # Adjust layout to make room for the title

    # save the figure
    if d1.get("outfile") is not None:
        plt.savefig(d1["outfile"], bbox_inches="tight")
        plt.close()
        logger.info(
            f"Spatial map of {d1['var_str']} for VPU {d1['vpu']} saved to {d1['outfile']}"
        )
    else:
        logger.warning("No output file specified for spatial map plot. Skipping save.")


def plot_histogram(data: pd.DataFrame, d1: dict) -> None:
    """Generate histogram plots for multiple columns in dataframe.

    Args:
        data : pd.DataFrame
            DataFrame containing the donor-receiver pairing results.
        d1: dict
            information needed for creating the plot, including:
            - columns: list of column names to plot
            - ncols: number of columns in the subplot grid (default is 3)
            - title: title of the plot
            - var_str: variable string for the plot
            - vpu: VPU identifier
            - algorithm: algorithm used for pairing (optional)

    """
    columns = d1.get("columns", [])
    if not columns:
        logger.warning("No valid columns specified to plot for histogram.")
        return

    # filter to numeric columns only
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_columns:
        logger.warning("No numeric columns found in the dataframe to plot histograms.")
        return

    if not set(columns).issubset(set(numeric_columns)):
        logger.warning(
            f"Some specified columns {set(columns) - set(numeric_columns)} are not numeric. "
            "Skipping these columns for histogram plots."
        )
        columns = [col for col in columns if col in numeric_columns]

    # Filter to columns that exist in data, allow case insensitivity
    valid_columns = [col for col in columns if col.lower() in data.columns.str.lower()]
    if not valid_columns:
        raise ValueError("None of the specified columns exist in the dataframe.")
    missing_columns = set(columns) - set(valid_columns)
    if missing_columns:
        logger.warning(
            f"Columns {missing_columns} not found in data. Only plotting valid columns: {valid_columns}"
        )

    n = len(valid_columns)
    ncols = d1.get("ncols", 3)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4 * nrows))
    axes = axes.flatten()  # Flatten in case of single row

    for i, col in enumerate(valid_columns):
        sns.histplot(
            data[col],
            ax=axes[i],
            kde=True,
            bins=30,
            color="lightblue",
            edgecolor="grey",
            stat="density",
        )
        sns.kdeplot(data[col], ax=axes[i], color="darkblue", linewidth=1.5)
        axes[i].set_title(f"{col}")

    # Hide any unused subplots
    for j in range(len(valid_columns), len(axes)):
        axes[j].set_visible(False)

    title = d1.get("title", f"Histograms of {d1['var_str']}: VPU {d1['vpu']}")
    if algorithm := d1.get("algorithm", None):
        title += f" (Algorithm: {algorithm})"
    fig.suptitle(title, fontsize=16, fontweight="bold")
    plt.xlabel(d1.get("xlabel", "Value"))
    plt.ylabel(d1.get("ylabel", "Density"))
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave space for main title

    # save the figure
    if d1.get("outfile") is not None:
        plt.savefig(d1["outfile"], bbox_inches="tight")
        plt.close()
        logger.info(
            f"Histogram of {d1['var_str']} for VPU {d1['vpu']} saved to {d1['outfile']}"
        )
    else:
        logger.warning("No output file specified for histogram plot. Skipping save.")


# NOT USED YET (for future use)
def plot_point_map(
    data: pd.DataFrame,
    d1: dict,
    base_layers: list[gpd.GeoDataFrame] = None,
) -> None:
    """Plot the spatial distribution of donors within a VPU and its buffer zone.

    Args:
        data : pd.DataFrame
            DataFrame containing the locations to be plotted.
        d1: dict
            Information needed for creating the plot, including:
        base_layers: list of GeoDataFrames
            Optional base layers to plot under the points (e.g., VPU boundaries, buffer zones).

    """
    if data.empty:
        logger.warning("No data provided for point map. Skipping plot.")
        return

    # visualize the donors selected
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot base layers
    colors_base = ["lightgray", "lightpink", "lightgreen", "lightblue"]
    colors_base = list(islice(cycle(colors_base), len(base_layers)))
    colors_point = ["red", "blue", "green", "orange"]
    colors_point = list(islice(cycle(colors_point), len(data)))
    for base_layer, clr_base, clr_point in zip(base_layers, colors_base, colors_point):
        base_layer.plot(ax=ax, color=clr_base, edgecolor="black", alpha=0)
        data.plot(ax=ax, color=clr_point, markersize=10)

    # TODO : Add legend for base layers and points and save the figure
