# python script to create crosswalk table between NextGen catchments and HUC12s

from pathlib import Path

import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


def create_cwt(vpu: str, shp1: gpd.GeoDataFrame, shp2: gpd.GeoDataFrame):
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
    overlap = overlap[["divide_id", "HUC_12", "overlap_area"]]
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
    nearest_matches = nearest_matches[["divide_id", "HUC_12", "nearest_dist_m"]]

    # create the final huc12/divide_id crosswalk table
    cwt = pd.concat([max_overlap, nearest_matches], axis=0, ignore_index=True)

    # rename column 'HUC_12' to 'huc12'
    cwt.rename(columns={"HUC_12": "huc12"}, inplace=True)

    return cwt


# Read HUC12 shapefiles
f1 = (
    "/home/yuqiong.liu/work/data/NHDPlusV21/NHDPlusNationalData/NationalWBDSnapshot.gdb"
)
shp_huc = gpd.read_file(f1)


gdb_path = (
    "/home/yuqiong.liu/work/data/NHDPlusV21/NHDPlusNationalData/NationalWBDSnapshot.gdb"
)
layer_name = "WBDSnapshot_National"  # Can be determined by listing layers
columns_to_check = {"geometry", "HUC_12"}

# List all layers if you're not sure of the layer name
print(fiona.listlayers(gdb_path))

with fiona.open(gdb_path, layer=layer_name) as src:
    # Get schema field names (attribute columns only)
    existing_fields = set(src.schema["properties"].keys())
    # Add geometry as a special case
    existing_fields.add("geometry")

    missing_fields = columns_to_check - existing_fields
    if missing_fields:
        print("Missing fields:", missing_fields)
    else:
        print("All fields exist.")

# %%
# loop through the domains and read NextGen hydrofabric for the domain
# Note: process conus, hi, and prvi first, since they can share the same 'shp_huc'from above;
# for AK, a new NHD gpkg file will be used (see below)
domain = "conus"
# domain = 'hi'
# domain = 'prvi'
# domain = 'ak'

if domain == "ak":
    file_ak = Path(
        "/home/yuqiong.liu/work/data/NHDPlusV21/NHD_H_Alaska_State_GPKG.gpkg"
    ).resolve(strict=True)
    shp_huc = gpd.read_file(file_ak, layer="WBDHU12")
    shp_huc["VPUID"] = "19"
    shp_huc.rename(columns={"huc12": "HUC_12"}, inplace=True)

f2 = Path("/home/yuqiong.liu/work/data/gpkg_v2.2/", domain + "_nextgen.gpkg").resolve()
shp_ngen = gpd.read_file(f2, layer="divides")
if domain == "ak":
    shp_ngen["vpuid"] = "19"
elif domain == "hi":
    shp_ngen["vpuid"] = "20"
elif domain == "prvi":
    shp_ngen["vpuid"] = "21"

# %%
# Create ngen catchment - huc12 crosswalk; process by vpus to reduce memory usage
vpus = shp_ngen["vpuid"].unique()
df_cwt = pd.DataFrame()
for vpu in vpus:
    print(f"Processing VPU {vpu}")
    shp1 = shp_huc[shp_huc["VPUID"] == vpu]
    shp2 = shp_ngen[shp_ngen["vpuid"] == vpu]
    df_cwt = pd.concat([df_cwt, create_cwt(vpu, shp1, shp2)])

# %%
# save crosswalk to file for use in formulation regionalization later
outdir = Path("/home/yuqiong.liu/work/data/ngen_reg/inputs/cwt_ngen_huc12")
outdir.mkdir(exist_ok=True, parents=True)
outfile = Path(outdir, "cwt_huc12_divide_" + domain + ".csv")

# Round all numeric columns to 2 decimal places
df_cwt[df_cwt.select_dtypes(include=["float64", "int64"]).columns] = (
    df_cwt.select_dtypes(include=["float64", "int64"]).round(2)
)

df_cwt.to_csv(outfile, index=False)

# %%
# print summary
print(f"Domain = {domain}")
print(
    f"Number of catchments matched with HUC12: {len(df_cwt[df_cwt['nearest_dist_m'].isna()])}"
)
print(
    f"Number of catchments not matched with HUC12: {len(df_cwt[~df_cwt['nearest_dist_m'].isna()])}"
)
display(df_cwt)

# %%
