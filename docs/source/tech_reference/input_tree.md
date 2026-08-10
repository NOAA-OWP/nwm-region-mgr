## Input Directory Structure

The input directory contains three subdirectories: `region`, `ngen`, and `eval`, which store the respective input files for the regionalization, ngen simulation, and evaluation steps.

```bash
inputs
├── eval
│   ├── gage_hydrofabric_all_domains.parquet
│   ├── gage_list_ak_vpu_ak.csv
│   ├── gage_list_conus_vpu_01.csv
│   ├── gage_list_conus_vpu_02.csv
│   ├── gage_list_conus_vpu_03N.csv
│   ├── gage_list_conus_vpu_03S.csv
│   ├── gage_list_conus_vpu_03W.csv
│   ├── gage_list_conus_vpu_04.csv
│   ├── gage_list_conus_vpu_05.csv
│   ├── gage_list_conus_vpu_06.csv
│   ├── gage_list_conus_vpu_07.csv
│   ├── gage_list_conus_vpu_08.csv
│   ├── gage_list_conus_vpu_09.csv
│   ├── gage_list_conus_vpu_10L.csv
│   ├── gage_list_conus_vpu_10U.csv
│   ├── gage_list_conus_vpu_11.csv
│   ├── gage_list_conus_vpu_12.csv
│   ├── gage_list_conus_vpu_13.csv
│   ├── gage_list_conus_vpu_14.csv
│   ├── gage_list_conus_vpu_15.csv
│   ├── gage_list_conus_vpu_16.csv
│   ├── gage_list_conus_vpu_17.csv
│   ├── gage_list_conus_vpu_18.csv
│   ├── gage_list_hi_vpu_hi.csv
│   ├── gage_list_prvi_vpu_prvi.csv
│   ├── usgs_ngen_crosswalk_ak.parquet
│   ├── usgs_ngen_crosswalk_conus.parquet
│   ├── usgs_ngen_crosswalk_hi.parquet
│   └── usgs_ngen_crosswalk_prvi.parquet
├── ngen
│   ├── module_parameter_files
│   │   ├── lasam
│   │   ├── lstm
│   │   ├── noah-owp-modular
│   │   ├── sac_sma_params_2.2.csv
│   │   ├── snow17_params_2.2.csv
│   │   └── ueb
│   └── mswm.config.template.docker
└── region
│   ├── NHDPlusV21
│   │   ├── NHDPlusNationalData
│   │   ├── NHD_H_Alaska_State_GPKG.gpkg
│   │   ├── NHD_H_Alaska_State_GPKG.jpg
│   │   ├── NHD_H_Alaska_State_GPKG.xml
│   │   └── README
│   ├── attr_config
│   │   ├── attr_selection_hlr.csv
│   │   ├── attr_selection_ngen.csv
│   │   └── attr_selection_streamcat.csv
│   ├── attr_datasets
│   │   ├── hlr
│   │   ├── ngen
│   │   └── streamcat
│   ├── calval_stats
│   │   ├── stat_calval_all_ak.csv
│   │   ├── stat_calval_all_ak.parquet
│   │   ├── stat_calval_all_conus.csv
│   │   ├── stat_calval_all_conus.parquet
│   │   ├── stat_calval_all_hi.csv
│   │   ├── stat_calval_all_hi.parquet
│   │   ├── stat_calval_all_prvi.csv
│   │   └── stat_calval_all_prvi.parquet
│   ├── cwt_divide_gage
│   │   ├── calib_gage_divide_ak.parquet
│   │   ├── calib_gage_divide_conus.parquet
│   │   ├── calib_gage_divide_hi.parquet
│   │   └── calib_gage_divide_prvi.parquet
│   ├── cwt_divide_huc12
│   │   ├── cwt_divide_huc12_ak.csv
│   │   ├── cwt_divide_huc12_conus.csv
│   │   ├── cwt_divide_huc12_hi.csv
│   │   └── cwt_divide_huc12_prvi.csv
│   ├── formulation_costs_secs_per_catchment.csv
│   ├── gages_nwm4_calib_all.csv
│   ├── hydrofabric
│   │   └── gpkg_vpu
│   ├── pseudo_calib_params
│   │   ├── sampled_params_ak.csv
│   │   ├── sampled_params_conus.csv
│   │   ├── sampled_params_hi.csv
│   │   └── sampled_params_prvi.csv
│   └── snow_frac
│   │   ├── vpu01_snow_frac.parquet
│   │   ├── vpu02_snow_frac.parquet
│   │   ├── vpu03N_snow_frac.parquet
│   │   ├── vpu03S_snow_frac.parquet
│   │   ├── vpu03W_snow_frac.parquet
│   │   ├── vpu04_snow_frac.parquet
│   │   ├── vpu05_snow_frac.parquet
│   │   ├── vpu06_snow_frac.parquet
│   │   ├── vpu07_snow_frac.parquet
│   │   ├── vpu08_snow_frac.parquet
│   │   ├── vpu09_snow_frac.parquet
│   │   ├── vpu10L_snow_frac.parquet
│   │   ├── vpu10U_snow_frac.parquet
│   │   ├── vpu11_snow_frac.parquet
│   │   ├── vpu12_snow_frac.parquet
│   │   ├── vpu13_snow_frac.parquet
│   │   ├── vpu14_snow_frac.parquet
│   │   ├── vpu15_snow_frac.parquet
│   │   ├── vpu16_snow_frac.parquet
│   │   ├── vpu17_snow_frac.parquet
│   │   ├── vpu18_snow_frac.parquet
│   │   ├── vpuak_snow_frac.parquet
│   │   └── vpuprvi_snow_frac.parquet
```
