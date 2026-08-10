import argparse
from pathlib import Path

import pandas as pd


def gather_streamcat_attrs():
    """Gather StreamCat attributes for NextGen catchments.

    Args:
        streamcat_dir: Directory containing StreamCat attribute files.
        ngen_divides_file: File path to NextGen catchment divides shapefile.
        attr_list: List of StreamCat attributes to gather.
        output_file: Output file path for the processed attributes.

    """
    # Streamcat metrics metadata
    streamcat_dir = Path("~/data/streamcat/").expanduser()
    file_metrics = streamcat_dir / "StreamCatMetrics.csv"
    df_metrics = pd.read_csv(file_metrics, encoding="latin1")

    # check which streamcat attribute files exist in the lynker directory
    tables = df_metrics["final_table"].unique().tolist()
    files = [
        streamcat_dir / "lynker" / f"streamcat_{table}_cat.parquet" for table in tables
    ]
    existing_files = [f for f in files if f.is_file()]

    # loop through each existing file and gather attributes
    df_list = []
    df_metric_desc = pd.DataFrame()
    for file in existing_files:
        print(f"Processing StreamCat attribute file: {file}")
        df_attr = pd.read_parquet(file)

        # get required attributes and descriptions from df_metrics
        table_name = file.stem.replace("streamcat_", "").replace("_cat", "")
        df_metric_table = df_metrics[df_metrics["final_table"] == table_name][
            ["metric_name", "metric_description"]
        ]
        df_metric_table["attr"] = df_metric_table["metric_name"]

        # remove "[AOI]" suffix if present in attr names
        df_metric_table["attr"] = df_metric_table["attr"].str.replace(
            "[AOI]", "", regex=False
        )

        # remove "8110" prefix if present
        df_metric_table["attr"] = df_metric_table["attr"].str.replace(
            "8110", "", regex=False
        )

        # remove "[Year]" suffix if present
        df_metric_table["attr"] = df_metric_table["attr"].str.replace(
            "[Year]", "", regex=False
        )

        # add "Cat" suffix to attr names in df_attr
        df_metric_table["attr"] = df_metric_table["attr"] + "Cat"

        attrs_needed = df_metric_table["attr"].tolist()
        print(f"Attributes needed from {file.name}: {attrs_needed}")
        # check if attributes exist in df_attr
        missing_attrs = [attr for attr in attrs_needed if attr not in df_attr.columns]
        if missing_attrs:
            print(
                f"Warning: The following attributes are missing in {file.name}: {missing_attrs}. "
                f"Skipping these attributes."
            )

            # use attributes that exist in df_attr
            attrs_needed = [attr for attr in attrs_needed if attr in df_attr.columns]
            df_metric_table = df_metric_table[
                df_metric_table["attr"].isin(attrs_needed)
            ]

        if not attrs_needed:
            print(f"No valid attributes found in {file.name}. Skipping this file.")
            continue

        df_attr = df_attr[["COMID"] + attrs_needed]
        df_list.append(df_attr)

        # remove "Cat" suffix for description mapping
        df_metric_table["attr"] = df_metric_table["attr"].str.replace(
            "Cat", "", regex=False
        )
        df_metric_desc = pd.concat([df_metric_desc, df_metric_table], ignore_index=True)

    return df_list, df_metric_desc


def process_streamcat_attrs(df_list):
    """Process StreamCat attributes and merge with NextGen catchments.

    Args:
        df_list: List of DataFrames containing StreamCat attributes.

    """
    # merge all attribute dataframes on COMID
    df_attrs = df_list[0]
    for df in df_list[1:]:
        df_attrs = df_attrs.merge(df, on="COMID", how="outer")

    # remove "Cat" suffix from column names
    df_attrs.columns = [col.replace("Cat", "") for col in df_attrs.columns]

    # rename COMID to be consistent with crosswalk
    df_attrs.rename(columns={"COMID": "FEATUREID"}, inplace=True)

    return df_attrs


def process_streamcat_attr_descriptions(df_metric_desc: pd.DataFrame, output_dir: Path):
    """Process StreamCat attribute descriptions for selection configuration.

    Args:
        df_metric_desc: DataFrame containing StreamCat attribute descriptions.
        output_dir: Directory to save the processed attribute descriptions.

    Returns:
        Processed DataFrame of attribute descriptions.

    """
    # remove metric_name column from df_metric_desc
    df_metric_desc = df_metric_desc.drop(columns=["metric_name"])

    # rename columns
    df_metric_desc = df_metric_desc.rename(
        columns={"attr": "attr_name", "metric_description": "description"}
    )

    # replace "AOI" with "catchment" in descriptions
    df_metric_desc["description"] = df_metric_desc["description"].str.replace(
        "AOI", "catchment", regex=False
    )

    # add select column (set to 1 for all attributes)
    df_metric_desc["select"] = 1

    # rearrange columns
    df_metric_desc = df_metric_desc[["select", "attr_name", "description"]]

    # save processed attributes and descriptions
    output_dir = Path(output_dir / "attr_config").expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_attrs = output_dir / "attr_selection_streamcat.csv"
    df_metric_desc.to_csv(output_file_attrs, index=False)
    print(f"Saved StreamCat attribute descriptions to {output_file_attrs}")

    return df_metric_desc


def compute_weighted_attrs(
    df_attrs: pd.DataFrame,
    attrs: list,
    id_col: str,
    output_dir: Path | str,
    domain: str,
    cwt_path: Path | str,
):
    """Compute area-weighted StreamCat attributes for NextGen catchments.

    Args:
        df_attrs: DataFrame containing StreamCat attributes.
        attrs: List of StreamCat attributes to process.
        id_col: Column name for catchment ID in attribute dataset.
        output_dir: Output directory to save processed attributes.
        domain: Domain to process StreamCat attributes for.
        cwt_path: Directory containing crosswalk files for StreamCat attributes.

    """
    # ngen-streamcat crosswalk file
    attr_dataset = "streamcat"
    cwt_file = Path(cwt_path, "cwt_ngen_streamcat_" + domain + ".parquet")

    # read the crosswalk file
    df_cwt = pd.read_parquet(cwt_file)

    # remove rows where no overlapping subbasin were found (hence the nearest subbasins were identified instead; not used here)
    df_cwt = df_cwt[df_cwt["nearest_dist_m"].isna()]

    # merge attributes dataset with crosswalk
    df_attrs1 = df_attrs.merge(df_cwt, on=id_col, how="outer")

    # Multiply attribute values by weights (overlap percentage)
    weighted = df_attrs1[attrs].multiply(df_attrs1["overlap_percentage"], axis=0)
    weighted["divide_id"] = df_attrs1["divide_id"]

    # Group by catchment and compute sum
    weighted_sum = weighted.groupby("divide_id").sum(
        min_count=1
    )  # min_count=1 to avoid summing to 0 when all values are NaN

    # Divide by sum of weights per group to get weighted mean
    sum_weights = df_attrs1.groupby("divide_id")["overlap_percentage"].sum()
    weighted_mean = weighted_sum[attrs].div(sum_weights, axis=0).reset_index()

    # save attr data to parquet file
    outfile = Path(
        output_dir,
        "attr_datasets",
        attr_dataset,
        "attr_" + attr_dataset + "_" + domain + ".parquet",
    )
    weighted_mean.to_parquet(outfile, engine="pyarrow")
    print(f"Saved processed StreamCat attributes to {outfile}")


if __name__ == "__main__":
    """Main function to process StreamCat attributes for NextGen catchments."""
    parser = argparse.ArgumentParser(
        description="Process StreamCat attributes for NextGen catchments."
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="conus",
        help="Domain to process StreamCat attributes for.",
    )
    parser.add_argument(
        "--cwt_dir",
        type=str,
        default="~/data/crosswalks/cwt_ngen_streamcat/",
        help="Directory containing crosswalk files for StreamCat attributes.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="~/repos/nwm-region-mgr/data/inputs/region",
        help="Output directory for processed attributes and descriptions.",
    )
    args = parser.parse_args()

    # gather raw StreamCat attributes
    df_list, df_metric_desc = gather_streamcat_attrs()

    # process raw StreamCat attributes
    df_attrs = process_streamcat_attrs(df_list)

    # process StreamCat attribute descriptions
    df_metric_desc = process_streamcat_attr_descriptions(
        df_metric_desc, Path(args.output_dir)
    )

    # compute weighted attributes
    attrs = df_metric_desc["attr_name"].unique().tolist()
    id_col = "FEATUREID"
    compute_weighted_attrs(
        df_attrs,
        attrs,
        id_col,
        Path(args.output_dir).expanduser(),
        args.domain,
        Path(args.cwt_dir).expanduser(),
    )
