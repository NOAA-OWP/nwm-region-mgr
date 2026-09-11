#!/usr/bin/env python3
"""Create crosswalk files between calibration gages and divides for NWM regionalization.

The script supports both NHF v1 and v2.2 GPKG files.

See run_create_crosswalk_ngen_donor.sh for example usage.

"""

import argparse
import glob
from pathlib import Path

import geopandas as gpd
import pandas as pd


def resolve_nested_gages(
    df: pd.DataFrame, nested_gages: str, id_col: str, area_col: str = "area_sqkm"
) -> pd.DataFrame:
    """Resolve nested gages by keeping only one gage per divide.

    For divides associated with multiple gages, keep the gage with
    the smallest or largest total drainage area.
    """
    # Find divides with multiple gages
    duplicates = df[df[id_col].duplicated(keep=False)]
    if duplicates.empty:
        return df

    # Compute drainage area for each gage
    gage_area = (
        df.groupby("gage_id", as_index=False)[area_col]
        .sum()
        .rename(columns={area_col: "drainage_area"})
    )

    # Join back to duplicates
    nested = duplicates.merge(gage_area, on="gage_id", how="left")

    # Select either the min or max drainage area per divide
    if nested_gages == "inner":
        keep = nested.loc[nested.groupby(id_col)["drainage_area"].idxmin()]
    elif nested_gages == "outer":
        keep = nested.loc[nested.groupby(id_col)["drainage_area"].idxmax()]
    else:
        raise ValueError(
            f"Invalid value for 'nested_gages': {nested_gages}. Expected 'inner' or 'outer'."
        )

    # Keep all unique divides + the chosen nested gages
    keep = keep.drop(columns=["drainage_area"])
    df_unduplicated = df[~df[id_col].isin(duplicates[id_col])]
    result = pd.concat([df_unduplicated, keep])

    return result.reset_index(drop=True)


def build_crosswalks(
    domains: list,
    input_dir: Path,
    outdir: Path,
    gages_file: Path,
    nested_gages: str = "inner",
    hf_version: str = "nhf",
):
    id_col = "divide_id" if hf_version == "v2.2" else "div_id"
    area_col = "areasqkm" if hf_version == "v2.2" else "area_sqkm"
    vpu_col = "vpuid" if hf_version == "v2.2" else "vpu_id"

    """Build crosswalk parquet files for all calibration domains."""
    domains_dict = {
        "conus": "CONUS",
        "ak": "Alaska",
        "hi": "Hawaii",
        "prvi": "Puerto_Rico",
    }

    outdir.mkdir(exist_ok=True, parents=True)
    ngage = ncats = 0

    for domain in domains:
        domain1 = domains_dict[domain]
        outfile = Path(outdir, f"calib_gage_divide_{domain}.parquet")
        if outfile.exists():
            print(f"Crosswalk file already exists for {domain1}: {outfile}. Skip")
            continue

        dir1 = Path(input_dir, domain1).resolve(strict=True)
        files = glob.glob(f"{dir1}/*.gpkg")

        df_cats = pd.DataFrame()
        for f1 in files:
            cats = gpd.read_file(f1, layer="divides")
            cols = [id_col, area_col, vpu_col, "type"]
            cats = cats.reindex(columns=cols, fill_value=float("nan"))

            cats["gage_id"] = (
                Path(f1)
                .name.replace("gages-", "")
                .replace("gauge_", "")
                .replace(".gpkg", "")
            )

            cats.insert(0, "gage_id", cats.pop("gage_id"))
            df_cats = pd.concat([df_cats, cats], ignore_index=True, axis=0)

        # resolve nested gages
        df_cats = resolve_nested_gages(
            df_cats, nested_gages=nested_gages, id_col=id_col, area_col=area_col
        )

        # save crosswalk to file for use in regionalization later
        df_cats[id_col] = df_cats[id_col].astype("string")
        df_cats.to_parquet(outfile, index=False)
        print(
            f"There are {len(files)} calibration gages and {len(df_cats)} catchments in the {domain} domain"
        )

        ngage += len(files)
        ncats += len(df_cats)

    # calibration gage list
    df_gages = pd.read_csv(gages_file)
    df_gages["domain"] = df_gages["domain"].str.replace(" ", "_", regex=False)

    for domain in domains:
        domain1 = domains_dict[domain]
        outfile = Path(outdir, f"calib_gage_divide_{domain}.parquet")
        if not outfile.exists():
            print(
                f"Crosswalk file not found for {domain1} at expected location: {outfile}"
            )
            continue
        df1 = pd.read_parquet(outfile)

        # check to make sure no duplicate divides
        dup_divides = df1[df1[id_col].duplicated(keep=False)]
        if not dup_divides.empty:
            raise ValueError(
                f"Duplicate divides still found in {domain1} crosswalk after resolving nested gages: {dup_divides}"
            )

        # check to see if all calibration gages in gages_file are included in the crosswalk
        gages1 = df1["gage_id"].unique().tolist()
        gages_nwm4 = (
            df_gages[df_gages["domain"] == domain1]["gage_id"].unique().tolist()
        )
        gages_missed = [g1 for g1 in gages_nwm4 if g1 not in gages1]
        gages_extra = [g1 for g1 in gages1 if g1 not in gages_nwm4]

        if gages_extra:
            print(f"Extra basins found in crosswalk for {domain1}: {gages_extra}")
        if gages_missed:
            print(
                f"Number of missing calibration basins in crosswalk for {domain1}: {len(gages_missed)}"
            )
            gages_missed = (
                gages_missed if len(gages_missed) <= 10 else gages_missed[:10]
            )
            print(
                f"First {len(gages_missed)} missing calibration basins in crosswalk for {domain1}: {gages_missed}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Build crosswalk parquet files for NWM calibration gages."
    )
    parser.add_argument(
        "--domains",
        nargs="+",
        choices=["conus", "ak", "hi", "prvi"],
        default=["conus", "ak", "hi", "prvi"],
        help="Domains to process (default: all).",
    )

    parser.add_argument(
        "--input-dir",
        required=True,
        type=Path,
        help="Base directory containing domain subfolders with gpkg files.",
    )
    parser.add_argument(
        "--outdir",
        required=True,
        type=Path,
        help="Output directory for crosswalk parquet files.",
    )
    parser.add_argument(
        "--gages-file",
        required=True,
        type=Path,
        help="CSV file listing NWMv4 calibration gages.",
    )
    parser.add_argument(
        "--nested-gages",
        choices=["inner", "outer"],
        default="inner",
        help="How to resolve nested gages (default: inner).",
    )
    parser.add_argument(
        "--hf-version",
        choices=["nhf", "v2.2"],
        default="nhf",
        help="Version of the hydrofabric GPKG files (default: nhf).",
    )

    args = parser.parse_args()
    build_crosswalks(
        args.domains,
        args.input_dir,
        args.outdir,
        args.gages_file,
        args.nested_gages,
        args.hf_version,
    )


if __name__ == "__main__":
    main()
