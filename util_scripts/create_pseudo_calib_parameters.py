"""Script to create pseudo calibration parameter sets by randomly sampling within given bounds."""

import os
from pathlib import Path

import numpy as np
import pandas as pd


def load_bounds(module: str, bounds_dir: str | Path) -> pd.DataFrame:
    """Load parameter bounds for a given module.

    Works for tab- or comma-delimited. Expected file name: calib_params_<module>.csv/tsv
    """
    bounds_dir = Path(bounds_dir)
    file_csv = bounds_dir / f"calib_params_{module}.csv"
    file_tsv = bounds_dir / f"calib_params_{module}.tsv"

    if file_csv.exists():
        return pd.read_csv(file_csv, sep=None, engine="python")
    elif file_tsv.exists():
        return pd.read_csv(file_tsv, sep=None, engine="python")
    else:
        raise FileNotFoundError(f"No bounds file found for module: {module}")


def generate_param_samples(bounds: pd.DataFrame) -> dict:
    """Randomly sample one value for each parameter in bounds."""
    sampled = {}
    for _, row in bounds.iterrows():
        sampled[row["param"]] = np.random.uniform(row["min"], row["max"])
    return sampled


def process_domain(
    domain: str,
    bounds_dir: str | Path,
    in_dir: str | Path,
    out_dir: str | Path,
    file_ext: str = ".parquet",
):
    """Process a single domain parquet file and generate sampled parameter sets."""
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)
    infile = in_dir / f"stat_calval_all_{domain}.parquet"
    outfile = out_dir / f"sampled_params_{domain}{file_ext}"

    # Load input parquet file
    df = pd.read_parquet(infile)

    # Get unique gage_id + formulation pairs
    unique_pairs = df[["gage_id", "formulation"]].drop_duplicates()

    results = []
    for _, row in unique_pairs.iterrows():
        gage_id = row["gage_id"]
        formulation = row["formulation"]

        # Each formulation may contain multiple modules
        modules = formulation.split()
        sampled_params = {}
        for module in modules:
            if module.lower() == "t-route":
                continue  # skip t-route, no parameters to sample
            try:
                module_bounds = load_bounds(module, bounds_dir)
                sampled_params.update(generate_param_samples(module_bounds))
            except FileNotFoundError:
                print(f"No bounds file for module '{module}', skipping.")

        results.append(
            {"gage_id": gage_id, "formulation": formulation, **sampled_params}
        )

    # Save to parquet
    result_df = pd.DataFrame(results)
    if file_ext == ".csv":
        result_df.to_csv(outfile.with_suffix(".csv"), index=False)
    elif file_ext == ".parquet":
        result_df.to_parquet(outfile, index=False)
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

    print(f"Saved {len(result_df)} parameter sets to {outfile}")


if __name__ == "__main__":
    # domains = ["conus", "ak", "hi", "prvi"]
    domains = ["conus"]  # for testing
    bounds_dir = Path("~/data/calib_params_tab_delimited").expanduser()
    data_dir = Path("~/repos/nwm-region-mgr/data/inputs/region/").expanduser()
    in_dir = data_dir / "calval_stats"
    out_dir = data_dir / "pseudo_calib_params"
    file_ext = ".csv"  # output file extension: .csv or .parquet

    os.makedirs(out_dir, exist_ok=True)

    for domain in domains:
        process_domain(domain, bounds_dir, in_dir, out_dir, file_ext)
