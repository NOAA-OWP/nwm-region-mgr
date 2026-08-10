"""Script to get column names of various input files used in the regionalization workflows."""

from pathlib import Path

import geopandas as gpd

from nwm_region_mgr.utils import read_table

# input files
dir1 = "~/repos/nwm-region-mgr/data/inputs"

file1 = "gages_nwm4_calib_all.csv"
file1 = "calval_stats/stat_calval_all_conus.parquet"
file1 = "pseudo_calib_params/sampled_params_conus.csv"
file1 = "cwt_divide_huc12/cwt_divide_huc12_conus.csv"
file1 = "attr_config/attr_selection_ngen.csv"
file1 = "attr_datasets/ngen/attr_ngen_conus.parquet"
file1 = "snow_frac/vpu03S_snow_frac.parquet"
file1 = "formulation_costs_secs_per_catchment.csv"
file1 = "hydrofabric/vpu_divides/vpu_03S.gpkg"

# output files
# dir1 = "~/repos/nwm-region-mgr/data/outputs"

# print column names, one per line
path1 = Path(dir1).expanduser() / file1
if path1.suffix == ".gpkg":
    df1 = gpd.read_file(path1)
else:
    df1 = read_table(path1)
for col in df1.columns:
    print(col)
