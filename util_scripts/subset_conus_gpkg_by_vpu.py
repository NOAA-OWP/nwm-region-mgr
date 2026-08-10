"""Retrieve VPU gpkg from conus.gpkg file"""

import argparse
from pathlib import Path

import fiona
import geopandas as gpd
import pandas as pd


def update_gpkg_layer(
    gpkg_path: Path | str,
    layer_name: str,
    new_gdf: gpd.GeoDataFrame,
    overwrite: bool = True,
):
    """Update or append rows to a layer in a GeoPackage.

    Args:
        gpkg_path: Path to the GeoPackage file.
        layer_name: Name of the layer to update.
        new_gdf: GeoDataFrame containing new/updated rows.
        overwrite: If True, replace existing layer with updated data.
                   If False, create a new layer with a modified name.
    """
    gpkg_path = Path(gpkg_path)

    # Check if layer exists
    existing_layers = fiona.listlayers(str(gpkg_path))
    if layer_name in existing_layers:
        # Read existing layer
        existing_gdf = gpd.read_file(gpkg_path, layer=layer_name)

        # Make CRS consistent
        new_gdf = new_gdf.to_crs(existing_gdf.crs)

        # Combine existing and new rows
        combined_gdf = gpd.GeoDataFrame(
            pd.concat([existing_gdf, new_gdf], ignore_index=True), crs=existing_gdf.crs
        )
        if overwrite:
            # Replace the existing layer
            combined_gdf.to_file(gpkg_path, layer=layer_name, driver="GPKG")
            print(f"Layer '{layer_name}' updated in {gpkg_path}")
        else:
            # Save to new layer
            new_layer_name = f"{layer_name}_updated"
            combined_gdf.to_file(gpkg_path, layer=new_layer_name, driver="GPKG")
            print(f"Layer '{new_layer_name}' created in {gpkg_path}")
    else:
        # Layer does not exist; create it
        new_gdf.to_file(gpkg_path, layer=layer_name, driver="GPKG")
        print(f"Layer '{layer_name}' created in {gpkg_path}")


def main(vpu_str: str):
    """Extract VPU from conus.gpkg and save to new gpkg file."""
    # conus gpkg file
    conus_in = Path(
        "~/s3/hydrofabric-data/patch/7_30_25/nwm_patch_conus_nextgen.gpkg"
    ).expanduser()

    # output gpkg file
    output_gpkg = (
        Path("../data/inputs/region/hydrofabric/gpkg_vpu/")
        / f"vpu_{vpu_str}_patch.gpkg"
    ).absolute()
    if output_gpkg.exists():
        print(f"Output gpkg {output_gpkg} already exists. Skipping extraction.")
        return

    output_gpkg.parent.mkdir(parents=True, exist_ok=True)

    if output_gpkg.exists():
        output_gpkg.unlink()

    # Set layers of conus geopackage
    layers = [
        "flowpaths",
        "divides",
        "lakes",
        "nexus",
        "pois",
        "hydrolocations",
        "flowpath-attributes",
        "network",
        "divide-attributes",
    ]

    # Loop through layers in gpkg, filtering by vpu_str
    for layer in layers:
        print(f"Processing layer: {layer}")

        # Read in conus geopackage layer
        gdf = gpd.read_file(conus_in, layer=layer)

        # Filter by VPU id
        filter_gdf = gdf[gdf["vpuid"] == vpu_str]

        # Fill layers with missing geometries
        if "geometry" not in filter_gdf.columns:
            filter_gdf = filter_gdf.copy()
            filter_gdf["geometry"] = None
            filter_gdf = gpd.GeoDataFrame(filter_gdf, geometry="geometry")
            filter_gdf.set_crs(crs="EPSG:5070", inplace=True)

        # Save to geopackage layer
        filter_gdf.to_file(output_gpkg, layer=layer, driver="GPKG")

        # save number of catchments for sanity check
        if layer == "divides":
            n_divides = filter_gdf.shape[0]
        elif layer == "divide-attributes":
            n_divide_attrs = filter_gdf.shape[0]

    # sanity check: ensure number of catchments in divides and divide-attributes layers are the same
    if n_divides != n_divide_attrs:
        print(
            f"Number of catchments not consist in divides and divide-attributes layers: "
            f"divides ({n_divides}), divide-attributes({n_divide_attrs})"
        )
        if n_divide_attrs < n_divides:
            # figure out which divides are missing in divide-attributes layer
            missing_divides = set(
                gpd.read_file(output_gpkg, layer="divides")["divide_id"]
            ) - set(gpd.read_file(output_gpkg, layer="divide-attributes")["divide_id"])
            print(f"Missing divide_ids in divide-attributes layer: {missing_divides}")

            # for missing divides in divide-attributes layer, get their attributes from a random existing catchment
            gdf = gpd.read_file(output_gpkg, layer="divide-attributes")
            new_attrs = pd.DataFrame()
            for divide_id in missing_divides:
                random_attrs = gdf.sample(n=1).iloc[0]
                random_attrs["divide_id"] = divide_id

                # append to new_attrs dataframe
                new_attrs = pd.concat(
                    [new_attrs, pd.DataFrame([random_attrs])], ignore_index=True
                )
            new_rows = gpd.GeoDataFrame(new_attrs, crs="EPSG:4326")

            update_gpkg_layer(
                output_gpkg, "divide-attributes", new_rows, overwrite=True
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract VPU from conus.gpkg")
    parser.add_argument(
        "--vpu", required=True, help="VPU identifier (e.g., 09, 10L, 10U)"
    )
    args = parser.parse_args()

    print(f"Extracting VPU {args.vpu} from CONUS geopackage...")
    main(args.vpu)
    print(f"VPU {args.vpu} geopackage created successfully.")
