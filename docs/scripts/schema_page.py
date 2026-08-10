import os
import re
from io import BytesIO
from pathlib import Path

import boto3
import fiona
import geopandas as gpd
import pandas as pd
import yaml
from dotenv import load_dotenv

CONFIG_DIR = "configs"

DATA_DESC_DIR = "docs/scripts/data_desc"
OUTPUT_DESC_DIR = DATA_DESC_DIR + "/outputs"
INPUT_DESC_DIR = DATA_DESC_DIR + "/inputs"

OUT_PATH = "docs/source/tech_reference"
OUT_PATH_INPUT_DATA = OUT_PATH + "/input_data.rst"
OUT_PATH_OUTPUT_DATA = OUT_PATH + "/output_data.rst"


def initialize_s3_client():
    """Initialize and return an S3 client using credentials from environment variables."""
    # Load environment variables from .env
    load_dotenv()  # looks for .env in current folder

    # Read AWS credentials from environment
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")  # optional default region
    aws_token = os.getenv("AWS_SESSION_TOKEN")  # session token

    # Initialize S3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
        aws_session_token=aws_token,
    )
    return s3


def get_sample_input_files(yaml_files: list[str]) -> dict[str, str]:
    all_config = {}
    for yaml_path in yaml_files:
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        all_config = deep_merge_keep_both(all_config, config)

    path_dict = unpack_dict(all_config)
    file_dict = {}
    for k, v in path_dict.items():
        v = v.replace("{domain}", all_config["general"]["domain"])
        v = v.replace("{run_name}", all_config["general"]["run_name"])
        v = v.replace("{base_dir}", all_config["general"]["base_dir"])
        v = v.replace("{vpu_list}", all_config["general"]["vpu_list"][0])

        if not os.path.exists(v) or not os.path.isfile(v):
            continue
        if "output" in k.lower():
            continue
        file_dict[k] = v
    return file_dict


def get_sample_output_files() -> dict[str, str]:
    """Return a dictionary of sample output file paths on S3 for different output types."""
    base_dir = Path("regionalization/data/sample_outputs/test")
    vpu = "03S"
    outputs = {
        "attr_data_final": base_dir
        / "attr_data_final"
        / f"attr_conus_vpu{vpu}.parquet",
        "formulations": base_dir / "formulations" / f"form_conus_vpu{vpu}.parquet",
        "formulations_pars": base_dir
        / "formulations"
        / f"form_conus_vpu{vpu}_pars.parquet",
        "pairs_distance_algorithms": base_dir
        / "pairs"
        / f"pairs_gower_conus_vpu{vpu}.parquet",
        "pairs_cluster_algorithms": base_dir
        / "pairs"
        / f"pairs_kmeans_conus_vpu{vpu}.parquet",
        "pairs_mswm": base_dir / "pairs" / f"pairs_kmeans_conus_vpu{vpu}_mswm.csv",
        "params": base_dir / "params" / f"formulation_params_gower_conus_vpu{vpu}.csv",
        "spatial_distance": base_dir
        / "spatial_distance"
        / f"donor_receiver_dist_conus_vpu{vpu}.parquet",
        "summary_score": base_dir / "summary_score" / f"score_conus_vpu{vpu}.parquet",
    }

    return outputs


def make_anchor(title: str) -> str:
    """Convert title to a safe RST anchor ID."""
    anchor = title.strip().lower()
    anchor = re.sub(r"[^\w\-]+", "-", anchor)  # replace non-alphanumerics
    anchor = re.sub(r"-+", "-", anchor).strip("-")
    return anchor


def schema_to_rst(df: pd.DataFrame, title: str, preview_rows: int = 3) -> str:
    """Convert a pandas DataFrame schema to an RST list-table."""
    lines = []
    description = ""
    desc_df = None

    # determine whether it is an input or output data file
    is_output = title in get_sample_output_files().keys()

    # read table and column descriptions if the description file is available in either input or output desc dir
    files = list(Path(INPUT_DESC_DIR).glob("*.csv")) + list(
        Path(OUTPUT_DESC_DIR).glob("*.csv")
    )
    file_stem = title.lower().replace(" ", "_").split(".")[-1]
    files = [f for f in files if f.stem.lower() in file_stem]
    if len(files) > 0:
        desc_file = files[0]
        with open(desc_file, "r") as f:
            desc_df = pd.read_csv(f, delimiter="|", index_col=False, header=None)

    # insert anchor for linking from the plots page
    anchor = make_anchor(title)
    lines.append(f".. _{anchor}:")
    lines.append("")

    # Title
    lines.append(f"{title}")
    lines.append("-" * len(title))
    lines.append("")

    # Optional description
    if desc_df is not None and "title" in desc_df[0].values:
        description = desc_df[desc_df[0] == "title"][1].values[0]
    if desc_df is not None and "sample_file_path" in desc_df[0].values:
        sample_path = desc_df[desc_df[0] == "sample_file_path"][1].values[0]
        description += f"\n\nSample file path: ``{sample_path}``"
    if description:
        lines.append(description)
        lines.append("")

    # skip table if title = spatial_distance (too large)
    if "spatial_distance" in title:
        lines.append(
            ".. warning:: Schema table omitted for spatial_distance files due to large number of columns."
        )
        lines.append("")
        return "\n".join(lines)

    # Insert preview of first few rows
    if not df.empty:
        preview_df = df.head(preview_rows)

        # drop geometry column if exists
        dropped_geom = False
        if "geometry" in preview_df.columns:
            preview_df = preview_df.drop(columns=["geometry"])
            dropped_geom = True

        if dropped_geom:
            lines.append(
                ".. note:: Geometry column omitted from preview table for brevity."
            )
            lines.append("")

        lines.append("**Example rows:**")
        lines.append("")
        lines.append(".. csv-table::")
        lines.append("   :header-rows: 1")
        lines.append("")

        # Header
        lines.append("   " + ", ".join(f'"{c}"' for c in preview_df.columns))
        # Rows
        for _, row in preview_df.iterrows():
            lines.append("   " + ", ".join(f'"{v}"' for v in row.values))
        lines.append("")

    # Table header
    lines.append("**Schema:**")
    lines.append("")
    lines.append(".. list-table::")
    lines.append("   :header-rows: 1\n")
    lines.append("   * - Column")
    lines.append("     - Description")
    lines.append("     - Type")
    # if not is_output:
    #     lines.append("     - Nullable")

    # nullables = (
    #     df.isnull().any().to_dict()
    #     if len(df) > 0
    #     else {c: "unknown" for c in df.columns}
    # )

    for col, dtype in df.dtypes.items():
        if desc_df is not None and col in desc_df[0].values:
            col_desc = desc_df[desc_df[0] == col][1].values[0]
        else:
            col_desc = col

        # not using nullable info for now
        # lines.append(
        #    f"   * - {col}\n     - {col_desc}\n     - {dtype}\n     - {nullables[col]}\n"

        lines.append(f"   * - {col}\n     - {col_desc}\n     - {dtype}\n")

    lines.append("")
    return "\n".join(lines)


def process_file(
    title: str,
    path: str,
    s3_client=None,
    bucket: str = "ngwpc-dev",
) -> str:
    """Load a file (csv, parquet, gpkg, gdb) and return an RST schema string."""
    # skip spatial_distance output files (too large)
    if "spatial_distance" in title:
        df = pd.DataFrame()
        return schema_to_rst(df, title)

    ext = os.path.splitext(path)[1].lower()
    try:
        if s3_client is None:
            if ext == ".csv":
                df = pd.read_csv(path, nrows=1000)  # sample for speed
            elif ext == ".parquet":
                df = pd.read_parquet(path, engine="pyarrow")
            elif ext in [".gpkg", ".gdb"]:
                if gpd is None:
                    raise RuntimeError("geopandas required for GPKG/GDB")
                layers = fiona.listlayers(path)
                rst_blocks = []
                for layer in layers:
                    gdf = gpd.read_file(path, layer=layer, rows=1000)
                    rst_blocks.append(schema_to_rst(gdf, f"{title} (layer: {layer})"))
                return "\n\n".join(rst_blocks)
            else:
                return
        else:
            response = s3_client.get_object(Bucket=bucket, Key=str(path))
            if ext == ".csv":
                df = pd.read_csv(BytesIO(response["Body"].read()), nrows=1000)
            elif ext == ".parquet":
                df = pd.read_parquet(BytesIO(response["Body"].read()), engine="pyarrow")
            else:
                return
    except Exception as e:
        return f".. warning:: Failed to read {path} ({e})"

    return schema_to_rst(df, title)


def unpack_dict(d: dict, root: str = "") -> list[str]:
    if len(root) > 0:
        root += "."
    out = {}
    for k, v in d.items():
        if isinstance(v, str):
            out[root + k] = v
        if isinstance(v, list):
            if isinstance(v[0], str):
                out[root + k] = v[0]
        if isinstance(v, dict):
            out = out | unpack_dict(v, root + k)
    return out


def deep_merge_keep_both(d1, d2):
    merged = dict(d1)
    for k, v in d2.items():
        if k not in merged:
            merged[k] = v
        else:
            if isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = deep_merge_keep_both(merged[k], v)
            else:
                # conflict → keep both in list
                if not isinstance(merged[k], list):
                    merged[k] = [merged[k]]
                merged[k].append(v)
    return merged


def main(
    file_dict: dict[str, str],
    output_rst,
    s3_client=None,
):
    all_schemas = ["Schemas", "=======", ""]

    for k, v in file_dict.items():
        schema = process_file(k, v, s3_client=s3_client)
        if schema is not None:
            all_schemas.append(schema)
            all_schemas.append("\n")
    all_schemas.append(".. toctree::\n   :maxdepth: 2")
    with open(output_rst, "w") as f:
        f.write("\n".join(all_schemas))


if __name__ == "__main__":
    # process input data schemas
    yaml_files = list(Path(CONFIG_DIR).glob("*.yaml"))
    yaml_files = [
        f
        for f in yaml_files
        if f.name
        in [
            "config_formreg.yaml",
            "config_parreg.yaml",
            "config_general.yaml",
        ]
    ]  # only process "general", "formreg", "parreg" configs

    main(get_sample_input_files(yaml_files), OUT_PATH_INPUT_DATA, s3_client=None)

    # process output data schemas
    s3_client = initialize_s3_client()
    output_files = get_sample_output_files()
    main(
        output_files,
        OUT_PATH_OUTPUT_DATA,
        s3_client=s3_client,
    )
