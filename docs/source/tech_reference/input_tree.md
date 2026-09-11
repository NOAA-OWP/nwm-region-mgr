## Input Directory Structure

The input directory contains three subdirectories: `region` and `eval`, which store the respective input files for the regionalization and evaluation steps. Note that the ngen simulation step does not require input files from this directory.

```bash
inputs
├── eval
│   ├── usgs_ngen_crosswalk_ak.parquet
│   ├── usgs_ngen_crosswalk_conus.parquet
│   ├── usgs_ngen_crosswalk_hi.parquet
│   └── usgs_ngen_crosswalk_prvi.parquet
└── region
│   ├── NHDPlusV21
│   │   ├── NHDPlusNationalData
│   │   ├── NHD_H_Alaska_State_GPKG.gpkg
│   │   └── README
│   ├── attr_config
│   │   ├── attr_selection_hlr.csv
│   │   ├── attr_selection_hydroatlas.csv
│   │   ├── attr_selection_ngen.csv
│   │   └── attr_selection_streamcat.csv
│   ├── attr_datasets
│   │   ├── hlr
│   │   ├── hydroatlas
│   │   ├── ngen
│   │   └── streamcat
│   ├── calval_stats
│   │   ├── stat_calval_all_ak.parquet
│   │   ├── stat_calval_all_conus.parquet
│   │   ├── stat_calval_all_hi.parquet
│   │   └── stat_calval_all_prvi.parquet
│   ├── cwt_divide_gage
│   │   ├── calib_gage_divide_ak.parquet
│   │   ├── calib_gage_divide_conus.parquet
│   │   ├── calib_gage_divide_hi.parquet
│   │   └── calib_gage_divide_prvi.parquet
│   ├── cwt_divide_huc12
│   │   ├── cwt_huc12_divide_ak.csv
│   │   ├── cwt_huc12_divide_conus.csv
│   │   ├── cwt_huc12_divide_hi.csv
│   │   ├── cwt_huc12_divide_prvi.csv
│   │   ├── unmatched_catchments_ak.png
│   │   └── unmatched_catchments_conus.png
│   ├── formulation_costs_secs_per_catchment.csv
│   ├── gages_nwm4_calib_all.csv
│   ├── hydrofabric
│   │   └── gpkg_vpu
│   ├── manual_pairs
│   │   ├── manual_pairs_vpu01_nhf.csv
│   │   ├── manual_pairs_vpu03S_nhf.csv
│   │   ├── manual_pairs_vpu20_nhf.csv
│   │   └── manual_pairs_vpu21_nhf.csv
│   ├── pseudo_calib_params
│   │   ├── sampled_params_ak.csv
│   │   ├── sampled_params_conus.csv
│   │   ├── sampled_params_hi.csv
│   │   └── sampled_params_prvi.csv
│   └── stats_calib_valid_nwmv3.csv
```
