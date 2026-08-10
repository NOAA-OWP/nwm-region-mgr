#!/usr/bin/env python3
"""Sample calibration basins and generate pseudo stats for formulations."""

import argparse
import random
from pathlib import Path

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def sample_locations(locations, n_samples):
    """Select a uniform sample of locations using KMeans clustering."""
    if len(locations) <= n_samples:
        return locations

    coords = locations[["latitude", "longitude"]].to_numpy()
    kmeans = KMeans(n_clusters=n_samples, random_state=42, n_init=10)
    kmeans.fit(coords)

    sampled_indices = []
    for center in kmeans.cluster_centers_:
        closest_idx = np.argmin(np.linalg.norm(coords - center, axis=1))
        sampled_indices.append(closest_idx)

    return locations.iloc[sampled_indices]


def plot_map_static(locations, sampled_locations, domain, crs="EPSG:4326"):
    """Plot all locations and sampled locations on a basemap."""
    gdf_all = gpd.GeoDataFrame(
        locations.copy(),
        geometry=gpd.points_from_xy(locations.longitude, locations.latitude),
        crs=crs,
    )
    gdf_sampled = gpd.GeoDataFrame(
        sampled_locations.copy(),
        geometry=gpd.points_from_xy(
            sampled_locations.longitude, sampled_locations.latitude
        ),
        crs=crs,
    )

    gdf_all_web = gdf_all.to_crs(epsg=3857)
    gdf_sampled_web = gdf_sampled.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(10, 8))
    gdf_all_web.plot(
        ax=ax,
        color="orange",
        markersize=10,
        alpha=0.8,
        label=f"All calibration basins ({len(gdf_all)})",
    )
    gdf_sampled_web.plot(
        ax=ax,
        facecolor="none",
        edgecolor="red",
        markersize=30,
        label=f"Sampled calibration basins ({len(gdf_sampled)})",
    )

    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)
    ax.set_axis_off()
    ax.set_title(f"Spatial Distribution of Calibration Basins: {domain}", fontsize=14)
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f"sampled_calibration_basins_{domain}.png", dpi=300)


def create_calval_stats(input_dir: Path, domain1: str, n_sample: int, n_form: int):
    """Create pseudo calibration/validation stats for sampled basins and formulations."""
    formulations = [
        "noah-owp-modular cfe-s t-route",
        "noah-owp-modular cfe-x t-route",
        # "noah-owp-modular lasam t-route",
        "noah-owp-modular sac-sma t-route",
        # "noah-owp-modular ueb cfe-s t-route",
        "noah-owp-modular snow-17 cfe-s t-route",
        "noah-owp-modular snow-17 cfe-x t-route",
        "noah-owp-modular snow-17 sac-sma t-route",
        # "noah-owp-modular snow-17 lasam t-route",
        # "noah-owp-modular ueb lasam t-route",
        # "noah-owp-modular ueb cfe-x t-route",
        # "noah-owp-modular ueb topmodel t-route",
        # "noah-owp-modular snow-17 topmodel t-route",
        # "noah-owp-modular topmodel t-route",
    ]

    stats = [
        "bias",
        "rmse",
        "cor",
        "nse",
        "nselog",
        "nseWt",
        "kge",
        "msof",
        "hyperResMultiObj",
        "nnsesq",
        "eventmultiobj",
        "lbem",
        "lbemprime",
        "corr1",
        "pod",
        "far",
        "csi",
        "nnse",
        "peak_bias",
        "peak_tm_err_hr",
        "event_volume_bias",
    ]

    stats_dict = {}
    for eval_period in ["calib", "valid", "full"]:
        stats_all = pd.read_csv(input_dir / "stats_calib_valid_nwmv3.csv")
        stats_all = stats_all[
            (stats_all["simulation"] == "calibrated")
            & (stats_all["evalPeriod"] == eval_period)
            & (stats_all["jobID"] < 100)
        ]
        stats_all = stats_all[["evalPeriod"] + stats]
        stats_all["gage_idx"] = range(len(stats_all))
        stats_dict[eval_period] = stats_all

    cwt_file = input_dir / "cwt_divide_gage" / f"calib_gage_divide_{domain1}.parquet"
    if not cwt_file.exists():
        raise FileNotFoundError(f"Crosswalk file {cwt_file} does not exist.")
    df_cats = pd.read_parquet(cwt_file)

    gages = pd.read_csv(input_dir / "gages_nwm4_calib_all.csv")
    df_gages = df_cats.merge(gages[["gage_id", "latitude", "longitude"]], how="left")[
        ["gage_id", "latitude", "longitude", "vpuid"]
    ]
    df_gages = df_gages.drop_duplicates()
    df_gages = df_gages.dropna(subset=["latitude", "longitude"])

    n_sample = min(n_sample, len(df_gages))
    print(f"Sample {n_sample} locations from {len(df_gages)} in {domain1}")
    sampled_gages = sample_locations(df_gages, n_sample).reset_index(drop=True)

    plot_map_static(df_gages, sampled_gages, domain1)

    df_stats = pd.DataFrame()
    for vpu in sampled_gages["vpuid"].unique():
        forms = random.sample(formulations, n_form)
        gage_idxs = sampled_gages[sampled_gages["vpuid"] == vpu].index

        for form1 in forms:
            stats_idxs = [
                random.randint(
                    stats_dict["calib"]["gage_idx"].min(),
                    stats_dict["calib"]["gage_idx"].max(),
                )
                for _ in range(n_sample)
            ]
            for eval_period, stats_all in stats_dict.items():
                df1 = (
                    stats_all.set_index("gage_idx")
                    .reindex(stats_idxs)
                    .reset_index()
                    .loc[gage_idxs]
                )
                df2 = sampled_gages.loc[gage_idxs]
                df1 = pd.concat([df2, df1], axis=1).drop(columns=["gage_idx"])
                df1.insert(0, "formulation", form1)
                df_stats = pd.concat([df_stats, df1], ignore_index=True)

    df_stats = df_stats.sort_values(by=["gage_id", "formulation", "evalPeriod"])
    print(
        f"{len(df_stats) / 3} calibration/validation runs for {df_stats['gage_id'].nunique()} sampled basins"
    )

    df_stats = df_stats.drop(columns=["latitude", "longitude", "vpuid"])
    outdir = input_dir / "calval_stats"
    outdir.mkdir(parents=True, exist_ok=True)

    csv_file = outdir / f"stat_calval_all_{domain1}.csv"
    parquet_file = outdir / f"stat_calval_all_{domain1}.parquet"
    df_stats.to_csv(csv_file, index=False)
    df_stats.to_parquet(parquet_file, index=False)
    print(f"Wrote stats to {csv_file} and {parquet_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Formulation calval stats generation tool"
    )
    parser.add_argument(
        "--input_dir",
        type=Path,
        default=Path("~/repos/nwm-region-mgr/inputs/region").expanduser(),
        help="Input directory containing stats and gage files",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="conus",
        help="Domain name (e.g., conus, ak, hi, prvi)",
    )
    parser.add_argument(
        "--n_sample", type=int, default=1000, help="Number of gages to sample"
    )
    parser.add_argument(
        "--n_form", type=int, default=3, help="Number of formulations per VPU"
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    domain1 = args.domain
    n_sample = args.n_sample
    n_form = args.n_form

    create_calval_stats(input_dir, domain1, n_sample, n_form)
