"""utils package with various utility/helper functions."""

from nwm_region_mgr.utils.config_utils import (
    BaseConfig,
    BaseConfigProcessor,
    BaseGeneralConfig,
    BaseOutputConfig,
    FieldCrosswalk,
    LayerCrosswalk,
    LoggingConfig,
)
from nwm_region_mgr.utils.dict_utils import (
    convert_enum_to_value,
    flatten_dict,
    remove_nulls,
)
from nwm_region_mgr.utils.hydrofabric_utils import (
    area_weighted_average,
    dissolve_polygons,
    find_gages_within_buffer,
)
from nwm_region_mgr.utils.io_utils import read_table, save_data
from nwm_region_mgr.utils.logging_utils import setup_logging
from nwm_region_mgr.utils.plot_utils import plot_histogram, plot_spatial_map
from nwm_region_mgr.utils.string_utils import (
    expand_with_lists,
    recursive_substitute,
    recursive_substitute_multi_lists,
)
from nwm_region_mgr.utils.validation_utils import (
    check_columns_dataframe,
    check_columns_hydrofabric,
    check_options,
)

__all__ = [
    "BaseConfig",
    "BaseGeneralConfig",
    "BaseOutputConfig",
    "BaseConfigProcessor",
    "LoggingConfig",
    "FieldCrosswalk",
    "LayerCrosswalk",
    "remove_nulls",
    "convert_enum_to_value",
    "flatten_dict",
    "dissolve_polygons",
    "find_gages_within_buffer",
    "area_weighted_average",
    "read_table",
    "save_data",
    "setup_logging",
    "plot_histogram",
    "plot_spatial_map",
    "expand_with_lists",
    "recursive_substitute",
    "recursive_substitute_multi_lists",
    "check_columns_dataframe",
    "check_columns_hydrofabric",
    "check_options",
]
