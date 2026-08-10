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
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable

from nwm_region_mgr.utils.hydrofabric_utils import dissolve_polygons

logger = logging.getLogger(__name__)


def _plot_columns_by_dtype(
    gdf: gpd.GeoDataFrame,
    columns: list[str],
    fillna_value=None,
    num_bins: int = None,
    cmap_numeric: str = "viridis",
    cmap_categorical: str = "Set3",
    figsize=(10, 6),
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
        antialiased: whether to disable antialiasing for the plots

    """
    n = len(columns)
    ncols = min(4, n)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = np.atleast_1d(axes).flatten()

    # outer boundary
    combined_polygon = dissolve_polygons(gdf, remove_holes=True)
    boundary = combined_polygon.boundary

    for i, column in enumerate(columns):
        ax = axes[i]
        dtype = gdf[column].dtype

        gdf_plot = gdf.copy()
        if fillna_value is not None:
            gdf_plot[column] = gdf_plot[column].fillna(fillna_value)

        gdf_plot = gdf_plot[~gdf_plot[column].isna()]
        if gdf_plot.empty:
            ax.axis("off")
            continue

        # numeric columns
        if pd.api.types.is_numeric_dtype(dtype):
            values = gdf_plot[column]

            if num_bins is not None:  # Treat as categorical (binned)
                values = pd.cut(values, bins=num_bins)
                gdf_plot["__binned__"] = values
                gdf_plot.plot(
                    ax=ax,
                    column="__binned__",
                    cmap=cmap_numeric,
                    edgecolor="none",
                    linewidth=0,
                )

                legend = ax.get_legend()
                if legend:
                    labels = [t.get_text() for t in legend.get_texts()]
                    ncol_legend = min(3, max(1, len(labels) // 2))

                    legend.set_bbox_to_anchor((0.5, -0.18))
                    legend.set_loc("upper center")
                    legend.set_ncol(ncol_legend)
                    legend.set_frame_on(True)

            else:
                vmin, vmax = values.min(), values.max()
                norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
                cmap = plt.get_cmap(cmap_numeric)

                gdf_plot.plot(
                    ax=ax,
                    column=column,
                    cmap=cmap,
                    edgecolor="none",
                    linewidth=0,
                )

                divider = make_axes_locatable(ax)
                cax = divider.append_axes("bottom", size="5%", pad=0.4)

                sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
                sm.set_array([])

                fig.colorbar(sm, cax=cax, orientation="horizontal")

        # categorical columns
        elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(
            dtype
        ):
            gdf_plot[column] = gdf_plot[column].astype("category")

            gdf_plot.plot(
                ax=ax,
                column=column,
                cmap=cmap_categorical,
                edgecolor="none",
                linewidth=0,
                legend=True,
            )

            legend = ax.get_legend()
            if legend:
                labels = [t.get_text() for t in legend.get_texts()]

                # dynamic column layout
                if len(labels) <= 3:
                    ncol_legend = len(labels)
                elif len(labels) <= 10:
                    ncol_legend = 4
                else:
                    ncol_legend = 5

                legend.set_bbox_to_anchor((0.5, -0.18))
                legend.set_loc("upper center")
                legend.set_ncols(ncol_legend)
                legend.set_frame_on(True)

                # shrink font if too many categories
                if len(labels) > 10:
                    for text in legend.get_texts():
                        text.set_fontsize(8)

        else:
            ax.set_title(f"Unsupported dtype: {column}")
            ax.axis("off")
            continue

        # antialiasing fix
        for coll in ax.collections:
            coll.set_antialiased(antialiased)

        # boundary overlay
        gpd.GeoSeries(boundary).plot(ax=ax, color="black", linewidth=0.5)

        ax.set_title(column)
        ax.set_axis_off()

    # turn off unused axes
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    # leave space for bottom elements
    plt.tight_layout(rect=[0, 0.12, 1, 0.95])

    return fig, axes[: i + 1]


def plot_spatial_map(gdf: gpd.GeoDataFrame, d1: dict) -> None:
    """Generate a spatial map plot for the given data.

    Args:
        gdf : gpd.GeoDataFrame
            GeoDataFrame containing the data to be plotted.
        d1: dict
            Information needed for creating the plot

    """
    _, ax = plt.subplots(figsize=(8, 6))

    # create spatial map
    fig, axes = _plot_columns_by_dtype(
        gdf,
        columns=d1["columns"],
        fillna_value=d1.get("fillna_value", None),
        num_bins=d1.get("num_bins", None),
        cmap_numeric=d1.get("cmap_numeric", "viridis"),
        cmap_categorical=d1.get("cmap_categorical", "Set3"),
    )

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
        plt.close(fig)
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
            - title: title of the plot
            - var_str: variable string for the plot
            - vpu: VPU identifier
            - algorithm: algorithm used for pairing (optional)

    """
    columns = d1.get("columns", [])
    if not columns:
        logger.warning("No valid columns specified to plot for histogram.")
        return

    n = len(columns)
    ncols = min(2, n)  # cap at 2 columns, but don’t exceed n
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4 * nrows))
    axes = np.atleast_1d(axes).flatten()  # always normalize to an array

    for i, col in enumerate(columns):
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
    for j in range(len(columns), len(axes)):
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
        plt.close(fig)
        logger.info(
            f"Histogram of {d1['var_str']} for VPU {d1['vpu']} saved to {d1['outfile']}"
        )
    else:
        logger.warning("No output file specified for histogram plot. Skipping save.")


# NOT USED YET (keep for future use)
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
