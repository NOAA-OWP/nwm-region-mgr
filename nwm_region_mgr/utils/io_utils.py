"""Define utilities and/or help functions for file I/O.

io_utils.py

Functions:
    - save_data: Save data to disk in an appropriate format based on its type and file extension
    - read_table: Read a table from a file, supporting CSV and Parquet formats.

"""

import csv
import logging
from enum import Enum
from pathlib import Path
from typing import Union

import pandas as pd
import yaml
from charset_normalizer import from_path
from pydantic import BaseModel

from nwm_region_mgr.utils.dict_utils import convert_enum_to_value, remove_nulls

logger = logging.getLogger(__name__)

# Module-level cache
_table_cache: dict[Path, pd.DataFrame] = {}
_file_mtime: dict[Path, float] = {}  # track modification times


def save_data(
    data: Union[pd.DataFrame, BaseModel],
    file_path: Union[str, Path],
    index: bool = False,
) -> None:
    """Save data to disk in an appropriate format based on its type and file extension.

    Args:
        data : Union[pandas.DataFrame, pydantic.BaseModel]
            The data object to save. Must be either a pandas DataFrame or a Pydantic BaseModel.

            - If `data` is a pandas DataFrame:
                - Supported file formats: `.csv`, `.parquet`.

            - If `data` is a Pydantic BaseModel:
                - Supported file format: `.yaml`.

        file_path : Union[str, pathlib.Path]
            The target file path where the data will be saved. The file extension determines the format.
        index : bool
            Whether to write row indices in the DataFrame (default: False).

    Raises:
        Exception
            If the file extension is not supported for the given data type.

        ValueError
            If `data` is neither a pandas DataFrame nor a Pydantic BaseModel.

    Notes:
        - If the directory for the specified file path does not exist, it will be created.
        - YAML files for Pydantic models are written with custom inline list formatting (if configured).

    """

    class InlineListDumper(yaml.Dumper):
        pass

    def represent_inline_list(dumper, data):
        return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)

    file_path = Path(file_path)
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.DataFrame):
        if file_path.suffix == ".csv":
            data.to_csv(file_path, index=index)
        elif file_path.suffix == ".parquet":
            data.to_parquet(file_path, index=index)
        else:
            raise Exception(
                "Only csv and parquet formats are supported for saving DataFrame"
            )

    elif isinstance(data, BaseModel):
        if file_path.suffix != ".yaml":
            raise Exception(f"Only yaml format is supported for saving {type(data)}")

        with open(file_path, "w") as f:
            InlineListDumper.add_representer(list, represent_inline_list)
            InlineListDumper.add_representer(
                Enum, lambda dumper, data: dumper.represent_scalar("!enum", data.value)
            )

            # Convert Enum values to their string representation for YAML serialization
            data_dict = convert_enum_to_value(data.model_dump())

            # Remove None values from the data dictionary
            data_dict = remove_nulls(data_dict)

            # Dump the data to YAML file with inline list formatting
            # and without sorting keys to preserve the order of fields
            yaml.dump(
                data_dict,
                f,
                Dumper=InlineListDumper,
                sort_keys=False,
            )

    else:
        raise ValueError(
            "Unsupported data type: must be a pandas DataFrame or Pydantic BaseModel"
        )


def read_table_safely(
    file_path: str,
    quotechar: str = '"',
    escapechar: str = "\\",
    fallback_encodings: list[str] = ["utf-8", "utf-8-sig", "latin1", "cp1252"],
    dtype: dict = None,
) -> pd.DataFrame:
    """Read a delimited text file (CSV/TSV) safely.

    With:  1. Automatic encoding detection.
           2. Automatic delimiter detection.
           3. Optional dtype specification.
           4. Fallback encodings if decoding fails.

    Args:
        file_path : str
            Path to the file.
        quotechar : str
            Character used to quote fields.
        escapechar : str
            Character used to escape quotechar inside quoted fields.
        fallback_encodings : list[str]
            Encodings to try if detection fails.
        dtype : dict, optional
            Column name to dtype mapping (like in pd.read_csv).

    Returns:
        pd.DataFrame
            Loaded DataFrame.

    """
    # Detect encoding
    try:
        detection = from_path(file_path).best()
        detected_encoding = (
            detection.encoding
            if detection and detection.encoding
            else fallback_encodings[0]
        )
        logger.debug(f"Detected encoding: {detected_encoding}")
    except Exception as e:
        logger.debug(f"Encoding detection failed: {e}")
        detected_encoding = fallback_encodings[0]

    # Detect delimiter
    try:
        with open(file_path, "r", encoding=detected_encoding, errors="ignore") as f:
            sample = f.read(2048)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample, delimiters=[",", "\t", ";", "|"])
            delimiter = dialect.delimiter
        logger.debug(f"Detected delimiter: '{delimiter}'")
    except Exception as e:
        logger.debug(f"Delimiter detection failed, defaulting to comma: {e}")
        delimiter = ","

    # Try reading with detected encoding and fallbacks
    tried = set()
    for enc in [detected_encoding] + fallback_encodings:
        if enc in tried:
            continue
        tried.add(enc)
        try:
            df = pd.read_csv(
                file_path,
                encoding=enc,
                quotechar=quotechar,
                escapechar=escapechar,
                delimiter=delimiter,
                dtype=dtype,
                skipinitialspace=True,
            )
            logger.debug(
                f"Successfully read file with encoding: {enc} and delimiter: '{delimiter}'"
            )
            return df
        except UnicodeDecodeError:
            logger.error(f"Failed with encoding: {enc}")
        except Exception as e:
            logger.error(f"Error reading file with encoding {enc}: {e}")

    raise UnicodeDecodeError(
        "utf-8", b"", 0, 1, "Unable to read file with tried encodings"
    )


def read_table(
    file_path: Path | str, dtype: dict | None = None, refresh: bool = False
) -> pd.DataFrame:
    """Read a table from CSV, TSV, or Parquet with caching and optional automatic refresh.

    Args:
        file_path (Path | str): Path to the file to read. Supported formats are CSV, TSV, and Parquet.
        dtype (dict | None): Optional dictionary specifying the data types for specific columns.
        refresh (bool): If True, forces re-reading the file even if it is cached. Default is False.

    Returns:
        pd.DataFrame: DataFrame containing the data from the file.

    """
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    # Check if cached and file not changed
    mtime = file_path.stat().st_mtime
    if file_path in _table_cache and not refresh:
        if _file_mtime.get(file_path, 0) == mtime:
            return _table_cache[file_path]

    # Load file based on suffix
    suffix = file_path.suffix.lower()
    if suffix in [".csv", ".tsv", ".txt"]:
        df = read_table_safely(file_path, dtype=dtype)
    elif suffix == ".parquet":
        df = pd.read_parquet(file_path)
        if dtype:
            for col, typ in dtype.items():
                if col in df.columns:
                    df[col] = df[col].astype(typ)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    # remove leading/trailing whitespace from column names
    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]

    # Update cache and mtime
    _table_cache[file_path] = df
    _file_mtime[file_path] = mtime

    return df
