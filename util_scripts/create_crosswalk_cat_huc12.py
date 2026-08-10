"""python script to create crosswalk table between NextGen catchments and HUC12s."""

from functools import lru_cache
from pathlib import Path

import geopandas as gpd
import pandas as pd


def create_cwt(
    vpu: str, shp1: gpd.GeoDataFrame, shp2: gpd.GeoDataFrame, huc_col: str
) -> pd.DataFrame:
    """Create crosswalk table between NextGen catchments and HUC12s for a given VPU."""
    # Convert to a projected CRS for accurate area calculations
    projected_crs = "EPSG:3857"
    shp1 = shp1.to_crs(projected_crs)
    shp2 = shp2.to_crs(projected_crs)

    # Find overlapping areas
    overlap = gpd.overlay(shp2, shp1, how="intersection")

    # Compute area of each original polygon in shp2 (and convert to km^2)
    shp2["original_area"] = shp2.geometry.area / 1_000_000

    # Compute intersection area (and convert to km^2)
    overlap["overlap_area"] = overlap.geometry.area / 1_000_000

    # merge with shp2
    overlap = overlap[["divide_id", huc_col, "overlap_area"]]
    shp2_tmp = shp2[["divide_id", "areasqkm", "original_area"]]
    overlap = overlap.merge(shp2_tmp, on="divide_id", how="left")

    # Calculate percentage of each shp2 polygon that is covered by intersecting polygons in shp1
    overlap["overlap_percentage"] = (
        overlap["overlap_area"] / overlap["original_area"]
    ) * 100

    # Find the maximum overlapping shp1 polygon for each polygon in shp2
    max_overlap = overlap.loc[
        overlap.groupby("divide_id")["overlap_percentage"].idxmax()
    ]

    # identify shp2 polygons not paired with a shp1 polygon
    polys = shp2["divide_id"].unique()
    polys_matched = max_overlap["divide_id"].unique()
    polys_unmatched = [x for x in polys if x not in polys_matched]

    # Find the nearest shp1 polygon for each unmatched shp2 polygon
    nearest_matches = gpd.sjoin_nearest(
        shp2[shp2["divide_id"].isin(polys_unmatched)],
        shp1,
        how="left",
        distance_col="nearest_distance",
    )
    nearest_matches.rename(columns={"nearest_distance": "nearest_dist_m"}, inplace=True)
    nearest_matches = nearest_matches[["divide_id", huc_col, "nearest_dist_m"]]

    # create the final huc12/divide_id crosswalk table
    cwt = pd.concat([max_overlap, nearest_matches], axis=0, ignore_index=True)

    return cwt


@lru_cache(maxsize=None)
def read_huc_layer(path: str, layer: str) -> gpd.GeoDataFrame:
    """Read and cache a GeoDataFrame by path and layer."""
    return gpd.read_file(Path(path).expanduser(), layer=layer)


def process_domain(domain: list | str):
    """Loop through the domains and read NextGen hydrofabric for the domain."""
    # Note: process conus, hi, and prvi first, since they can share the same 'shp_huc'from above;
    # for AK, a new NHD gpkg file will be used (see below)
    domains = (
        ["conus", "hi", "prvi", "ak"]
        if domain == "all"
        else domain
        if isinstance(domain, list)
        else [domain]
    )
    for domain in domains:
        print(f"Processing domain: {domain}")

        # Read HUC12 shapefiles
        if domain != "ak":
            shp_huc = read_huc_layer(
                "~/work/data/NHDPlusV21/NHDPlusNationalData/NationalWBDSnapshot.gdb",
                "WBDSnapshot_National",
            )
            shp_huc["VPUID"] = shp_huc["VPUID"].astype(str)
            huc_col = "HUC_12"
        else:
            shp_huc = read_huc_layer(
                "~/work/data/NHDPlusV21/NHD_H_Alaska_State_GPKG.gpkg", "WBDHU12"
            ).copy()
            shp_huc["VPUID"] = "19"
            huc_col = "huc12"
            # shp_huc.rename(columns={"huc12": "HUC_12"}, inplace=True)

        # Read NextGen hydrofabric shapefiles
        f2 = Path("~/work/data/gpkg_v2.2/", domain + "_nextgen.gpkg").expanduser()
        shp_ngen = gpd.read_file(f2, layer="divides")
        if domain == "ak":
            shp_ngen["vpuid"] = "19"
        elif domain == "hi":
            shp_ngen["vpuid"] = "20"
        elif domain == "prvi":
            shp_ngen["vpuid"] = "21"

        # Create ngen catchment - huc12 crosswalk; process by vpus to reduce memory usage
        vpus = shp_ngen["vpuid"].unique()
        df_cwt = pd.DataFrame()
        for vpu in vpus:
            print(f"Processing VPU {vpu}")
            shp1 = shp_huc[shp_huc["VPUID"] == vpu]
            shp2 = shp_ngen[shp_ngen["vpuid"] == vpu]
            df = create_cwt(vpu, shp1, shp2, huc_col)
            df.rename(
                columns={huc_col: huc_col.lower()}, inplace=True
            )  # rename huc_col to lowercase
            df_cwt = pd.concat([df_cwt, df])

        # Round all numeric columns to 2 decimal places
        df_cwt[df_cwt.select_dtypes(include=["float64", "int64"]).columns] = (
            df_cwt.select_dtypes(include=["float64", "int64"]).round(2)
        )

        # save crosswalk to file for use in formulation regionalization later
        outdir = Path(
            "~/repos/nwm-region-mgr/inputs/region/cwt_ngen_huc12"
        ).expanduser()
        outdir.mkdir(exist_ok=True, parents=True)
        outfile = Path(outdir, "cwt_huc12_divide_" + domain + ".csv")
        df_cwt.to_csv(outfile, index=False)

        # print summary
        print(
            f"Number of catchments matched with HUC12: {len(df_cwt[df_cwt['nearest_dist_m'].isna()])}"
        )
        print(
            f"Number of catchments not matched with HUC12: {len(df_cwt[~df_cwt['nearest_dist_m'].isna()])}"
        )


if __name__ == "__main__":
    process_domain("all")
