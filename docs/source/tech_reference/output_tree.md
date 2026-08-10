## Output Directory Structure

The output directory contains three subdirectories: `region`, `ngen`, and `eval`, which store the respective output files for the regionalization, ngen simulation, and evaluation steps.

```bash
outputs
├── eval
│   └── vpu_09
│   │   ├── joined
│   │   │   ├── test1_gower.ngen.ngen_simulation.joined.parquet
│   │   │   └── test1_kmeans.ngen.ngen_simulation.joined.parquet
│   │   ├── metrics
│   │   │   ├── test1_gower.ngen.ngen_simulation.metrics.parquet
│   │   │   └── test1_kmeans.ngen.ngen_simulation.metrics.parquet
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
│   │   │   │   │   ├── map_CORR_test1_gower.png
│   │   │   │   │   ├── map_CORR_test1_kmeans.png
│   │   │   │   │   ├── map_KGE_test1_gower.png
│   │   │   │   │   ├── map_KGE_test1_kmeans.png
│   │   │   │   │   ├── map_NNSE_test1_gower.png
│   │   │   │   │   ├── map_NNSE_test1_kmeans.png
│   │   │   │   │   ├── map_NSE_test1_gower.png
│   │   │   │   │   └── map_NSE_test1_kmeans.png
│   │   ├── test1_gower
│   │   │   └── ngen_simulation
│   │   │   │   └── 20221001T03-20221001T10.parquet
│   │   ├── test1_kmeans
│   │   │   └── ngen_simulation
│   │   │   │   └── 20221001T03-20221001T10.parquet
│   │   ├── usgs
│   │   │   └── 2022-10-01_2022-10-03.parquet
│   │   └── verification.log
├── mswm.config_test1_gower_vpu09
├── mswm.config_test1_kmeans_vpu09
├── ngen
│   ├── regionalization
│   │   ├── test1_gower
│   │   │   └── vpu_09
│   │   │   │   └── Output
│   │   │   │   │   └── troute_output_202210010000.nc
│   │   └── test1_kmeans
│   │   │   └── vpu_09
│   │   │   │   └── Output
│   │   │   │   │   └── troute_output_202210010000.nc
│   └── test1
│   │   └── config_ngen_final.yaml
└── region
│   ├── test1
│   │   ├── attr_data_final
│   │   │   ├── attr_conus_vpu09.parquet
│   │   │   └── plots
│   │   │   │   ├── bar_attr_missing_count_conus_vpu09.png
│   │   │   │   ├── hist_attr_conus_vpu09.png
│   │   │   │   └── map_attr_conus_vpu09.png
│   │   ├── config_formreg_final.yaml
│   │   ├── config_parreg_final.yaml
│   │   ├── formulations
│   │   │   ├── form_conus_vpu04.parquet
│   │   │   ├── form_conus_vpu04_pars.parquet
│   │   │   ├── form_conus_vpu07.parquet
│   │   │   ├── form_conus_vpu07_pars.parquet
│   │   │   ├── form_conus_vpu09.parquet
│   │   │   ├── form_conus_vpu09_pars.parquet
│   │   │   ├── form_conus_vpu10U.parquet
│   │   │   ├── form_conus_vpu10U_pars.parquet
│   │   │   └── plots
│   │   │   │   ├── hist_form_conus_vpu04.png
│   │   │   │   ├── hist_form_conus_vpu07.png
│   │   │   │   ├── hist_form_conus_vpu09.png
│   │   │   │   ├── hist_form_conus_vpu10U.png
│   │   │   │   ├── map_form_conus_vpu04.png
│   │   │   │   ├── map_form_conus_vpu07.png
│   │   │   │   ├── map_form_conus_vpu09.png
│   │   │   │   └── map_form_conus_vpu10U.png
│   │   ├── pairs
│   │   │   ├── pairs_gower_conus_vpu09.parquet
│   │   │   ├── pairs_gower_conus_vpu09_mswm.csv
│   │   │   ├── pairs_kmeans_conus_vpu09.parquet
│   │   │   ├── pairs_kmeans_conus_vpu09_mswm.csv
│   │   │   └── plots
│   │   │   │   ├── hist_pairs_gower_conus_vpu09.png
│   │   │   │   ├── hist_pairs_kmeans_conus_vpu09.png
│   │   │   │   ├── map_donors_conus_vpu09.png
│   │   │   │   ├── map_pairs_gower_conus_vpu09.png
│   │   │   │   └── map_pairs_kmeans_conus_vpu09.png
│   │   ├── params
│   │   │   ├── formulation_params_gower_conus_vpu09.csv
│   │   │   ├── formulation_params_kmeans_conus_vpu09.csv
│   │   │   └── plots
│   │   │   │   └── map_formulation_params_kmeans_conus_vpu09.png
│   │   ├── spatial_distance
│   │   │   └── donor_receiver_dist_conus_vpu09.parquet
│   │   └── summary_score
│   │   │   ├── plots
│   │   │   │   ├── hist_score_conus_vpu04.png
│   │   │   │   ├── hist_score_conus_vpu07.png
│   │   │   │   ├── hist_score_conus_vpu09.png
│   │   │   │   ├── hist_score_conus_vpu10U.png
│   │   │   │   ├── map_score_conus_vpu04.png
│   │   │   │   ├── map_score_conus_vpu07.png
│   │   │   │   ├── map_score_conus_vpu09.png
│   │   │   │   └── map_score_conus_vpu10U.png
│   │   │   ├── score_conus_all_gages.parquet
│   │   │   ├── score_conus_vpu04.parquet
│   │   │   ├── score_conus_vpu07.parquet
│   │   │   ├── score_conus_vpu09.parquet
│   │   │   └── score_conus_vpu10U.parquet
│   └── test1.log
```
