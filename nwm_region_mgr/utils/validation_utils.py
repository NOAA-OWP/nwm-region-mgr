"""Define utilities and/or help functions for validation.

validation_utils.py

Functions:
    - check_columns_dataframe: Check if the required columns are present in a DataFrame (CSV or Parquet).
    - check_columns_hydrofabric: Check if the required fields are present in a hydrofabric file (GeoPackage or Shapefile).
    - check_options: Check if the provided option is valid against a list of valid options.

"""

import logging
from pathlib import Path
from typing import Set

import fiona
import pandas as pd
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)


def check_columns_dataframe(
    file: Path | str, columns: Set[str], case_sensitive: bool = True
):
    """Check if the required columns are present in the file.

    Args:
        file: Path to the CSV or Parquet file.
        columns: Set of required column names.
        case_sensitive: Whether to check column names in a case-sensitive manner (default: True).

    Raises:
        ValueError: If any of the required columns are missing in the file.

    """
    if isinstance(file, str):
        file = Path(file)

    if not file.exists():
        msg = f"File not found: {file}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    suffix = file.suffix.lower()
    if suffix == ".csv":
        # Read full DataFrame with minimal memory usage
        df = pd.read_csv(file)
        columns_present = [col.strip() for col in df.columns]
        is_empty = df.empty

    elif suffix == ".parquet":
        pf = pq.ParquetFile(file)
        columns_present = [col.strip() for col in pf.schema.names]
        is_empty = pf.metadata.num_rows == 0  # More efficient than loading into pandas

    else:
        msg = f"Unsupported file format: {suffix}. Supported formats are .csv and .parquet."
        logger.error(msg)
        raise ValueError(msg)

    # raise error if the file is empty
    if is_empty:
        msg = f"The file {file} is empty. Please provide a file with data."
        logger.error(msg)
        raise ValueError(msg)

    # Normalize only if case-insensitive
    if case_sensitive:
        required = {col.strip() for col in columns}
        present = set(columns_present)
    else:
        required = {col.strip().lower() for col in columns}
        present = {col.lower() for col in columns_present}

    # check for missing columns
    missing_cols = required - present
    if missing_cols:
        mode = "case sensitive" if case_sensitive else "case insensitive"
        msg = (
            f"Missing columns ({mode}) in {file}: {missing_cols}. "
            f"Available columns: {columns_present}"
        )
        logger.error(msg)
        raise ValueError(msg)


def check_columns_hydrofabric(
    hydro_file: str | Path,
    required_fields: list[str],
    layer_name: str = None,
    case_sensitive: bool = True,
) -> str:
    """Check if the required fields are present in the hydrofabric file.

    Args:
        hydro_file: Path to the hydrofabric file (GeoPackage or Shapefile).
        required_fields: List of required fields to check.
        layer_name: Optional layer name for GeoPackage or Geodatabase files.
        case_sensitive: Whether to check field names in a case-sensitive manner (default: True).

    Returns:
        str: The layer name used for the hydrofabric file.

    """
    # get the file suffix
    if isinstance(hydro_file, str):
        hydro_file = Path(hydro_file)
    suffix = hydro_file.suffix.lower()

    # check if the file format is supported
    if suffix not in (".gpkg", ".shp", ".gdb"):
        msg = f"Unsupported hydrofabric file format: {suffix}. Supported formats are .gpkg, .shp, and .gdb."
        logger.error(msg)
        raise ValueError(msg)

    # Determine if layer is needed
    use_layer = suffix in (".gpkg", ".gdb")

    # Automatically select layer if needed and not provided
    if use_layer and layer_name is None:
        layers = fiona.listlayers(hydro_file)
        if len(layers) == 1:
            layer_name = layers[0]
        else:
            raise ValueError(
                f"Multiple layers found in {hydro_file}. Please specify a layer: {layers}"
            )

    # Open with or without layer
    open_kwargs = {"layer": layer_name} if use_layer else {}

    def _normalize(value: str, case_sensitive: bool) -> str:
        return value if case_sensitive else value.lower()

    with fiona.open(hydro_file, **open_kwargs) as src:
        raw_fields = list(src.schema["properties"].keys())
        has_geometry = src.schema.get("geometry") is not None

        schema_fields = {_normalize(f, case_sensitive) for f in raw_fields}

        missing = []
        for field in required_fields:
            norm_field = _normalize(field, case_sensitive)

            # Special handling for geometry
            if norm_field == _normalize("geometry", case_sensitive):
                if not has_geometry:
                    missing.append(field)
            elif norm_field not in schema_fields:
                missing.append(field)

    if missing:
        mode = "case sensitive" if case_sensitive else "case insensitive"
        msg = f"Missing required fields ({mode}) in {hydro_file}: {missing}. Available fields: {schema_fields}"
        logger.error(msg)
        raise ValueError(msg)

    return layer_name


def check_options(options: str | list[str], valid_options: list[str], var: str):
    """Check if the provided options are valid against a list of valid options."""
    if isinstance(options, str):
        options = [options]

    options_unsupported = set(options) - set(valid_options)
    if options_unsupported:
        raise ValueError(
            f"Unsupported options for {var}: {options_unsupported}. Valid options are: {valid_options}"
        )
