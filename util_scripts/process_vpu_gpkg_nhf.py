"""Processes the GPKG files for the VPUs in CONUS and oCONUS.

The script checks and reprojects CRS if necessary, and removes empty nexuses (i.e., nexuses with no upstream catchments)
from the nexus layer. The processed GPKG files will be used as input for regionalized NGEN simulations.

Note for NHF 1.2.0, only the oCONUS domains (Alaska, Hawaii, Puerto Rico & Virgin Islands) needs to be processed,
as the CONUS VPUs are already in EPSG:4326.
"""

import shutil
import sqlite3
from pathlib import Path

import fiona
import geopandas as gpd
import pandas as pd
from shapely.ops import transform


def reproject_gpkg(
    input_gpkg: str | Path, output_gpkg: str | Path, target_crs: str = "EPSG:4326"
):
    """Reproject all spatial layers in a GeoPackage to the target CRS.

    Args:
        input_gpkg : str or Path
            Input GeoPackage.
        output_gpkg : str or Path
            Output GeoPackage.
        target_crs : str
            Target CRS (default: EPSG:4326).

    """
    input_gpkg = Path(input_gpkg)
    output_gpkg = Path(output_gpkg)

    # Remove existing output file
    if output_gpkg.exists():
        output_gpkg.unlink()

    # Copy input GPKG to output GPKG
    shutil.copy(input_gpkg, output_gpkg)

    layers = fiona.listlayers(output_gpkg)

    print(f"Found {len(layers)} layers")

    for layer in layers:
        print(f"Processing layer: {layer}")

        gdf = gpd.read_file(output_gpkg, layer=layer)

        # Skip non-spatial layer
        if not isinstance(gdf, gpd.GeoDataFrame):
            print(f"  Skipping non-spatial layer: {layer}")
            continue

        # Skip empty layer
        if gdf.empty:
            print("  Empty layer")
            gdf.to_file(output_gpkg, layer=layer, driver="GPKG")
            continue

        # Skip layer with no CRS and give a warning
        if gdf.crs is None:
            print("  WARNING: Layer has no CRS. Skipping.")
            continue

        print(f"  Original CRS: {gdf.crs}")

        if gdf.crs.to_string() != target_crs:
            gdf = gdf.to_crs(target_crs)
            print(f"  Reprojected to {target_crs}")

        # Drop Z dimension if present
        gdf["geometry"] = gdf.geometry.apply(drop_z)

        # if any column ending with _id is not integer, convert to integer
        for col in gdf.columns:
            if col.endswith("_id") and not pd.api.types.is_integer_dtype(gdf[col]):
                gdf[col] = gdf[col].astype("Int64")

        gdf.to_file(
            output_gpkg,
            layer=layer,
            driver="GPKG",
        )

        print(f"  Saved to {output_gpkg} with layer name: {layer}")


def drop_z(geom):
    """Drop Z dimension from geometry if present."""
    if geom is None:
        return geom

    return transform(lambda x, y, z=None: (x, y), geom)


def remove_empty_nexus(gpkg_file: Path):
    """Remove empty nexus (i.e., nexus with no upstream catchments) in the nexus layer."""
    conn = sqlite3.connect(gpkg_file)
    cur = conn.cursor()

    # find nexuses with no upstream divides
    cur.execute("""
    SELECT nex_id FROM nexus
    WHERE nex_id NOT IN (
        SELECT DISTINCT dn_nex_id FROM flowpaths
    )
    """)

    bad = [r[0] for r in cur.fetchall()]
    print("Removing", len(bad), "empty nexuses")

    # delete from nexus layer
    cur.executemany("DELETE FROM nexus WHERE nex_id=?", [(x,) for x in bad])

    conn.commit()
    conn.close()


def process_gpkg(input_gpkg, target_gpkg):
    """Process target GPKG file by checking CRS and reprojecting if necessary, then removing empty nexuses."""
    reproject_gpkg(input_gpkg, target_gpkg, target_crs="EPSG:4326")

    # remove_empty_nexus(target_gpkg)


if __name__ == "__main__":
    # fmt: off
    vpus = [
        ## CONUS vpus
        #"01", "02", "03N", "03S", "03W", "04", "05", "06", "07", "08", "09",
        #"10L", "10U", "11", "12", "13", "14", "15", "16", "17", "18",
        ## oCONUS VPUs
        "19",  # Alaska
        "20",  # Hawaii
        "21"   # Puerto Rico & Virgin Islands
    ]
    # fmt: on

    for vpu in vpus:
        input_gpkg = Path(
            "~/data/hydrofabric/gpkg_nhf_1.2.2", f"vpu_{vpu}.gpkg"
        ).expanduser()
        target_gpkg = Path(
            "~/repos/nwm-region-mgr/data/inputs/region/hydrofabric/gpkg_vpu",
            f"vpu_{vpu}.gpkg",
        ).expanduser()

        process_gpkg(input_gpkg, target_gpkg)
