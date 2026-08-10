"""Process the orginal VPU GeoPackage v2.2 files for use in regionalization.

The following processing steps are performed:

1. Reproject to WGS84 (EPSG:4326) if not already in that CRS
2. For non-spatial layers, add an empty geometry column with the same CRS as the spatial layers
3. Remove any empty nexus (i.e., nexus with no upstream catchments) in the nexus layer, as they cause issues in
ngen simulation
4. If hl_uri column is missing in hydrolocations layer, create hl_uri by combining "hl_reference" and "hl_link" columns
 (mainly for AK domain)

"""

import sqlite3
from pathlib import Path

import fiona
import geopandas as gpd
import pandas as pd


def reproject_and_add_geometry(src: Path, dst: Path, target_crs: str, vpu: str):
    """Reproject spatial layers to target CRS and add empty geometry to non-spatial layers."""
    layers = fiona.listlayers(src)

    for i, layer in enumerate(layers):
        print(f"Processing {layer}")

        df = gpd.read_file(src, layer=layer)

        mode = "w" if i == 0 else "a"

        # spatial layer
        if isinstance(df, gpd.GeoDataFrame) and df.geometry.name in df.columns:
            print("  → spatial layer")

            if df.crs is None and vpu == "prvi":
                print(f"  → CRS missing, assuming EPSG:6566 for {vpu}")
                df = df.set_crs(6566)
                df = df.to_crs(target_crs)
            else:
                print(f"  → CRS detected for {vpu}: {df.crs}")
                df = df.to_crs(target_crs)
        else:
            print("  → non-spatial layer, adding empty geometry")
            df["geometry"] = None

            df = gpd.GeoDataFrame(df, geometry="geometry", crs=target_crs)

        # create output directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        df.to_file(dst, layer=layer, driver="GPKG", mode=mode)


def remove_empty_nexus(gpkg_file: Path):
    """Remove empty nexus (i.e., nexus with no upstream catchments) in the nexus layer."""
    conn = sqlite3.connect(gpkg_file)
    cur = conn.cursor()

    # find nexuses with no upstream divides
    cur.execute("""
    SELECT id FROM nexus
    WHERE id NOT IN (
        SELECT DISTINCT toid FROM divides
    )
    """)

    bad = [r[0] for r in cur.fetchall()]
    print("Removing", len(bad), "empty nexuses")

    # delete from nexus layer
    cur.executemany("DELETE FROM nexus WHERE id=?", [(x,) for x in bad])

    conn.commit()
    conn.close()


def create_hl_uri_if_missing(gpkg_file: Path):
    """Add 'hl_uri' column to the hydrolocations layer if missing.

    Combines 'hl_reference' and 'hl_link', lowercase.
    Preserves all other columns and layers in the GeoPackage.
    """
    layer_name = "hydrolocations"

    # Read the layer into a GeoDataFrame
    gdf = gpd.read_file(gpkg_file, layer=layer_name)

    if "hl_uri" in gdf.columns:
        print("hl_uri column already exists. Skipping creation.")
        return

    print("Adding hl_uri column...")

    # Compute hl_uri safely
    gdf["hl_uri"] = gdf.apply(
        lambda row: f"{str(row.hl_reference).lower()}-{str(row.hl_link)}"
        if pd.notnull(row.hl_reference) and pd.notnull(row.hl_link)
        else None,
        axis=1,
    )

    gdf.to_file(gpkg_file, layer=layer_name, driver="GPKG")


def main():
    """Process VPU GeoPackage files."""
    # source folder for original VPU GeoPackage files
    src_dir = Path("~/data/hydrofabric/gpkg_vpu_original").expanduser()

    # find all gpkg files in the source folder
    gpkg_files = list(src_dir.glob("vpu_*.gpkg"))
    print(f"Found {len(gpkg_files)} GeoPackage files in {src_dir}:")

    # loop through each gpkg file and process
    for src in gpkg_files:
        vpu = src.stem.replace("vpu_", "").replace("_patch", "")
        print(f"\n--------------- Processing VPU {vpu} ---------------")

        dst = Path(
            f"~/repos/nwm-region-mgr/data/inputs/region/hydrofabric/gpkg_vpu/vpu_{vpu}.gpkg"
        ).expanduser()

        # if output file already exists, overwrite
        if dst.exists():
            print(f"{dst} already exists. Skipping...")
            continue

        print("Reprojecting and adding geometry...")
        reproject_and_add_geometry(src, dst, target_crs="EPSG:4326", vpu=vpu)

        print("Creating hl_uri if missing...")
        create_hl_uri_if_missing(dst)

        print("Removing empty nexus...")
        remove_empty_nexus(dst)

        print(f"Finished processing VPU {vpu}.")


if __name__ == "__main__":
    main()
