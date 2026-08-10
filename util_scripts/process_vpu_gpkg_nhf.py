"""Processes the GPKG files for the VPUs in CONUS and oCONUS.

The script checks and reprojects CRS if necessary, and removes empty nexuses (i.e., nexuses with no upstream catchments)
from the nexus layer. The processed GPKG files will be used as input for regionalized NGEN simulations.
"""

import sqlite3
from pathlib import Path

import fiona
import geopandas as gpd
from shapely.ops import transform


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


def process_gpkg(target_gpkg, gdf_ref):
    """Process target GPKG file by checking CRS and reprojecting if necessary, then removing empty nexuses."""
    # remove empty nexuses
    remove_empty_nexus(target_gpkg)

    for layer in fiona.listlayers(target_gpkg):
        if layer not in fiona.listlayers(ref_gpkg):
            print(f"[SKIP] {layer}: not in reference")
            continue

        gdf_target = gpd.read_file(target_gpkg, layer=layer)
        gdf_ref = gpd.read_file(ref_gpkg, layer=layer)

        # Skip non-spatial layers
        if not isinstance(gdf_ref, gpd.GeoDataFrame):
            print(f"[SKIP] {layer}: not a spatial layer (no geometry)")
            continue

        # if layer == "divides" and "Cgw" in gdf_target.columns:
        #     gdf_target = gdf_target.rename(columns={"Cgw": "cgw"})
        #     print(f"[RENAME] {layer}: renamed 'Cgw' to 'cgw'")

        # Drop Z dimension if present
        gdf_target["geometry"] = gdf_target.geometry.apply(drop_z)

        if gdf_ref.crs is None:
            print(f"[SKIP] {layer}: reference CRS undefined")
            continue

        if gdf_target.crs is None:
            print(f"[ASSIGN] {layer}: setting CRS to {gdf_ref.crs}")
            gdf_target = gdf_target.set_crs(gdf_ref.crs)

        elif gdf_target.crs != gdf_ref.crs:
            print(f"[REPROJECT] {layer}")
            gdf_target = gdf_target.to_crs(gdf_ref.crs)
        else:
            continue

        gdf_target.to_file(target_gpkg, layer=layer, driver="GPKG")
        print(f"[SAVE] {layer}: saved changes to {target_gpkg}")


if __name__ == "__main__":
    vpus = [
        "02",
        "03N",
        "03W",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10L",
        "10U",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
    ]

    # read ref_gpkg to get reference CRS
    ref_gpkg = Path("~/data/hydrofabric/gpkg_nhf/Hawaii/16620000.gpkg").expanduser()
    gdf_ref = gpd.read_file(ref_gpkg, layer="divides")
    print(f"Reference CRS: {gdf_ref.crs}")

    for vpu in vpus:
        target_gpkg = Path(
            "~/run_region/region_input/hydrofabric/gpkg_nhf", f"vpu_{vpu}.gpkg"
        ).expanduser()

        process_gpkg(target_gpkg, gdf_ref)
