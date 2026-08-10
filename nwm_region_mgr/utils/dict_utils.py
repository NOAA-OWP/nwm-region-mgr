"""Define utilities and/or help functions for dictionaries.

dict_utils.py

Functions:
    - remove_nulls: Recursively remove None values from a dictionary or list.
    - convert_enum_to_value: Recursively convert Enum values to their `.value` (string) for YAML serialization.
    - flatten_dict: Flatten a nested dictionary into a single level with concatenated keys.

"""

from enum import Enum
from typing import Any


def remove_nulls(d: dict | list) -> dict | list:
    """Remove nulls.

    Recursively remove None values from a dictionary or list.
    This function traverses the input data structure and removes any keys with None values
    or any elements that are None in lists. It also removes empty dictionaries.

    Parameters
    ----------
    d : dict or list
        The input data structure to clean. It can be a dictionary or a list.

    Returns
    -------
    dict or list
        The cleaned data structure with None values and empty dictionaries removed.

    """
    if isinstance(d, dict):
        return {
            k: remove_nulls(v)
            for k, v in d.items()
            if v is not None and remove_nulls(v) != {}
        }
    elif isinstance(d, list):
        return [remove_nulls(v) for v in d if v is not None]
    else:
        return d


def convert_enum_to_value(obj: Any) -> Any:
    """Recursively convert Enum values to their `.value` (string) for YAML serialization.

    Args:
        obj: The object to convert, which can be a dictionary, list, or an Enum instance.

    Returns:
        The converted object with Enum values replaced by their string representations.

    """
    if isinstance(obj, dict):
        return {k: convert_enum_to_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_enum_to_value(item) for item in obj]
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dictionary.

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): The base key to prepend to the flattened keys.
        sep (str): The separator to use between keys.

    Returns:
        dict: A flattened dictionary with concatenated keys.

    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
