"""Script to add modules to formulation column in stats and params files.

Also renames columns in stats files to match ngenCERF format and adds random calibration_run_id and validation_run_id columns.
"""

from pathlib import Path

import numpy as np
import pandas as pd

stat_dir = Path("../data/inputs/region/calval_stats")
param_dir = Path("../data/inputs/region/pseudo_calib_params")

stat_file_pattern = "stat_calval_all"
param_file_pattern = "sampled_params"

column_name = "formulation"
modules = ("cfe-s", "cfe-x")
insert_modules = ["smp", "sft"]

domains = ["conus", "ak", "hi", "prvi"]


def update_formulation(df: pd.DataFrame) -> pd.DataFrame:
    """Insert modules after specified modules in the formulation column."""
    if column_name not in df.columns:
        print(f"Skipping file (no '{column_name}' column)")
        return df

    def insert_module(val: str) -> str:
        if pd.isna(val):
            return val

        parts = val.split()

        i = 0
        while i < len(parts):
            if parts[i].lower() in modules:
                # avoid duplicate insertion
                if parts[i + 1 : i + 3] == insert_modules:
                    i += 1
                    continue

                parts[i + 1 : i + 1] = insert_modules  # insert both modules
                i += 3  # skip past inserted modules
            else:
                i += 1

        return " ".join(parts)

    mask = df[column_name].str.contains(
        "|".join(modules),
        case=False,
        na=False,
        regex=True,
    )

    df.loc[mask, column_name] = df.loc[mask, column_name].apply(insert_module)

    return df


def rename_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:  # Mapping of old column names to new column names
    column_name_map = {
        "csi": "CSI",
        "cor": "Corr",
        "event_volume_bias": "EVBIAS",
        "far": "FAR",
        "kge": "KGE",
        "nse": "NSE",
        "nselog": "NSELog",
        "nseWt": "NSEWt",
        "bias": "PBIAS",
        "peak_bias": "PKBIAS",
        "peak_tm_err_hr": "PKTE",
        "pod": "POD",
        "rmse": "RMSE",
    }

    # Rename columns
    df = df.rename(columns=column_name_map)

    # columns to keep
    cols_to_keep = ["formulation", "gage_id", "evalPeriod"] + list(
        column_name_map.values()
    )
    df = df[cols_to_keep]

    return df


def add_job_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Add random calibration_run_id and validation_run_id columns to the dataframe."""
    n_rows = len(df)
    df["calibration_run_id"] = np.random.randint(10000, 100000, size=n_rows)
    df["validation_run_id"] = np.random.randint(10000, 100000, size=n_rows)

    # Move the two columns to the front
    front_cols = ["calibration_run_id", "validation_run_id"]
    df = df[front_cols + [col for col in df.columns if col not in front_cols]]

    return df


def process_files(
    directory: Path,
    file_pattern: str,
    extension: str,
    extension_new: str,
    type_str: str,
):
    """Process files in the specified directory matching the pattern and extension."""
    for domain in domains:
        file = Path(f"{directory}.old") / f"{file_pattern}_{domain}.{extension}"

        if not file.exists():
            print(f"Skipping missing file: {file}")
            continue

        print(f"Processing {extension.upper()}: {file.name}")

        # read
        if extension == "parquet":
            df = pd.read_parquet(file)
        elif extension == "csv":
            df = pd.read_csv(file)
        else:
            raise ValueError(f"Unsupported extension: {extension}")

        # replace formulation
        df = update_formulation(df)

        # rename columns
        if type_str == "stats":
            df = rename_columns(df)

        # add job ids
        df = add_job_ids(df)

        # loop through columns and convert to -9999 to NaN
        df = df.replace(-9999, np.nan)

        # write
        out_file = directory / f"{file_pattern}_{domain}.{extension_new}"

        if extension_new == "parquet":
            df.to_parquet(out_file, index=False)
        elif extension_new == "csv":
            df.to_csv(out_file, index=False)


if __name__ == "__main__":
    """Add modules to formulation column in stats and params files."""
    # stats
    process_files(stat_dir, stat_file_pattern, "parquet", "parquet", "stats")

    # params
    process_files(param_dir, param_file_pattern, "csv", "csv", "params")
