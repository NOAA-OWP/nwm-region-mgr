# Regionalization Configuration

### Introduction

This section provides detailed documentation for the configuration files used in the NWM Regionalization Manager (nwm-region-mgr) tool. The configuration files define the parameters and settings for both formulation and parameter regionalization processes.

Example files and schemas for all configuration fields and subfields are included below. You can navigate to each config file or schema section using the tabs on the right or the table of contents below.

The tabs on the left will take you to the builder for each of the specific config files. Currently, only the general configuration builder is available. The builders for formulation and parameter regionalizations are still under development. In the builder, you will be prompted to enter setup information for your regionalization run, or you can scroll to the bottom to fill in default values. Once done, hit 'download' to save the generated configuration YAML file to your local system.
### Schema Reference and Sample YAML Config Files

  - [General configurations (shared by formulation & parameter regionalizations)](#general-configurations-shared-by-formulation-parameter-regionalizations)
    - [Example File](#example-file)
    - [general Schema (general)](#general-schema-general)
    - [general Schema (id_col)](#general-schema-id-col)
    - [general Schema (layer_name)](#general-schema-layer-name)
    - [general Schema (logging)](#general-schema-logging)
  - [Specific configurations for formulation regionalization (formreg)](#specific-configurations-for-formulation-regionalization-formreg)
    - [Example File](#example-file)
    - [formreg Schema (general)](#formreg-schema-general)
    - [formreg Schema (spatial_unit)](#formreg-schema-spatial-unit)
    - [formreg Schema (best_formulation)](#formreg-schema-best-formulation)
    - [formreg Schema (summary_score)](#formreg-schema-summary-score)
    - [formreg Schema (metric_eval_period)](#formreg-schema-metric-eval-period)
    - [formreg Schema (metrics)](#formreg-schema-metrics)
    - [formreg Schema (formulation_cost)](#formreg-schema-formulation-cost)
    - [formreg Schema (output)](#formreg-schema-output)
    - [formreg Schema (BaseOutputConfig)](#formreg-schema-baseoutputconfig)
  - [Specific configurations for parameter regionalization (parreg)](#specific-configurations-for-parameter-regionalization-parreg)
    - [Example File](#example-file)
    - [parreg Schema (general)](#parreg-schema-general)
    - [parreg Schema (donor)](#parreg-schema-donor)
    - [parreg Schema (metric_eval_period)](#parreg-schema-metric-eval-period)
    - [parreg Schema (metric_threshold)](#parreg-schema-metric-threshold)
    - [parreg Schema (attr_datasets_config)](#parreg-schema-attr-datasets-config)
    - [parreg Schema (attr_datasets)](#parreg-schema-attr-datasets)
    - [parreg Schema (snow_cover)](#parreg-schema-snow-cover)
    - [parreg Schema (algorithms)](#parreg-schema-algorithms)
    - [parreg Schema (algo_general)](#parreg-schema-algo-general)
    - [parreg Schema (gower)](#parreg-schema-gower)
    - [parreg Schema (kmeans)](#parreg-schema-kmeans)
    - [parreg Schema (kmedoids)](#parreg-schema-kmedoids)
    - [parreg Schema (birch)](#parreg-schema-birch)
    - [parreg Schema (hdbscan)](#parreg-schema-hdbscan)
    - [parreg Schema (output)](#parreg-schema-output)
    - [parreg Schema (BaseOutputConfig)](#parreg-schema-baseoutputconfig)

### General configurations (shared by formulation & parameter regionalizations)

#### Example File
```yaml
general:
  run_name: 'test' #----------------------------------------------------------------------------Name of the run, used to create output folders and files.
  domain: 'conus' #-----------------------------------------------------------------------------Which National Water Model Domain this run uses.
  vpu_list: ['09'] #----------------------------------------------------------------------------List of vector processing units (VPUs) within the domain or 'all' to process all.
  base_dir: '/root/nwm-region-mgr/data/' #------------------------------------------------------Path to base directory for input/output files.
  ngen_hydrofabric_file: '{base_dir}/inputs/hydrofabric/vpu_09.gpkg' #--------------------------Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'}.If providing a string with placeholders like {vpu_list}, they will be substituted accordingly and expanded to a dictionary mapping each VPU to its corresponding file. This file must include columns 'divide_id', 'vpuid' and 'geometry'.
  gage_divide_cwt_file: '{base_dir}/inputs/calib_gage_divide_{domain}.parquet' #----------------Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'.
  donor_gage_file: '{base_dir}/inputs/gages_nwm4_calib_all.csv' #-------------------------------Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'.
  calval_stats_file: ['stat_calval_all_{domain}.csv', 'stat_calval_all_{domain}.parquet'] #-----Path to CSV or parquet file with calibration/validation statistics for all calibration gages and formulations, e.g., 'stat_calval_all_conus.parquet', 'stat_calval_all_conus.csv'. Must include columns for 'gage_id', 'formulation', and relevant metrics to be used for formulation and parameter regionalization.
  calib_param_file: ['calib_params_{domain}.csv', 'calib_params_{domain}.parquet'] #------------Path to CSV or parquet file containing calibrated parameters for all calibration gages and formulations in the domain. Must include columns for 'gage_id', 'formulation', and calibrated parameters.
  approach_calib_basins: ['regionalization', 'summary_score'] #---------------------------------Strategy for assigning formulations to calibrated basins. Valid options are 'regionalization' (assign the formulation chosen for the region) or 'summary_score' (assign based on formulation summary scores for the calibrated basin).
  id_col: #-------------------------------------------------------------------------------------Dictionary mapping column names for unique identifiers in all applicable files.
    divide: 'divide_id' #-----------------------------------------------------------------------Column name for divide (catchment) ID.
    gage: 'gage_id' #---------------------------------------------------------------------------Column name for gage (basin) ID.
    huc12: 'huc_12' #---------------------------------------------------------------------------Column name for HUC12 ID.
    vpu: 'vpuid' #------------------------------------------------------------------------------Column name for VPU ID.
    drainage_area: 'areasqkm' #-----------------------------------------------------------------Column name for drainage area.
  layer_name: #---------------------------------------------------------------------------------Dictionary mapping layer names for hydrofabric files. Identifies the layer in each hydrofabric file to be used during regionalization.
    huc12: 'WBDSnapshot_National' #-------------------------------------------------------------Layer name for HUC12 hydrofabric file.
    ngen: 'divides' #---------------------------------------------------------------------------Layer name for NextGen hydrofabric file.
  logging: #------------------------------------------------------------------------------------Logging configuration for the application.
    level: 'info' #-----------------------------------------------------------------------------Logging level.
    log_to_file: True #-------------------------------------------------------------------------Whether to log to a file. If set to True, logging messages will be written to the specified log file, in addition to the console.
    file: 'logs/{run_name}.log' #---------------------------------------------------------------Path to the log file. If not provided, logging will be written to console only.
```

#### general Schema (general)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| run_name | str | Name of the run, used to create output folders and files. | test | test |
| domain | str = conus \| ak \| hi \| prvi | Which National Water Model Domain this run uses. | conus | conus |
| vpu_list | List[str] \| str | List of vector processing units (VPUs) within the domain or 'all' to process all. | ['03S'] | ['09'] |
| base_dir | str | Path to base directory for input/output files. | ./data/ | /root/nwm-region-mgr/data/ |
| ngen_hydrofabric_file | Path \| str \| Dict[str, Path] \| Dict[str, str] | Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'}.If providing a string with placeholders like {vpu_list}, they will be substituted accordingly and expanded to a dictionary mapping each VPU to its corresponding file. This file must include columns 'divide_id', 'vpuid' and 'geometry'. | vpu_03S.gpkg | {base_dir}/inputs/hydrofabric/vpu_09.gpkg |
| gage_divide_cwt_file | Path \| str | Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'. | calib_gage_divide_{domain}.parquet | {base_dir}/inputs/calib_gage_divide_{domain}.parquet |
| donor_gage_file | Path \| str | Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'. | gages_nwm4_calib_all.csv | {base_dir}/inputs/gages_nwm4_calib_all.csv |
| calval_stats_file | Path \| str | Path to CSV or parquet file with calibration/validation statistics for all calibration gages and formulations, e.g., 'stat_calval_all_conus.parquet', 'stat_calval_all_conus.csv'. Must include columns for 'gage_id', 'formulation', and relevant metrics to be used for formulation and parameter regionalization. | stat_calval_all_{domain}.parquet | ['stat_calval_all_{domain}.csv', 'stat_calval_all_{domain}.parquet'] |
| calib_param_file | Path \| str | Path to CSV or parquet file containing calibrated parameters for all calibration gages and formulations in the domain. Must include columns for 'gage_id', 'formulation', and calibrated parameters. | calib_params_{domain}.csv | ['calib_params_{domain}.csv', 'calib_params_{domain}.parquet'] |
| approach_calib_basins | str = regionalization \| summary_score | Strategy for assigning formulations to calibrated basins. Valid options are 'regionalization' (assign the formulation chosen for the region) or 'summary_score' (assign based on formulation summary scores for the calibrated basin). | summary_score | ['regionalization', 'summary_score'] |
| id_col | FieldCrosswalk | Dictionary mapping column names for unique identifiers in all applicable files. | divide='divide_id' gage='gage_id' huc12='huc_12' vpu='vpuid' drainage_area='areasqkm' | {'divide': 'divide_id', 'gage': 'gage_id', 'huc12': 'huc_12', 'vpu': 'vpuid', 'drainage_area': 'areasqkm'} |
| layer_name | LayerCrosswalk | Dictionary mapping layer names for hydrofabric files. Identifies the layer in each hydrofabric file to be used during regionalization. | huc12='WBDSnapshot_National' ngen='divides' | {'huc12': 'WBDSnapshot_National', 'ngen': 'divides'} |
| logging | LoggingConfig | Logging configuration for the application. | level='info' log_to_file=False file=None | {'level': 'info', 'log_to_file': True, 'file': 'logs/{run_name}.log'} |

#### general Schema (id_col)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| divide | str | Column name for divide (catchment) ID. | divide_id | divide_id |
| gage | str | Column name for gage (basin) ID. | gage_id | gage_id |
| huc12 | str | Column name for HUC12 ID. | huc_12 | huc_12 |
| vpu | str | Column name for VPU ID. | vpuid | vpuid |
| drainage_area | str | Column name for drainage area. | areasqkm | areasqkm |

#### general Schema (layer_name)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| huc12 | str | Layer name for HUC12 hydrofabric file. | WBDSnapshot_National | WBDSnapshot_National |
| ngen | str | Layer name for NextGen hydrofabric file. | divides | divides |

#### general Schema (logging)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| level | str = debug \| info \| warning \| error \| critical | Logging level. | info | debug |
| log_to_file | bool | Whether to log to a file. If set to True, logging messages will be written to the specified log file, in addition to the console. | False | False |
| file | str \| NoneType | Path to the log file. If not provided, logging will be written to console only. | None | logfile.log |
### Specific configurations for formulation regionalization (formreg)

#### Example File
```yaml
general: #-----------------------------------------------------------------------------------------------General settings for formulation regionalization
  huc12_hydrofabric_file: 'NationalWBDSnapshot.gdb' #----------------------------------------------------Path to HUC12 hydrofabric file containing HUC12 polygons for spatial discretization.
  divide_huc12_cwt_file: 'cwt_divide_huc12_{domain}.csv' #-----------------------------------------------Path to crosswalk file between HUC12 basins and NextGen catchments, with columns 'divide_id' and 'huc_12'.
  calib_basins_only: False #-----------------------------------------------------------------------------Whether to run formulation selection only for calibrated basins (based on summary score). Set to True to limit formulation selection to calibrated basins only; in such cases, parameter regionalization for uncalibrated catchments will not consider preferred formulations.
  formulation_to_include: ['noah-owp-modular cfe-s t-route', 'noah-owp-modular ueb cfe-x t-route'] #-----List of formulations to consider. If None, all available formulations are considered.  If 'all', all formulations are included.
  formulation_to_exclude: ['noah-owp-modular cfe-s t-route'] #-------------------------------------------List of formulations to exclude. If None, no formulations are excluded from available options.
  consider_cost: False #---------------------------------------------------------------------------------Whether to consider computational costs of formulations in the regionalization process.
spatial_unit: #------------------------------------------------------------------------------------------Spatial discretization settings for formulation regionalization.
  huc_level: ['huc2', 'huc4', 'huc6', 'huc8', 'huc10', 'huc12'] #----------------------------------------USGS HUC level used for spatial discretization (e.g., 'huc8'). A single formulation is selected per spatial unit given the spatial discretization level. Accepted formats: 'huc8', 'HUC8', 'huc-8'.
  nmin_calib_basin: 5 #----------------------------------------------------------------------------------Minimum number of calibration basins required per spatial unit for valid formulation selection.
  basin_fill_method: 'upscaling' #-----------------------------------------------------------------------Method to handle spatial units with too few calibration basins. Options: 'upscaling' (by upscaling to a coarser spatial unit), and 'nearest-neighbor' (by pooling basins from neighboring units).
  best_formulation: #------------------------------------------------------------------------------------Strategy to determine the best formulation for each spatial unit.
    method: 'total_score' #------------------------------------------------------------------------------Method to determine the best formulation, options: 'total_score', 'average_score', which selects the formulation with the highest total or average summary score across all subdivisions (e.g., basins or divides as specified by the 'type' field), respectively.
    type: 'divide' #-------------------------------------------------------------------------------------Type of subdivision to use for computing total or average score, options: 'basin', 'divide'.
    tolerance: 0.05 #------------------------------------------------------------------------------------Tolerance (on scale of 0.0 to 1.0) for the summary score. Formulations within this tolerance of the best score are considered equally good.
summary_score: #-----------------------------------------------------------------------------------------Summary score computation configuration for formulation regionalization.
  metric_eval_period: #----------------------------------------------------------------------------------Evaluation period of metrics to be used for screening donors.
    col_name: evalPeriod
    value: valid
  metrics: #---------------------------------------------------------------------------------------------Dictionary of metrics used in the summary score, keyed by metric name. Metric names must match columns in the calibration/validation stats file. Weights must sum to 1.0. Refer to schema of MetricConfig for individual metric settings.
    cor:
      upper: 1.0
      lower: -0.5
      orientation: positive
      weight: 0.5
    kge:
      upper: 1.0
      lower: -0.5
      orientation: positive
      weight: 0.5
formulation_cost: #--------------------------------------------------------------------------------------Computational cost configuration for each formulation.
  file: 'formulation_costs_secs_per_catchment.csv' #-----------------------------------------------------Path to CSV file with formulation costs. If provided, costs will be read from this file.
  costs: #-----------------------------------------------------------------------------------------------Dictionary of formulation costs, keyed by formulation name. If `file` is provided, this is ignored.
    noah-owp-modular ueb cfe-x t-route: 10
output: #------------------------------------------------------------------------------------------------Output configuration for formulation regionalization.
  formulation: #-----------------------------------------------------------------------------------------Output configurations for the selected formulations.
    save: True #-----------------------------------------------------------------------------------------Whether to save output files
    path: '{base_dir}/outputs/{run_name}/formulations' #-------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
    stem: 'form_{domain}_vpu{vpu_list}' #----------------------------------------------------------------File stem for output files, used to create unique file names based on the path.
    stem_suffix: '_pars' #-------------------------------------------------------------------------------Suffix for the file stem, used to create unique file names based on the path for specific needs.
    format: 'parquet' #----------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
    plots: #---------------------------------------------------------------------------------------------Configuration for output plots, if applicable.
      spatial_map: True
      histogram: True
    plot_path: '{base_dir}/outputs/{run_name}/formulations/plots' #--------------------------------------Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path.
  config_final: #----------------------------------------------------------------------------------------Output configuration for the final configuration file after processing, with placeholders resolved.
    save: True #-----------------------------------------------------------------------------------------Whether to save output files
    path: '{base_dir}/outputs/{run_name}/config_formreg_final.yaml' #------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
  summary_score: #---------------------------------------------------------------------------------------Output configurations for the summary score.
    save: True #-----------------------------------------------------------------------------------------Whether to save output files
    path: '{base_dir}/outputs/{run_name}/summary_score' #------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
    stem: 'score_{domain}_vpu{vpu_list}' #---------------------------------------------------------------File stem for output files, used to create unique file names based on the path.
    stem_suffix: '_all_gages' #--------------------------------------------------------------------------Suffix for the file stem, used to create unique file names based on the path for specific needs.
    format: 'parquet' #----------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
    plots: #---------------------------------------------------------------------------------------------Configuration for output plots, if applicable.
      histogram: True
      spatial_map: True
    plot_path: '{base_dir}/outputs/{run_name}/summary_score/plots' #-------------------------------------Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path.
```

#### formreg Schema (general)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| huc12_hydrofabric_file | str \| Path \| NoneType | Path to HUC12 hydrofabric file containing HUC12 polygons for spatial discretization. | None | NationalWBDSnapshot.gdb |
| divide_huc12_cwt_file | str \| NoneType | Path to crosswalk file between HUC12 basins and NextGen catchments, with columns 'divide_id' and 'huc_12'. | None | cwt_divide_huc12_{domain}.csv |
| calib_basins_only | bool | Whether to run formulation selection only for calibrated basins (based on summary score). Set to True to limit formulation selection to calibrated basins only; in such cases, parameter regionalization for uncalibrated catchments will not consider preferred formulations. | False | False |
| formulation_to_include | List[str] \| NoneType | List of formulations to consider. If None, all available formulations are considered.  If 'all', all formulations are included. | None | ['noah-owp-modular cfe-s t-route', 'noah-owp-modular ueb cfe-x t-route'] |
| formulation_to_exclude | List[str] \| NoneType | List of formulations to exclude. If None, no formulations are excluded from available options. | None | ['noah-owp-modular cfe-s t-route'] |
| consider_cost | bool | Whether to consider computational costs of formulations in the regionalization process. | True | False |

#### formreg Schema (spatial_unit)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| huc_level | str | USGS HUC level used for spatial discretization (e.g., 'huc8'). A single formulation is selected per spatial unit given the spatial discretization level. Accepted formats: 'huc8', 'HUC8', 'huc-8'. | huc8 | ['huc2', 'huc4', 'huc6', 'huc8', 'huc10', 'huc12'] |
| nmin_calib_basin | int | Minimum number of calibration basins required per spatial unit for valid formulation selection. | 3 | 5 |
| basin_fill_method | str = upscaling \| nearest-neighbor | Method to handle spatial units with too few calibration basins. Options: 'upscaling' (by upscaling to a coarser spatial unit), and 'nearest-neighbor' (by pooling basins from neighboring units). | upscaling | upscaling |
| best_formulation | BestFormulation | Strategy to determine the best formulation for each spatial unit. | <factory> | {'method': 'total_score', 'type': 'divide', 'tolerance': 0.05} |

#### formreg Schema (best_formulation)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| method | str = total_score \| average_score | Method to determine the best formulation, options: 'total_score', 'average_score', which selects the formulation with the highest total or average summary score across all subdivisions (e.g., basins or divides as specified by the 'type' field), respectively. | total_score | total_score |
| type | str = basin \| divide | Type of subdivision to use for computing total or average score, options: 'basin', 'divide'. | PydanticUndefined | basin |
| tolerance | float | Tolerance (on scale of 0.0 to 1.0) for the summary score. Formulations within this tolerance of the best score are considered equally good. | 0.05 | 0.05 |

#### formreg Schema (summary_score)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| metric_eval_period | MetricEvalPeriod \| NoneType | Evaluation period of metrics to be used for screening donors. | None | {'col_name': 'evalPeriod', 'value': 'valid'} |
| metrics | Dict[str, MetricConfig] | Dictionary of metrics used in the summary score, keyed by metric name. Metric names must match columns in the calibration/validation stats file. Weights must sum to 1.0. Refer to schema of MetricConfig for individual metric settings. | PydanticUndefined | {'cor': {'upper': 1.0, 'lower': -0.5, 'orientation': 'positive', 'weight': 0.5}, 'kge': {'upper': 1.0, 'lower': -0.5, 'orientation': 'positive', 'weight': 0.5}} |

#### formreg Schema (metric_eval_period)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| col_name | str \| NoneType | Name of the column in the donor stats file that contains the evaluation period. No filtering by evaluation period if None. | None | evalPeriod |
| value | str \| NoneType | Value of the evaluation period to filter donor stats. No filtering by evaluation period if None. | None | full |

#### formreg Schema (metrics)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| upper | float \| NoneType | Upper bound for scaling and normalization, must be greater than lower bound. | None | 1 |
| lower | float \| NoneType | Lower bound for scaling and normalization, must be less than upper bound. | None | 0 |
| orientation | str = positive \| negative | Orientation of the metric, either 'positive' or 'negative'. | positive | positive |
| weight | float | Weight of the metric in the summary score, must be between 0.0 and 1.0. If 0.0, the metric is ignored. | 0.0 | 0.25 |
| absolute | bool | Whether to use the absolute value of the metric (e.g., for bias) for normalization. | False | False |

#### formreg Schema (formulation_cost)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| file | str \| NoneType | Path to CSV file with formulation costs. If provided, costs will be read from this file. | None | formulation_costs_secs_per_catchment.csv |
| costs | Dict[str, float] \| NoneType | Dictionary of formulation costs, keyed by formulation name. If `file` is provided, this is ignored. | None | {'noah-owp-modular ueb cfe-x t-route': 10} |

#### formreg Schema (output)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| formulation | BaseOutputConfig | Output configurations for the selected formulations. | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/formulations', 'stem': 'form_{domain}_vpu{vpu_list}', 'stem_suffix': '_pars', 'format': 'parquet', 'plots': {'spatial_map': True, 'histogram': True}, 'plot_path': '{base_dir}/outputs/{run_name}/formulations/plots'} |
| config_final | BaseOutputConfig | Output configuration for the final configuration file after processing, with placeholders resolved. | PydanticUndefined | {'save': True, 'path': '{base_dir}/outputs/{run_name}/config_formreg_final.yaml'} |
| summary_score | BaseOutputConfig | Output configurations for the summary score. | PydanticUndefined | {'save': True, 'path': '{base_dir}/outputs/{run_name}/summary_score', 'stem': 'score_{domain}_vpu{vpu_list}', 'stem_suffix': '_all_gages', 'format': 'parquet', 'plots': {'histogram': True, 'spatial_map': True}, 'plot_path': '{base_dir}/outputs/{run_name}/summary_score/plots'} |

#### formreg Schema (BaseOutputConfig)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| save | bool | Whether to save output files | True | True |
| path | Path \| str | Path to save output file or files. If a directory, the 'stem' and 'format' must be specified. | None | None |
| stem | str \| Dict[str, str] \| NoneType | File stem for output files, used to create unique file names based on the path. | None | None |
| stem_suffix | str \| NoneType | Suffix for the file stem, used to create unique file names based on the path for specific needs. | None | None |
| format | str \| NoneType | File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file. | None | None |
| plots | Dict[str, Any] \| NoneType | Configuration for output plots, if applicable. | None | None |
| plot_path | str \| NoneType | Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path. | None | None |
### Specific configurations for parameter regionalization (parreg)

#### Example File
```yaml
general:
  general: #-------------------------------------------------------------------------------------------------------------------------General configuration settings specific to parameter regionalization.
    n_procs: -1 #--------------------------------------------------------------------------------------------------------------------Number of processors to use for parallel processing. Set to -1 to use all available processors.
    attr_dataset_list: ['ngen', 'streamcat'] #---------------------------------------------------------------------------------------List of attribute dataset names to use. Valid options include 'ngen', 'hlr', 'streamcat'.
    algorithm_list: ['gower', 'kmeans'] #--------------------------------------------------------------------------------------------Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch').
    manual_pairings_file: 'pairs_kmeans_conus_vpu09.parquet' #-----------------------------------------------------------------------Path to the manual pairings file. If provided, this file will be used to specify manual donor-receiver pairings, overriding the algorithmic selections.
  donor: #---------------------------------------------------------------------------------------------------------------------------Configuration for donor selection.
    buffer_km: 100.0 #---------------------------------------------------------------------------------------------------------------Size of buffer (in km) around current VPU to identify qualified donors.
    metric_eval_period: #------------------------------------------------------------------------------------------------------------Evaluation period of metrics to be used for screening donors.
      col_name: eval_period
      value: full
    metric_threshold: #--------------------------------------------------------------------------------------------------------------Dictionary of metric thresholds to be used for screening donors. Each key is a metric name, and the value is a MetricThreshold object specifying the min, max, and absolute settings. Refer to schema of MetricThreshold for details.
      cor:
        min: 0.4
        max: None
        absolute: False
      kge:
        min: 0.2
        max: None
        absolute: False
  attr_datasets: #-------------------------------------------------------------------------------------------------------------------Configuration for attribute datasets available for use in regionalization.
    ngen: #--------------------------------------------------------------------------------------------------------------------------Configuration for NGEN attribute dataset.(https://lynker-spatial.s3-us-west-2.amazonaws.com/hydrofabric/v2.2/hfv2.2-data_model.html).
      attr_select_file: '{base_dir}/inputs/attr_config/attr_selection_ngen.csv' #----------------------------------------------------Path to file where selection of attributes to use during regionalization may be found.
      attr_data_file: '{base_dir}/inputs/attr_datasets/ngen/attr_ngen_{domain}.parquet' #--------------------------------------------Path to file where attribute data may be found.
      base_attr_list: ['elevation', 'slope', 'aspect'] #-----------------------------------------------------------------------------Small list of basic attributes during a 2nd round of pairing if no donor is found using the full set of selected attributes during the first round.
    hlr: #---------------------------------------------------------------------------------------------------------------------------Configuration for Hydrologic Landscape Regions (HLR) attribute dataset (https://www.usgs.gov/publications/hydrologic-landscape-regions-united-states).
      attr_select_file: '{base_dir}/inputs/attr_config/attr_selection_hlr.csv' #-----------------------------------------------------Path to file where selection of attributes to use during regionalization may be found.
      attr_data_file: '{base_dir}/inputs/attr_datasets/hlr/attr_hlr_{domain}.parquet' #----------------------------------------------Path to file where attribute data may be found.
      base_attr_list: ['PPT', 'SAND'] #----------------------------------------------------------------------------------------------Small list of basic attributes during a 2nd round of pairing if no donor is found using the full set of selected attributes during the first round.
    streamcat: #---------------------------------------------------------------------------------------------------------------------Configuration for StreamCat attribute dataset (https://www.epa.gov/national-aquatic-resource-surveys/streamcat-dataset).
      attr_select_file: '{base_dir}/inputs/attr_config/attr_selection_streamcat.csv' #-----------------------------------------------Path to file where selection of attributes to use during regionalization may be found.
      attr_data_file: '{base_dir}/inputs/attr_datasets/streamcat/attr_streamcat_{domain}.parquet' #----------------------------------Path to file where attribute data may be found.
      base_attr_list: ['Precip_Minus_EVT', 'Elev', 'BFI'] #--------------------------------------------------------------------------Small list of basic attributes during a 2nd round of pairing if no donor is found using the full set of selected attributes during the first round.
  snow_cover: #----------------------------------------------------------------------------------------------------------------------Configuration for snow cover data to be used in determining whether catchments are snow-driven.
    consider_snowness: True #--------------------------------------------------------------------------------------------------------Whether to consider snow driven and non-snow driven catchments separately in the regionalization process. If True, snow-driven receivers will only consider snow-driven donors and non-snow-driven receivers will only consider non-snow-driven donors.
    snow_cover_file: 'vpu{vpu_list}_snow_frac.parquet' #-----------------------------------------------------------------------------Path to the snow cover data file, or a dictionary with VPU as keys and file paths as values.
    column: 'snow_pc_hydroatlas' #---------------------------------------------------------------------------------------------------Column name in the snow cover data file that contains the snow cover percentage.
    threshold: '20' #----------------------------------------------------------------------------------------------------------------Threshold value for snow cover percentage to determine if a catchment is considered snow-driven.
  output: #--------------------------------------------------------------------------------------------------------------------------Configuration for parameter regionalization output.
    pairs: #-------------------------------------------------------------------------------------------------------------------------Configuration for saving donor-receiver pairs.
      save: True #-------------------------------------------------------------------------------------------------------------------Whether to save output files
      path: '{base_dir}/outputs/{run_name}/pairs' #----------------------------------------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
      stem: 'pairs_{algorithm_list}_{domain}_vpu{vpu_list}' #------------------------------------------------------------------------File stem for output files, used to create unique file names based on the path.
      stem_suffix: '_mswm' #---------------------------------------------------------------------------------------------------------Suffix for the file stem, used to create unique file names based on the path for specific needs.
      format: 'parquet' #------------------------------------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
      plots: #-----------------------------------------------------------------------------------------------------------------------Configuration for output plots, if applicable.
        spatial_map: True
        histogram: True
        columns_to_plot: ['distSpatial', 'distAttr']
      plot_path: '{base_dir}/outputs/{run_name}/pairs/plots' #-----------------------------------------------------------------------Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path.
    params: #------------------------------------------------------------------------------------------------------------------------Configuration for saving regionalized parameters.
      save: True #-------------------------------------------------------------------------------------------------------------------Whether to save output files
      path: '{base_dir}/outputs/{run_name}/params' #---------------------------------------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
      stem: 'formulation_params_{algorithm_list}_{domain}_vpu{vpu_list}' #-----------------------------------------------------------File stem for output files, used to create unique file names based on the path.
      format: 'csv' #----------------------------------------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
      plots: #-----------------------------------------------------------------------------------------------------------------------Configuration for output plots, if applicable.
        spatial_map: True
        columns_to_plot: ['MP', 'MFSNO', 'uztwm', 'uzfwm', 'pxtemp', 'plwhc']
      plot_path: '{base_dir}/outputs/{run_name}/params/plots' #----------------------------------------------------------------------Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path.
    attr_data_final: #---------------------------------------------------------------------------------------------------------------("Configuration for saving and plotting final attribute data used in regionalization. Note only selected attributes are saved, and attribute names are prefixed with the name of the corresponding attribute source (e.g., 'Elev' in StreamCat becomes 'streamcat_Elev').",)
      save: True #-------------------------------------------------------------------------------------------------------------------Whether to save output files
      path: '{base_dir}/outputs/{run_name}/attr_data_final' #------------------------------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
      stem: 'attr_{domain}_vpu{vpu_list}' #------------------------------------------------------------------------------------------File stem for output files, used to create unique file names based on the path.
      format: 'parquet' #------------------------------------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
      plots: #-----------------------------------------------------------------------------------------------------------------------Configuration for output plots, if applicable.
        spatial_map: True
        histogram: True
        columns_to_plot: ['streamcat_Elev', 'streamcat_BFI', 'streamcat_Precip_Minus_EVT', 'hlr_PMPE', 'hlr_SAND', 'hlr_TAVE']
      plot_path: '{base_dir}/outputs/{run_name}/attr_data_final/plots' #-------------------------------------------------------------Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path.
    config_final: #------------------------------------------------------------------------------------------------------------------Configuration for saving final configuration file used in regionalization.
      save: True #-------------------------------------------------------------------------------------------------------------------Whether to save output files
      path: '{base_dir}/outputs/{run_name}/config_parreg_final.yaml' #---------------------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
    spatial_distance: #--------------------------------------------------------------------------------------------------------------Configuration for saving spatial distance data.
      save: True #-------------------------------------------------------------------------------------------------------------------Whether to save output files
      path: '{base_dir}/outputs/{run_name}/spatial_distance' #-----------------------------------------------------------------------Path to save output file or files. If a directory, the 'stem' and 'format' must be specified.
      format: 'parquet' #------------------------------------------------------------------------------------------------------------File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file.
  algorithms: #----------------------------------------------------------------------------------------------------------------------Algorithm configuration class.  See specific algorithms for additional arguments.
    algo_general: #------------------------------------------------------------------------------------------------------------------General configurations shared by all regionalization algorithms.
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
    gower: #-------------------------------------------------------------------------------------------------------------------------Configurations for the distance-based algorithm Gower.
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      min_attr_dist: 0.1 #-----------------------------------------------------------------------------------------------------------Minimum attribute distance. If one or more donors have a distance to receiver smaller than this threshold, stop searching.
      max_attr_dist: 0.25 #----------------------------------------------------------------------------------------------------------Maximum attribute distance. Donors with distance to receiver larger than this value are discarded, unless no donor smaller than this threshold is available.
      min_spa_dist: 200.0 #----------------------------------------------------------------------------------------------------------Starting distance (km) to iteratively search for donors in the neighborhood
      zero_spa_dist: 1.0 #-----------------------------------------------------------------------------------------------------------Distance threshold (in km) where receiver adopts a donor directly (i.e., donor/receiver are considered overlapping each other)
    urf: #---------------------------------------------------------------------------------------------------------------------------Configurations for the distance-based algorithm Unsupervised Random Forest (URF)
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      pca: False #-------------------------------------------------------------------------------------------------------------------Whether to perform PCA on the attribute data before building the forest. Preliminary testing indicates limited difference in results with/without PCA.
      n_trees: 500 #-----------------------------------------------------------------------------------------------------------------Number of trees in the random forest.
      max_depth: 3 #-----------------------------------------------------------------------------------------------------------------Maximum depth of each tree. If None, nodes are expanded until all leaves are pure.
      min_attr_dist: 0.1 #-----------------------------------------------------------------------------------------------------------Minimum attribute distance. If one or more donors have a distance to receiver smaller than this threshold, stop searching.
      max_attr_dist: 0.25 #----------------------------------------------------------------------------------------------------------Maximum attribute distance. Donors with distance to receiver larger than this value are discarded, unless no donor smaller than this threshold is available.
      min_spa_dist: 200.0 #----------------------------------------------------------------------------------------------------------Starting distance (km) to iteratively search for donors in the neighborhood
      zero_spa_dist: 1.0 #-----------------------------------------------------------------------------------------------------------Distance threshold (in km) where receiver adopts a donor directly (i.e., donor/receiver are considered overlapping each other)
    kmeans: #------------------------------------------------------------------------------------------------------------------------Configurations for the clustering algorithm K-means
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      n_iter_max: 100 #--------------------------------------------------------------------------------------------------------------Maximum number of iterations for the algorithm.
      init: 'k-means++' #------------------------------------------------------------------------------------------------------------Method for initialization.
      n_init: 3 #--------------------------------------------------------------------------------------------------------------------Number of times the k-means algorithm will be run with different centroid seeds.
    kmedoids: #----------------------------------------------------------------------------------------------------------------------Configurations for the clustering algorithm K-medoids
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      n_iter_max: 100 #--------------------------------------------------------------------------------------------------------------Maximum number of iterations for the algorithm.
      init: 'heuristic' #------------------------------------------------------------------------------------------------------------Method for initialization.
    hdbscan: #-----------------------------------------------------------------------------------------------------------------------('Configurations for the clustering algorithm Hierarchical Density Based Spatial Clustering of Applications with Noise (HDBSCAN)',)
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 20 #--------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria.
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      min_cluster_size: 3 #----------------------------------------------------------------------------------------------------------Minimum size of clusters (to avoid being considered noise)
    birch: #-------------------------------------------------------------------------------------------------------------------------('Configurations for the clustering algorithm Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH)',)
      max_spa_dist: 1500.0 #---------------------------------------------------------------------------------------------------------Maximum spatial distance (km) to consider a donor suitable
      n_donor_max: 3 #---------------------------------------------------------------------------------------------------------------Maximum number of donors to keep that satisfy all criteria
      min_var_pca: 0.8 #-------------------------------------------------------------------------------------------------------------Minimum total variance explained by chosen PCA components
      branching_factor: 50 #---------------------------------------------------------------------------------------------------------Branching factor for the BIRCH algorithm.
      min_thresh: 1.5 #--------------------------------------------------------------------------------------------------------------Minimum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds between min_thresh and max_thresh to identify a suitable threshold.
      max_thresh: 4.0 #--------------------------------------------------------------------------------------------------------------Maximum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds between min_thresh and max_thresh to identify a suitable threshold.
      max_resample: 20 #-------------------------------------------------------------------------------------------------------------Maximum number of resamples.
```

#### parreg Schema (general)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| n_procs | int | Number of processors to use for parallel processing. Set to -1 to use all available processors. | -1 | -1 |
| attr_dataset_list | List[str = ngen \| hlr \| streamcat] | List of attribute dataset names to use. Valid options include 'ngen', 'hlr', 'streamcat'. | ['ngen'] | ['ngen', 'streamcat'] |
| algorithm_list | List[str = gower \| urf \| kmeans \| kmedoids \| hdbscan \| birch] | Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch'). | ['gower'] | ['gower', 'kmeans'] |
| manual_pairings_file | Path \| str \| NoneType | Path to the manual pairings file. If provided, this file will be used to specify manual donor-receiver pairings, overriding the algorithmic selections. | None | pairs_kmeans_conus_vpu09.parquet |

#### parreg Schema (donor)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| buffer_km | float \| NoneType | Size of buffer (in km) around current VPU to identify qualified donors. | 0.0 | 100.0 |
| metric_eval_period | MetricEvalPeriod \| NoneType | Evaluation period of metrics to be used for screening donors. | None | {'col_name': 'eval_period', 'value': 'full'} |
| metric_threshold | Dict[str, MetricThreshold] | Dictionary of metric thresholds to be used for screening donors. Each key is a metric name, and the value is a MetricThreshold object specifying the min, max, and absolute settings. Refer to schema of MetricThreshold for details. | None | {'cor': {'min': 0.4, 'max': None, 'absolute': False}, 'kge': {'min': 0.2, 'max': None, 'absolute': False}} |

#### parreg Schema (metric_eval_period)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| col_name | str \| NoneType | Name of the column in the donor stats file that contains the evaluation period. No filtering by evaluation period if None. | None | evalPeriod |
| value | str \| NoneType | Value of the evaluation period to filter donor stats. No filtering by evaluation period if None. | None | full |

#### parreg Schema (metric_threshold)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| min | float \| NoneType | Minimum threshold for the metric. If None, no minimum threshold is applied. | None | None |
| max | float \| NoneType | Maximum threshold for the metric. If None, no maximum threshold is applied. | None | None |
| absolute | bool \| NoneType | If True, apply the absolute value of the metric before applying the thresholds. | False | False |

#### parreg Schema (attr_datasets_config)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| attr_list | list \| NoneType | List of attributes to use from this dataset. If not provided, attributes will be determined from attr_select_file. Either this field or attr_select_file must be provided.If both are provided, attr_list takes priority. | None | None |
| attr_select_file | Path \| str \| NoneType | Path to file where selection of attributes to use during regionalization may be found. | None | ['attr_selection_ngen.csv'] |
| attr_data_file | Path \| str \| NoneType | Path to file where attribute data may be found. | None | ['attr_ngen_{domain}.parquet'] |
| base_attr_list | list \| NoneType | Small list of basic attributes during a 2nd round of pairing if no donor is found using the full set of selected attributes during the first round. | None | ['elevation', 'slope', 'aspect'] |

#### parreg Schema (attr_datasets)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| ngen | AttrDatasetConfig | Configuration for NGEN attribute dataset.(https://lynker-spatial.s3-us-west-2.amazonaws.com/hydrofabric/v2.2/hfv2.2-data_model.html). | PydanticUndefined | {'attr_list': None, 'attr_select_file': '{base_dir}/inputs/attr_config/attr_selection_ngen.csv', 'attr_data_file': '{base_dir}/inputs/attr_datasets/ngen/attr_ngen_{domain}.parquet', 'base_attr_list': ['elevation', 'slope', 'aspect']} |
| hlr | AttrDatasetConfig | Configuration for Hydrologic Landscape Regions (HLR) attribute dataset (https://www.usgs.gov/publications/hydrologic-landscape-regions-united-states). | PydanticUndefined | {'attr_list': None, 'attr_select_file': '{base_dir}/inputs/attr_config/attr_selection_hlr.csv', 'attr_data_file': '{base_dir}/inputs/attr_datasets/hlr/attr_hlr_{domain}.parquet', 'base_attr_list': ['PPT', 'SAND']} |
| streamcat | AttrDatasetConfig | Configuration for StreamCat attribute dataset (https://www.epa.gov/national-aquatic-resource-surveys/streamcat-dataset). | PydanticUndefined | {'attr_list': None, 'attr_select_file': '{base_dir}/inputs/attr_config/attr_selection_streamcat.csv', 'attr_data_file': '{base_dir}/inputs/attr_datasets/streamcat/attr_streamcat_{domain}.parquet', 'base_attr_list': ['Precip_Minus_EVT', 'Elev', 'BFI']} |

#### parreg Schema (snow_cover)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| consider_snowness | bool \| NoneType | Whether to consider snow driven and non-snow driven catchments separately in the regionalization process. If True, snow-driven receivers will only consider snow-driven donors and non-snow-driven receivers will only consider non-snow-driven donors. | True | True |
| snow_cover_file | Path \| str \| Dict[str, Path \| str] \| NoneType | Path to the snow cover data file, or a dictionary with VPU as keys and file paths as values. | None | vpu{vpu_list}_snow_frac.parquet |
| column | str \| NoneType | Column name in the snow cover data file that contains the snow cover percentage. | snow_pc_hydroatlas | snow_pc_hydroatlas |
| threshold | float \| NoneType | Threshold value for snow cover percentage to determine if a catchment is considered snow-driven. | None | 20 |

#### parreg Schema (algorithms)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| algo_general | AlgoGeneral | General configurations shared by all regionalization algorithms. | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 |
| gower | Gower | Configurations for the distance-based algorithm Gower. | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 min_attr_dist=0.1 max_attr_dist=0.2 min_spa_dist=100.0 zero_spa_dist=1.0 | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 min_attr_dist=0.1 max_attr_dist=0.2 min_spa_dist=100.0 zero_spa_dist=1.0 |
| urf | URF | Configurations for the distance-based algorithm Unsupervised Random Forest (URF) | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 pca=False n_trees=500 max_depth=3 min_attr_dist=None max_attr_dist=None min_spa_dist=None zero_spa_dist=None | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 pca=False n_trees=500 max_depth=3 min_attr_dist=None max_attr_dist=None min_spa_dist=None zero_spa_dist=None |
| kmeans | KMeans | Configurations for the clustering algorithm K-means | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 n_iter_max=100 init='k-means++' n_init=None | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 n_iter_max=100 init='k-means++' n_init=None |
| kmedoids | KMedoids | Configurations for the clustering algorithm K-medoids | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 n_iter_max=None init='heuristic' | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 n_iter_max=None init='heuristic' |
| hdbscan | HDBSCAN | ('Configurations for the clustering algorithm Hierarchical Density Based Spatial Clustering of Applications with Noise (HDBSCAN)',) | max_spa_dist=1000.0 n_donor_max=20 min_var_pca=0.9 min_cluster_size=3 | max_spa_dist=1000.0 n_donor_max=20 min_var_pca=0.9 min_cluster_size=3 |
| birch | Birch | ('Configurations for the clustering algorithm Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH)',) | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 branching_factor=50 min_thresh=1.5 max_thresh=4.0 max_resample=20 | max_spa_dist=1000.0 n_donor_max=3 min_var_pca=0.9 branching_factor=50 min_thresh=1.5 max_thresh=4.0 max_resample=20 |

#### parreg Schema (algo_general)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria | 3 | 3 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |

#### parreg Schema (gower)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria | 3 | 3 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |
| min_attr_dist | float \| NoneType | Minimum attribute distance. If one or more donors have a distance to receiver smaller than this threshold, stop searching. | 0.1 | 0.1 |
| max_attr_dist | float \| NoneType | Maximum attribute distance. Donors with distance to receiver larger than this value are discarded, unless no donor smaller than this threshold is available. | 0.2 | 0.25 |
| min_spa_dist | float \| NoneType | Starting distance (km) to iteratively search for donors in the neighborhood | 100.0 | 200.0 |
| zero_spa_dist | float \| NoneType | Distance threshold (in km) where receiver adopts a donor directly (i.e., donor/receiver are considered overlapping each other) | 1.0 | 1.0 |

#### parreg Schema (kmeans)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria | 3 | 3 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |
| n_iter_max | int \| NoneType | Maximum number of iterations for the algorithm. | 100 | 100 |
| init | str = k-means++ \| random \| NoneType | Method for initialization. | k-means++ | k-means++ |
| n_init | int \| NoneType | Number of times the k-means algorithm will be run with different centroid seeds. | None | 3 |

#### parreg Schema (kmedoids)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria | 3 | 3 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |
| n_iter_max | int \| NoneType | Maximum number of iterations for the algorithm. | None | 100 |
| init | str = random \| heuristic \| k-medoids++ \| build \| NoneType | Method for initialization. | heuristic | heuristic |

#### parreg Schema (birch)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria | 3 | 3 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |
| branching_factor | int \| NoneType | Branching factor for the BIRCH algorithm. | 50 | 50 |
| min_thresh | float \| NoneType | Minimum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds between min_thresh and max_thresh to identify a suitable threshold. | 1.5 | 1.5 |
| max_thresh | float \| NoneType | Maximum threshold for the BIRCH algorithm. The algorithm will iterate through thresholds between min_thresh and max_thresh to identify a suitable threshold. | 4.0 | 4.0 |
| max_resample | int \| NoneType | Maximum number of resamples. | 20 | 20 |

#### parreg Schema (hdbscan)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| max_spa_dist | float \| NoneType | Maximum spatial distance (km) to consider a donor suitable | 1000.0 | 1500.0 |
| n_donor_max | int \| NoneType | Maximum number of donors to keep that satisfy all criteria. | 20 | 20 |
| min_var_pca | float \| NoneType | Minimum total variance explained by chosen PCA components | 0.9 | 0.8 |
| min_cluster_size | int \| NoneType | Minimum size of clusters (to avoid being considered noise) | 3 | 3 |

#### parreg Schema (output)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| pairs | BaseOutputConfig | Configuration for saving donor-receiver pairs. | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/pairs', 'stem': 'pairs_{algorithm_list}_{domain}_vpu{vpu_list}', 'stem_suffix': '_mswm', 'format': 'parquet', 'plots': {'spatial_map': True, 'histogram': True, 'columns_to_plot': ['distSpatial', 'distAttr']}, 'plot_path': '{base_dir}/outputs/{run_name}/pairs/plots'} |
| params | BaseOutputConfig | Configuration for saving regionalized parameters. | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/params', 'stem': 'formulation_params_{algorithm_list}_{domain}_vpu{vpu_list}', 'format': 'csv', 'plots': {'spatial_map': True, 'columns_to_plot': ['MP', 'MFSNO', 'uztwm', 'uzfwm', 'pxtemp', 'plwhc']}, 'plot_path': '{base_dir}/outputs/{run_name}/params/plots'} |
| attr_data_final | BaseOutputConfig | ("Configuration for saving and plotting final attribute data used in regionalization. Note only selected attributes are saved, and attribute names are prefixed with the name of the corresponding attribute source (e.g., 'Elev' in StreamCat becomes 'streamcat_Elev').",) | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/attr_data_final', 'stem': 'attr_{domain}_vpu{vpu_list}', 'format': 'parquet', 'plots': {'spatial_map': True, 'histogram': True, 'columns_to_plot': ['streamcat_Elev', 'streamcat_BFI', 'streamcat_Precip_Minus_EVT', 'hlr_PMPE', 'hlr_SAND', 'hlr_TAVE']}, 'plot_path': '{base_dir}/outputs/{run_name}/attr_data_final/plots'} |
| config_final | BaseOutputConfig | Configuration for saving final configuration file used in regionalization. | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/config_parreg_final.yaml'} |
| spatial_distance | BaseOutputConfig | Configuration for saving spatial distance data. | <factory> | {'save': True, 'path': '{base_dir}/outputs/{run_name}/spatial_distance', 'format': 'parquet'} |

#### parreg Schema (BaseOutputConfig)

| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| save | bool | Whether to save output files | True | True |
| path | Path \| str | Path to save output file or files. If a directory, the 'stem' and 'format' must be specified. | None | None |
| stem | str \| Dict[str, str] \| NoneType | File stem for output files, used to create unique file names based on the path. | None | None |
| stem_suffix | str \| NoneType | Suffix for the file stem, used to create unique file names based on the path for specific needs. | None | None |
| format | str \| NoneType | File format for output files, e.g., 'parquet', 'csv', 'yaml'. If not specified, the path must be a file. | None | None |
| plots | Dict[str, Any] \| NoneType | Configuration for output plots, if applicable. | None | None |
| plot_path | str \| NoneType | Path to save output plots, if applicable. If not specified, plots will be saved in a subfolder 'plots' in the defined output path. | None | None |

:::{toctree}
:maxdepth: 2
:hidden:

General<general>
Formulation Regionalization<formreg>
Parameter Regionalization<parreg>
:::