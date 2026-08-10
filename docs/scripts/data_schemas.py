"""Generate RST files with schema tables for input and output data files.

Based on sample files on S3 and description CSVs in the docs folder. This script reads sample file paths
 from the description CSVs, loads the sample files (csv, parquet, gpkg/gdb) from S3, extracts the schema and
 a preview of the data, and writes it to RST files for documentation.

The generated RST files are saved in the `docs/source/tech_reference` directory:
    i.e., `input_data.rst` and `output_data.rst`.

To add a new file schema to the documentation:
1. Upload a sample file to S3 and get the path.
2. Add a description CSV in `docs/scripts/data_desc/inputs` or `docs/scripts/data_desc/outputs`
with a `sample_file_path` entry pointing to the sample file on S3.
3. Run this script to regenerate the RST files with the new schema included. Prior to running, ensure your AWS
credentials are up to date in the `.env` file or environment variables for S3 access.
"""

import os
import re
import tempfile
from io import BytesIO
from pathlib import Path
from pprint import pprint

import boto3
import fiona
import geopandas as gpd
import pandas as pd
import yaml
from dotenv import load_dotenv

S3_DATA_DIR = "regionalization/data"
INPUT_DATA_DIR = S3_DATA_DIR + "/inputs/region"
OUTPUT_DATA_DIR = S3_DATA_DIR + "/sample_outputs/test"

DATA_DESC_DIR = "docs/scripts/data_desc"
OUTPUT_DESC_DIR = DATA_DESC_DIR + "/outputs"
INPUT_DESC_DIR = DATA_DESC_DIR + "/inputs"

OUT_PATH = "docs/source/tech_reference"
INPUT_DATA_FILE = OUT_PATH + "/input_data.rst"
OUTPUT_DATA_FILE = OUT_PATH + "/output_data.rst"


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


def get_sample_data_files(base_dir: Path, desc_dir: Path) -> dict[str, str]:
    """Return a dictionary of sample input and output file paths on S3."""
    # get list of all files in the data description directory
    desc_files = list(Path(desc_dir).glob("*.csv"))

    # create a mapping of file stem to sample file path from the description files
    file_dict = {}
    for f in desc_files:
        df = pd.read_csv(f, delimiter="|", index_col=False, header=None)
        if "sample_file_path" in df[0].values:
            sample_path = df[df[0] == "sample_file_path"][1].values[0]
            sample_path = sample_path.replace("inputs/region/", "")
            sample_path = sample_path.replace("outputs/region/", "")
            file_dict[Path(f).stem] = base_dir / sample_path
        else:
            print(f"Warning: no sample_file_path found in description file {f}")

    return file_dict


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

    # read table and column descriptions if the description file is available in either input or output desc dir
    files = list(Path(INPUT_DESC_DIR).glob("*.csv")) + list(
        Path(OUTPUT_DESC_DIR).glob("*.csv")
    )
    files = [f for f in files if f.stem.lower() in title.lower()]

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
        sample_path = desc_df[desc_df[0] == "sample_file_path"][1].values[0].strip()
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

    for col, dtype in df.dtypes.items():
        if desc_df is not None and col in desc_df[0].values:
            col_desc = desc_df[desc_df[0] == col][1].values[0]
        else:
            col_desc = col

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
    df = pd.DataFrame()

    # skip spatial_distance output files (too large)
    if "spatial_distance" in title:
        return schema_to_rst(df, title)

    ext = os.path.splitext(path)[1].lower().strip()
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
            response = s3_client.get_object(Bucket=bucket, Key=str(path).strip())
            if ext == ".csv":
                df = pd.read_csv(
                    BytesIO(response["Body"].read()),
                    nrows=1000,
                    dtype={
                        "gage_id": str,
                        "donor_gage_id": str,
                        "receiver_gage_id": str,
                    },
                )
            elif ext == ".parquet":
                df = pd.read_parquet(BytesIO(response["Body"].read()), engine="pyarrow")
            elif ext in [".gpkg", ".gdb"]:
                if gpd is None:
                    raise RuntimeError("geopandas required for GPKG/GDB")
                # Write S3 content to temporary file
                with tempfile.NamedTemporaryFile(suffix=ext) as tmp_file:
                    tmp_file.write(response["Body"].read())
                    tmp_file.flush()  # ensure data is written
                    layers = fiona.listlayers(tmp_file.name)
                    rst_blocks = []
                    for layer in layers:
                        gdf = gpd.read_file(tmp_file.name, layer=layer, rows=1000)
                        rst_blocks.append(
                            schema_to_rst(gdf, f"{title} (layer: {layer})")
                        )
                    return "\n\n".join(rst_blocks)
            else:
                print(
                    f"ERROR: Unsupported file type for schema extraction: {ext} in file {path}"
                )
                return
    except Exception as e:
        print(f"ERROR reading {path}: {e}")

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


def process_schema(
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
    s3_client = initialize_s3_client()
    input_files = get_sample_data_files(Path(INPUT_DATA_DIR), Path(INPUT_DESC_DIR))
    print("============ Creating schemas for input files ============")
    pprint(input_files)
    process_schema(
        dict(sorted(input_files.items())), INPUT_DATA_FILE, s3_client=s3_client
    )

    # process output data schemas
    output_files = get_sample_data_files(Path(OUTPUT_DATA_DIR), Path(OUTPUT_DESC_DIR))
    print("\n============ Creating schemas for output files ============")
    pprint(output_files)
    process_schema(
        dict(sorted(output_files.items())),
        OUTPUT_DATA_FILE,
        s3_client=s3_client,
    )
