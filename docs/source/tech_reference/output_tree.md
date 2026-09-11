## Output Directory Structure

The output directory contains three subdirectories: `region`, `ngen`, and `eval`, which store the respective output files for the regionalization, ngen simulation, and evaluation steps.

```bash
outputs
├── eval
│   └── vpu_03S
│   │   ├── joined
│   │   │   ├── test_kmeans.ngen.ngen_simulation.joined.group0.parquet
│   │   │   ├── test_kmeans.ngen.ngen_simulation.joined.group1.parquet
│   │   │   └── test_kmeans.ngen.ngen_simulation.joined.group2.parquet
│   │   ├── metrics
│   │   │   └── test_kmeans.ngen.ngen_simulation.metrics.parquet
│   │   ├── nwm_verf_config_expanded.yaml
│   │   ├── plots
│   │   │   └── ngen_simulation
│   │   │   │   ├── boxplot
│   │   │   │   │   ├── boxplot_CORR.png
│   │   │   │   │   ├── boxplot_KGE.png
│   │   │   │   │   ├── boxplot_NNSE.png
│   │   │   │   │   └── boxplot_NSE.png
│   │   │   │   ├── histogram
│   │   │   │   │   ├── hist_CORR.png
│   │   │   │   │   ├── hist_KGE.png
│   │   │   │   │   ├── hist_NNSE.png
│   │   │   │   │   └── hist_NSE.png
│   │   │   │   └── spatial_map
│   │   │   │   │   ├── map_CORR_test_kmeans.png
│   │   │   │   │   ├── map_KGE_test_kmeans.png
│   │   │   │   │   ├── map_NNSE_test_kmeans.png
│   │   │   │   │   └── map_NSE_test_kmeans.png
│   │   ├── test_kmeans
│   │   │   └── ngen_simulation
│   │   │   │   └── 20121001T03-20121001T10.parquet
│   │   ├── usgs
│   │   │   └── 2012-10-01_2012-10-03.parquet
│   │   └── verification.log
├── mswm.config_test_kmeans_vpu03S
├── ngen
│   ├── regionalization
│   │   └── test_kmeans
│   │   │   └── vpu_03S
│   │   │   │   ├── Output
│   │   │   │   │   └── troute_output_201210010000.nc
│   │   │   │   ├── logs
│   │   │   │   │   ├── msw_mgr_regionalization.log
│   │   │   │   │   └── msw_mgr_regionalization_payload.log
│   │   │   │   └── vpu_03S_realization_config_bmi_region.json
│   └── test
│   │   ├── config_ngen_final_conus.yaml
│   │   └── ngen_conus.log
└── region
│   └── test
│   │   ├── attr_data_final
│   │   │   ├── attr_conus_vpu03S.parquet
│   │   │   └── plots
│   │   │   │   ├── bar_attr_missing_count_conus_vpu03S.png
│   │   │   │   ├── hist_attr_conus_vpu03S.png
│   │   │   │   └── map_attr_conus_vpu03S.png
│   │   ├── config_parreg_final_conus.yaml
│   │   ├── formulations
│   │   │   ├── form_conus_vpu03N.parquet
│   │   │   ├── form_conus_vpu03N_pars.parquet
│   │   │   ├── form_conus_vpu03S.parquet
│   │   │   ├── form_conus_vpu03S_pars.parquet
│   │   │   ├── form_conus_vpu03W.parquet
│   │   │   ├── form_conus_vpu03W_pars.parquet
│   │   │   ├── form_conus_vpu06.parquet
│   │   │   ├── form_conus_vpu06_pars.parquet
│   │   │   └── plots
│   │   │   │   ├── hist_form_conus_vpu03N.png
│   │   │   │   ├── hist_form_conus_vpu03S.png
│   │   │   │   ├── hist_form_conus_vpu03W.png
│   │   │   │   ├── hist_form_conus_vpu06.png
│   │   │   │   ├── map_form_conus_vpu03N.png
│   │   │   │   ├── map_form_conus_vpu03S.png
│   │   │   │   ├── map_form_conus_vpu03W.png
│   │   │   │   └── map_form_conus_vpu06.png
│   │   ├── pairs
│   │   │   ├── pairs_gower_conus_vpu03S.parquet
│   │   │   ├── pairs_gower_conus_vpu03S_mswm.csv
│   │   │   ├── pairs_kmeans_conus_vpu03S.parquet
│   │   │   ├── pairs_kmeans_conus_vpu03S_mswm.csv
│   │   │   └── plots
│   │   │   │   ├── hist_pairs_gower_conus_vpu03S.png
│   │   │   │   ├── hist_pairs_kmeans_conus_vpu03S.png
│   │   │   │   ├── map_donors_conus_vpu03S.png
│   │   │   │   ├── map_pairs_gower_conus_vpu03S.png
│   │   │   │   └── map_pairs_kmeans_conus_vpu03S.png
│   │   ├── params
│   │   │   ├── formulation_params_gower_conus_vpu03S.csv
│   │   │   ├── formulation_params_kmeans_conus_vpu03S.csv
│   │   │   └── plots
│   │   │   │   ├── map_formulation_params_gower_conus_vpu03S.png
│   │   │   │   └── map_formulation_params_kmeans_conus_vpu03S.png
│   │   ├── parreg_conus.log
│   │   ├── spatial_distance
│   │   │   └── donor_receiver_dist_conus_vpu03S.parquet
│   │   └── summary_score
│   │   │   ├── plots
│   │   │   │   ├── hist_score_conus_vpu03N.png
│   │   │   │   ├── hist_score_conus_vpu03S.png
│   │   │   │   ├── hist_score_conus_vpu03W.png
│   │   │   │   ├── hist_score_conus_vpu06.png
│   │   │   │   ├── map_score_conus_vpu03N.png
│   │   │   │   ├── map_score_conus_vpu03S.png
│   │   │   │   ├── map_score_conus_vpu03W.png
│   │   │   │   └── map_score_conus_vpu06.png
│   │   │   ├── score_conus_all_gages.parquet
│   │   │   ├── score_conus_vpu03N.parquet
│   │   │   ├── score_conus_vpu03S.parquet
│   │   │   ├── score_conus_vpu03W.parquet
│   │   │   └── score_conus_vpu06.parquet
```
