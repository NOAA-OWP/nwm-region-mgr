import os

import fiona
import geopandas as gpd
import pandas as pd
import yaml

CONFIG_DIR = "sample_files/configs"
OUT_PATH = "docs/source/tech_reference/input_data.rst"


def schema_to_rst(df: pd.DataFrame, title: str) -> str:
    """Convert a pandas DataFrame schema to an RST list-table."""
    lines = []
    lines.append(f"{title}")
    lines.append("-" * len(title))
    lines.append("")
    lines.append(".. list-table::")
    lines.append("   :header-rows: 1\n")
    lines.append("   * - Column\n     - Type\n     - Nullable")

    nullables = df.isnull().any().to_dict() if len(df) > 0 else {c: "unknown" for c in df.columns}

    for col, dtype in df.dtypes.items():
        lines.append(f"   * - {col}\n" f"     - {dtype}\n" f"     - {nullables[col]}\n")

    lines.append("")
    return "\n".join(lines)


def process_file(title: str, path: str) -> str:
    """Load a file (csv, parquet, gpkg, gdb) and return an RST schema string."""
    ext = os.path.splitext(path)[1].lower()
    try:
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


def main(yaml_files, output_rst):
    all_schemas = ["Schemas", "=======", ""]
    all_config = {}
    for yaml_path in yaml_files:
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        all_config = all_config | config

    path_dict = unpack_dict(all_config)
    for k, v in path_dict.items():
        v = v.replace("{domain}", all_config["general"]["domain"])
        v = v.replace("{run_name}", all_config["general"]["run_name"])
        v = v.replace("{base_dir}", all_config["general"]["base_dir"])
        v = v.replace("{vpu_list}", all_config["general"]["vpu_list"][0])
        print(v)
        if not os.path.exists(v):
            continue
        schema = process_file(k, v)
        if schema is not None:
            all_schemas.append(schema)
            all_schemas.append("\n")
    all_schemas.append(".. toctree::\n   :maxdepth: 2")
    with open(output_rst, "w") as f:
        f.write("\n".join(all_schemas))


if __name__ == "__main__":
    yaml_files = [os.path.join(CONFIG_DIR, i) for i in os.listdir(CONFIG_DIR)]
    main(yaml_files, OUT_PATH)
