"""Create NGEN crosswalk for all gages for regionalization evaluation."""

import argparse
from pathlib import Path

import geopandas as gpd


def main(domain: str = "conus", out_dir: str | Path = "."):
    """Create ngen divide crosswalk for all gages for regionalization evaluation."""
    # Input GeoPackage (mount the s3 bucket with: s3fs hydrofabric-data ~/s3/hydrofabric-data)
    conus_in = Path(
        f"~/s3/hydrofabric-data/patch/7_30_25/nwm_patch_{domain}_nextgen.gpkg"
    ).expanduser()

    print(f"Reading hydrolocations from {conus_in}...")
    gdf = gpd.read_file(conus_in, layer="hydrolocations")

    # Select required columns
    df_cwt = gdf[["id", "hl_uri", "vpuid"]].copy()

    # Keep only rows with hl_uri starting with 'gages-'
    df_cwt = df_cwt[df_cwt["hl_uri"].str.startswith("gages-")].copy()

    print(f"Reading divides from {conus_in}...")
    gdf_divides = gpd.read_file(conus_in, layer="divides")[["id", "geometry"]]

    print("Merging crosswalk with divide geometries...")
    df_cwt = df_cwt.merge(gdf_divides, on="id", how="left")
    gdf_cwt = gpd.GeoDataFrame(df_cwt, geometry="geometry", crs=gdf_divides.crs)

    print("Converting divide polygons to points with centroids...")
    gdf_cwt["centroid"] = gdf_cwt.geometry.centroid
    gdf_cwt["geometry"] = gpd.points_from_xy(
        gdf_cwt["centroid"].x, gdf_cwt["centroid"].y, crs=gdf_cwt.crs
    )
    gdf_cwt = gdf_cwt.drop(columns=["centroid"])

    # Reproject to WGS84 (lat/lon)
    gdf_cwt = gdf_cwt.to_crs(epsg=4326)

    # Replace prefixes to make location IDs
    gdf_cwt["secondary_location_id"] = gdf_cwt["id"].str.replace(
        "wb-", "ngen-", regex=False
    )
    gdf_cwt["primary_location_id"] = gdf_cwt["hl_uri"].str.replace(
        "gages-", "usgs-", regex=False
    )

    # Add domain column
    gdf_cwt["domain"] = domain.upper()

    # Reorder columns
    gdf_cwt = gdf_cwt[
        ["domain", "primary_location_id", "secondary_location_id", "vpuid", "geometry"]
    ]

    # Save the crosswalk GeoDataFrame to Parquet
    cwt_file = Path(out_dir) / f"usgs_ngen_crosswalk_{domain}.parquet"
    print(f"Saving Crosswalk GeoDataFrame to {cwt_file} with {len(gdf_cwt)} entries...")

    cwt_file.parent.mkdir(parents=True, exist_ok=True)
    gdf_cwt.to_parquet(cwt_file, index=False)

    # loop through unique VPUs to create a gage list file for each VPU
    for vpu in gdf_cwt["vpuid"].dropna().unique():
        df_vpu = gdf_cwt.loc[gdf_cwt["vpuid"] == vpu, ["primary_location_id"]].copy()
        df_vpu.rename(columns={"primary_location_id": "gage"}, inplace=True)

        # remove "gages-" prefix
        df_vpu["gage"] = df_vpu["gage"].str.replace("usgs-", "", regex=False)

        gage_file = Path(out_dir) / f"gage_list_{domain}_vpu_{vpu}.csv"
        df_vpu = df_vpu.sort_values(by="gage").reset_index(drop=True)

        df_vpu.to_csv(gage_file, index=False, header=True)
        print(f"Gage list for VPU {vpu} saved to {gage_file} with {len(df_vpu)} gages.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create crosswalk for all gages.")
    parser.add_argument(
        "--domain",
        type=str,
        default="conus",
        help="Domain name (default: conus)",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default=".",
        help="Output directory for the crosswalk files",
    )

    args = parser.parse_args()
    main(args.domain, args.out_dir)
