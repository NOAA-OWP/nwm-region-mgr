"""Functions for generating specific/interim plots from parameter regionalization.

plot_outputs.py

Functions:
    - plot_missing_attr_counts: Plots the number of catchments with missing values for each selected attribute.
    - plot_donor_spatial_map: Plots the spatial distribution of donors within a VPU and its buffer zone.

"""

import logging
from pathlib import Path
from typing import Union

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.validation import make_valid

from nwm_region_mgr.parreg import config_schema as cs
from nwm_region_mgr.utils import read_table

logger = logging.getLogger(__name__)


def plot_missing_attr_counts(
    config: cs.Config, vpu: str, df_attrs_all: pd.DataFrame
) -> None:
    """Plot the number of catchments with missing values for each selected attribute.

    Args:
        config : cs.Config
            Configuration object containing settings for the regionalization.
        vpu : str
            The VPU (Vector Processing Unit) identifier.
        df_attrs_all : pd.DataFrame
            DataFrame containing all attributes for the catchments.

    """
    cols = []
    for dataset in config.general.attr_dataset_list:
        cols = cols + [
            dataset + "_" + x for x in getattr(config.attr_datasets, dataset).attr_list
        ]

    missing_cols = set(cols) - set(df_attrs_all.columns)
    cols1 = [col for col in cols if col not in missing_cols]

    if missing_cols:
        logger.warning(
            f"Missing columns in final attribute dataframe df_attrs_all: {missing_cols}."
        )
        logger.info("Please check the configuration.")

    # Compute missing counts
    missing_counts = df_attrs_all[cols1].isnull().sum()
    total = len(df_attrs_all)

    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.bar(
        missing_counts.index, missing_counts.values, color="skyblue", edgecolor="black"
    )
    ax1.set_ylabel("Missing Count")
    ax1.set_title(
        f"Number (and %) of Catchments with Missing Values for Each Selected Attribute (VPU {vpu})"
    )

    # Rotate x-labels for readability
    plt.xticks(rotation=90, ha="center")

    # Add secondary axis for percentage
    ax2 = ax1.twinx()
    ax2.set_ylim(ax1.get_ylim()[0], ax1.get_ylim()[1])
    ax2.set_ylabel("Missing (%)")

    # Set percent ticks aligned with counts
    yticks = ax1.get_yticks()
    ax2.set_yticks(yticks)
    ax2.set_yticklabels([f"{y / total * 100:.1f}%" for y in yticks])

    # Save figure
    out = getattr(config.output, "attr_data_final", None)
    if out is None:
        msg = "Output configuration for 'attr_data_final' is not defined. Skipping plot saving."
        logger.warning(msg)
        return

    outfile = Path(
        out.path,
        f"plots/bar_attr_missing_count_{config.general.domain}_vpu{vpu}.png",
    )
    outfile.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile, bbox_inches="tight")
    logger.info(f"Missing attribute counts plot saved to {outfile}")

    plt.close(fig)


def plot_donor_spatial_map(
    config: cs.Config,
    vpu: str,
    donor_basins: list,
    final_donor_basins: list,
    gdf_buffered: Union[Polygon, MultiPolygon],
    combined_geom: Union[Polygon, MultiPolygon],
    donors_only: bool = False,
) -> None:
    """Plot the spatial distribution of donors within a VPU and its buffer zone.

    Args:
        config : cs.Config
            Configuration object containing settings for the regionalization.
        vpu : str
            The VPU (Vector Processing Unit) identifier.
        donor_basins : list
            List of initial donor basin identifiers.
        final_donor_basins : list
            List of final donor basin identifiers.
        gdf_buffered : gpd.GeoDataFrame
            GeoDataFrame of the buffered VPU polygon.
        combined_geom : gpd.GeoDataFrame
            GeoDataFrame of the combined geometry of the VPU.
        donors_only: bool
            Whether to plot donor basins only (i.e., omit receivers)

    """
    # read in lat/lon of all donors
    gage_col = getattr(config.general.id_col, "gage", "gage_id")
    donors_all = read_table(config.general.donor_gage_file, dtype={gage_col: str})

    # filter donors based on the donor_basins list (qualified donors)
    donors = donors_all[donors_all[gage_col].isin(donor_basins)]
    donor_gdf = gpd.GeoDataFrame(
        donors,
        geometry=[Point(xy) for xy in zip(donors["longitude"], donors["latitude"])],
        crs="EPSG:4326",
    )

    # Project to meters for accurate distance calculations
    donor_gdf = donor_gdf.to_crs(epsg=3857)

    # visualize the donors selected
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot base layer, use combined_geom if ring is empty (buffer is zero)
    gdf_buffered = make_valid(gdf_buffered)
    combined_geom = make_valid(combined_geom)

    ring = gdf_buffered.difference(combined_geom)

    if ring.is_empty:
        base_geom = combined_geom
    else:
        base_geom = ring
    base_geom = make_valid(base_geom)
    base_geom = base_geom.buffer(0)  # fix any invalid geometries in the ring
    ring_gdf = gpd.GeoDataFrame(geometry=[base_geom], crs=donor_gdf.crs)

    ring_gdf.plot(ax=ax, facecolor="lightgray", edgecolor="black")

    # donor and non-donor calibration basins in the buffered VPU
    non_donor_gdf = donor_gdf[~donor_gdf["gage_id"].isin(final_donor_basins)]
    final_donor_gdf = donor_gdf[donor_gdf["gage_id"].isin(final_donor_basins)]

    # plot calibration basins in the buffered VPU
    if not donors_only:
        non_donor_gdf.plot(ax=ax, color="red", markersize=20, marker="x")
    final_donor_gdf.plot(
        ax=ax, edgecolor="red", facecolor="none", markersize=20, marker="o"
    )

    # donors and non-donors in the original VPU
    donors_vpu = final_donor_gdf[final_donor_gdf.geometry.within(combined_geom)]
    non_donors_vpu = non_donor_gdf[non_donor_gdf.geometry.within(combined_geom)]
    donors_vpu.plot(
        ax=ax, edgecolor="blue", facecolor="none", markersize=20, marker="o"
    )
    if not donors_only:
        non_donors_vpu.plot(ax=ax, color="blue", markersize=20, marker="x")

    # Create custom legend handles
    leg_donor_vpu = Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label=f"Donors within VPU ({len(donors_vpu)})",
        markeredgecolor="blue",
        markerfacecolor="none",
        markersize=6,
    )
    leg_donor_buffer = Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label=f"Donors in buffer zone ({len(final_donor_gdf) - len(donors_vpu)})",
        markeredgecolor="red",
        markerfacecolor="none",
        markersize=6,
    )
    leg_non_donor_vpu = Line2D(
        [0],
        [0],
        marker="x",
        color="blue",
        label=f"non-donors within VPU ({len(non_donors_vpu)})",
        markersize=6,
        linestyle="None",
    )
    leg_non_donor_buffer = Line2D(
        [0],
        [0],
        marker="x",
        color="red",
        label=f"non-donors in buffer zone ({len(non_donor_gdf) - len(non_donors_vpu)})",
        markersize=6,
        linestyle="None",
    )
    leg_buffer_zone = Line2D(
        [0],
        [0],
        marker="s",
        color="black",
        label=f"Buffer zone ({round(config.donor.buffer_km)} km)",
        markerfacecolor="lightgray",
        markersize=6,
        linestyle="None",
    )
    if ring.is_empty:
        if not donors_only:
            legend_elements = [
                leg_donor_vpu,
                leg_non_donor_vpu,
            ]
        else:
            legend_elements = [leg_donor_vpu]
    else:
        if not donors_only:
            legend_elements = [
                leg_donor_vpu,
                leg_donor_buffer,
                leg_non_donor_vpu,
                leg_non_donor_buffer,
                leg_buffer_zone,
            ]
        else:
            legend_elements = [
                leg_donor_vpu,
                leg_donor_buffer,
                leg_buffer_zone,
            ]

    # Add legend
    ax.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5))

    # title
    plt.title(f"Donor basins available for VPU {vpu} regionalization")

    # tidy up plot
    ax.set_axis_off()
    plt.tight_layout()

    # save the figure
    out = getattr(config.output, "pairs", None)
    if out is None:
        msg = "Output configuration for 'pairs' is not defined. Skipping plot saving."
        logger.warning(msg)
        return

    outfile = Path(
        out.path,
        f"plots/map_donors_{config.general.domain}_vpu{vpu}.png",
    )
    outfile.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outfile, bbox_inches="tight")
    logger.info(f"Donor spatial map saved to {outfile}")

    plt.close(fig)
