# Configuration File Builder

Welcome to the Configuration File Builder! The tabs on the left will take you to the builder for each of the specific
config files. Once in the builder, you will be prompted to enter setup information for your regionalization run, or you
can scroll to the bottom to fill in default values.  Once done, hit "download" to save the generated configuration YAML
file to your local system.

Example files and schemas for all configuration fields and subfields are included below.

## config_general.yaml
### Example File
```yaml
general:
  run_name: 'test' #-----------------------------------------------Name of the run, used to create output folders and files.
  domain: 'conus' #------------------------------------------------Which National Water Model Domain this run uses.
  vpu_list: ['09'] #-----------------------------------------------List of vector processing units (VPUs) within the domain or 'all' to process all.
  base_dir: '/root/nwm-region-mgr/data/inputs' #-------------------Path to base directory for input/output files.
  ngen_hydrofabric_file: 'vpu_09.gpkg' #---------------------------Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'}
  gage_divide_cwt_file: 'calib_gage_divide_{domain}.parquet' #-----Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'.
  donor_gage_file: 'gages_nwm4_calib_all.csv' #--------------------Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'.
  calval_stats_file: 'stat_calval_all_{domain}.parquet' #----------Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'.
  calib_param_file: 'sampled_params_{domain}.csv' #----------------Path to file containing calibration parameters for all gages in the domain.
  approach_calib_basins: 'regionalization' #-----------------------Strategy for assigning formulations to calibrated basins.
  id_col: #--------------------------------------------------------Dictionary mapping column names for unique identifiers in all applicable files.
    divide: 'divide_id'
    gage: 'gage_id'
    huc12: 'huc_12'
    vpu: 'vpuid'
    drainage_area: 'areasqkm'
  layer_name: #----------------------------------------------------Dictionary mapping layer names for hydrofabric files.
    huc12: 'WBDSnapshot_National'
    ngen: 'divides'
  logging: #-------------------------------------------------------Logging configuration for the application.
    level: 'DEBUG' #-----------------------------------------------Logging level.
    log_to_file: True #--------------------------------------------Whether to log to a file.
```
### Schema Reference (general)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| run_name | str | Name of the run, used to create output folders and files. | required | test |
| domain | str = conus \| ak \| hi \| prvi | Which National Water Model Domain this run uses. | required | conus |
| vpu_list | List[str] \| str | List of vector processing units (VPUs) within the domain or 'all' to process all. | required | ['09'] |
| base_dir | str | Path to base directory for input/output files. | required | /root/nwm-region-mgr/data/inputs |
| ngen_hydrofabric_file | Path \| str \| Dict[str, Path] \| Dict[str, str] | Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'} | required | vpu_09.gpkg |
| gage_divide_cwt_file | Path \| str | Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'. | required | calib_gage_divide_{domain}.parquet |
| donor_gage_file | Path \| str | Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'. | required | gages_nwm4_calib_all.csv |
| calval_stats_file | Path \| str | Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'. | required | stat_calval_all_{domain}.parquet |
| calib_param_file | Path \| str | Path to file containing calibration parameters for all gages in the domain. | required | sampled_params_{domain}.csv |
| approach_calib_basins | str = regionalization \| summary_score | Strategy for assigning formulations to calibrated basins. | required | regionalization |
| id_col | FieldCrosswalk | Dictionary mapping column names for unique identifiers in all applicable files. | FieldCrosswalk | None |
| layer_name | LayerCrosswalk | Dictionary mapping layer names for hydrofabric files. | LayerCrosswalk | None |
| logging | LoggingConfig | Logging configuration for the application. | LoggingConfig | None |
### Schema Reference (id_col)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| divide | str | No description provided | divide_id | divide_id |
| gage | str | No description provided | gage_id | gage_id |
| huc12 | str | No description provided | huc_12 | huc_12 |
| vpu | str | No description provided | vpuid | vpuid |
| drainage_area | str | No description provided | areasqkm | areasqkm |
### Schema Reference (layer_name)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| huc12 | str | No description provided | WBDSnapshot_National | WBDSnapshot_National |
| ngen | str | No description provided | divides | divides |
### Schema Reference (logging)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| level | str = debug \| info \| warning \| error \| critical | Logging level. | INFO | DEBUG |
| log_to_file | bool | Whether to log to a file. | True | True |
## config_formreg.yaml
### Example File
```yaml
general: #---------------------------------------------------------General settings for the formulation regionalization application.
  run_name: 'test' #-----------------------------------------------Name of the run, used to create output folders and files.
  domain: 'conus' #------------------------------------------------Which National Water Model Domain this run uses.
  vpu_list: ['09'] #-----------------------------------------------List of vector processing units (VPUs) within the domain or 'all' to process all.
  base_dir: '/root/nwm-region-mgr/data/inputs' #-------------------Path to base directory for input/output files.
  ngen_hydrofabric_file: 'vpu_09.gpkg' #---------------------------Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'}
  gage_divide_cwt_file: 'calib_gage_divide_{domain}.parquet' #-----Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'.
  donor_gage_file: 'gages_nwm4_calib_all.csv' #--------------------Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'.
  calval_stats_file: 'stat_calval_all_{domain}.parquet' #----------Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'.
  calib_param_file: 'sampled_params_{domain}.csv' #----------------Path to file containing calibration parameters for all gages in the domain.
  approach_calib_basins: 'regionalization' #-----------------------Strategy for assigning formulations to calibrated basins.
  id_col: #--------------------------------------------------------Dictionary mapping column names for unique identifiers in all applicable files.
    divide: 'divide_id'
    gage: 'gage_id'
    huc12: 'huc_12'
    vpu: 'vpuid'
    drainage_area: 'areasqkm'
  layer_name: #----------------------------------------------------Dictionary mapping layer names for hydrofabric files.
    huc12: 'WBDSnapshot_National'
    ngen: 'divides'
  logging: #-------------------------------------------------------Logging configuration for the application.
    level: 'DEBUG' #-----------------------------------------------Logging level.
    log_to_file: True #--------------------------------------------Whether to log to a file.
  calib_basins_only: False #---------------------------------------Whether to run formulation selection only for calibrated basins (based on summary score).
  consider_cost: False #-------------------------------------------Whether to consider computational costs of formulations in the regionalization process.
output: ''
spatial_unit: #----------------------------------------------------Spatial discretization settings for the application.
  huc_level: 'huc-12' #--------------------------------------------USGS HUC level used for discretization, e.g., 'huc-8'.
  nmin_calib_basin: 5 #--------------------------------------------Minimum number of calibration basins required per spatial unit to consider it valid.
  basin_fill_method: 'upscaling' #---------------------------------Method to handle units with too few calibration basins. Options: 'upscaling', 'nearest-neighbor'.
  best_formulation: #----------------------------------------------Strategy to determine the best formulation for each spatial unit.
    method: 'total_score' #----------------------------------------Method to determine the best formulation, options: 'total_score', 'total_count'.
    type: 'basin' #------------------------------------------------Type of spatial unit for best formulation, options: 'basin', 'divide'.
    tolerance: 0.05 #----------------------------------------------Score tolerance as a fraction of the best score, must be between 0.0 and 1.0.
summary_score: #---------------------------------------------------Summary score computation configuration for the application.
  metrics: #-------------------------------------------------------Dictionary of metrics used in the summary score, keyed by metric name.
    cor:
      upper: 1
      lower: -0.5
      orientation: positive
      weight: 0.25
formulation_cost: #------------------------------------------------Computational cost configuration for each formulation.
```
### Schema Reference (general)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| run_name | str | Name of the run, used to create output folders and files. | required | test |
| domain | str = conus \| ak \| hi \| prvi | Which National Water Model Domain this run uses. | required | conus |
| vpu_list | List[str] \| str | List of vector processing units (VPUs) within the domain or 'all' to process all. | required | ['09'] |
| base_dir | str | Path to base directory for input/output files. | required | /root/nwm-region-mgr/data/inputs |
| ngen_hydrofabric_file | Path \| str \| Dict[str, Path] \| Dict[str, str] | Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'} | required | vpu_09.gpkg |
| gage_divide_cwt_file | Path \| str | Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'. | required | calib_gage_divide_{domain}.parquet |
| donor_gage_file | Path \| str | Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'. | required | gages_nwm4_calib_all.csv |
| calval_stats_file | Path \| str | Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'. | required | stat_calval_all_{domain}.parquet |
| calib_param_file | Path \| str | Path to file containing calibration parameters for all gages in the domain. | required | sampled_params_{domain}.csv |
| approach_calib_basins | str = regionalization \| summary_score | Strategy for assigning formulations to calibrated basins. | required | regionalization |
| id_col | FieldCrosswalk | Dictionary mapping column names for unique identifiers in all applicable files. | FieldCrosswalk | None |
| layer_name | LayerCrosswalk | Dictionary mapping layer names for hydrofabric files. | LayerCrosswalk | None |
| logging | LoggingConfig | Logging configuration for the application. | LoggingConfig | None |
| calib_basins_only | bool | Whether to run formulation selection only for calibrated basins (based on summary score). | False | False |
| consider_cost | bool | Whether to consider computational costs of formulations in the regionalization process. | False | False |
### Schema Reference (spatial_unit)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| huc_level | str = huc-2 \| huc-4 \| huc-6 \| huc-8 \| huc-10 \| huc-12 | USGS HUC level used for discretization, e.g., 'huc-8'. | huc-8 | huc-12 |
| nmin_calib_basin | int | Minimum number of calibration basins required per spatial unit to consider it valid. | 5 | 5 |
| basin_fill_method | str = upscaling \| nearest-neighbor | Method to handle units with too few calibration basins. Options: 'upscaling', 'nearest-neighbor'. | upscaling | upscaling |
| best_formulation | BestFormulation | Strategy to determine the best formulation for each spatial unit. | BestFormulation | None |
### Schema Reference (best_formulation)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| method | str = total_score \| total_count | Method to determine the best formulation, options: 'total_score', 'total_count'. | required | total_score |
| type | str = basin \| divide | Type of spatial unit for best formulation, options: 'basin', 'divide'. | required | basin |
| tolerance | float | Score tolerance as a fraction of the best score, must be between 0.0 and 1.0. | 0.05 | 0.05 |
### Schema Reference (summary_score)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| metrics | Dict[str, MetricConfig] | Dictionary of metrics used in the summary score, keyed by metric name. | required | {'cor': {'upper': 1, 'lower': -0.5, 'orientation': 'positive', 'weight': 0.25}} |
### Schema Reference (metric_eval_period)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| col_name | str | Name of the column in the donor stats file that contains the evaluation period. | required | evalPeriod |
| value | str | Value of the evaluation period to filter the donor stats file. | required | full |
### Schema Reference (metric)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| orientation | str = positive \| negative | Orientation of the metric, either 'positive' or 'negative'. | positive | positive |
| weight | float | Weight of the metric in the summary score, must be between 0.0 and 1.0. | 0.0 | 0.25 |
| absolute | bool | Whether to use the absolute value of the metric for normalization. | False | False |
### Schema Reference (formulation_cost)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
## config_parreg.yaml
### Example File
```yaml
general:
  general: #---------------------------------------------------------General configuration settings specific to parameter regionalization.
    run_name: 'test' #-----------------------------------------------Name of the run, used to create output folders and files.
    domain: 'conus' #------------------------------------------------Which National Water Model Domain this run uses.
    vpu_list: ['09'] #-----------------------------------------------List of vector processing units (VPUs) within the domain or 'all' to process all.
    base_dir: '/root/nwm-region-mgr/data/inputs' #-------------------Path to base directory for input/output files.
    ngen_hydrofabric_file: 'vpu_09.gpkg' #---------------------------Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'}
    gage_divide_cwt_file: 'calib_gage_divide_{domain}.parquet' #-----Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'.
    donor_gage_file: 'gages_nwm4_calib_all.csv' #--------------------Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'.
    calval_stats_file: 'stat_calval_all_{domain}.parquet' #----------Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'.
    calib_param_file: 'sampled_params_{domain}.csv' #----------------Path to file containing calibration parameters for all gages in the domain.
    approach_calib_basins: 'regionalization' #-----------------------Strategy for assigning formulations to calibrated basins.
    id_col: #--------------------------------------------------------Dictionary mapping column names for unique identifiers in all applicable files.
      divide: 'divide_id'
      gage: 'gage_id'
      huc12: 'huc_12'
      vpu: 'vpuid'
      drainage_area: 'areasqkm'
    layer_name: #----------------------------------------------------Dictionary mapping layer names for hydrofabric files.
      huc12: 'WBDSnapshot_National'
      ngen: 'divides'
    logging: #-------------------------------------------------------Logging configuration for the application.
      level: 'DEBUG' #-----------------------------------------------Logging level.
      log_to_file: True #--------------------------------------------Whether to log to a file.
    n_procs: '-1' #--------------------------------------------------Number of processors to use for parallel processing. Set to -1 to use all available processors.
    attr_dataset_list: ['hlr'] #-------------------------------------List of attribute dataset names to use. Valid options include 'ngen', 'hlr'.
    algorithm_list: ['gower', 'kmeans'] #----------------------------Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch').
  output: ''
  donor: #-----------------------------------------------------------Configuration for donor selection.
    buffer_km: 100.0 #-----------------------------------------------Size of buffer (in km) around current VPU to identify qualified donors.
  attr_datasets: #---------------------------------------------------Configuration for attribute datasets that can be used in the regionalization process.
    ngen:
      attr_list: None
      attr_select_file: attr_selection_ngen.csv
      attr_data_file: attr_ngen_{domain}.parquet
      base_attr_list: ['elevation', 'slope', 'aspect']
  snow_cover: #------------------------------------------------------Configuration for snow cover data.
    consider_snowness: False #---------------------------------------Whether to consider snow cover data in the regionalization process.
  algorithms: #------------------------------------------------------Algorithm configuration class.  See specific algorithms for additional arguments.
    algo_general: #--------------------------------------------------Base config for all algorithms.
      min_snow_frac: ''
      max_spa_dist: ''
      max_attr_diff: ''
      n_donor_max: ''
      min_var_pca: ''
```
### Schema Reference (general)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| run_name | str | Name of the run, used to create output folders and files. | required | test |
| domain | str = conus \| ak \| hi \| prvi | Which National Water Model Domain this run uses. | required | conus |
| vpu_list | List[str] \| str | List of vector processing units (VPUs) within the domain or 'all' to process all. | required | ['09'] |
| base_dir | str | Path to base directory for input/output files. | required | /root/nwm-region-mgr/data/inputs |
| ngen_hydrofabric_file | Path \| str \| Dict[str, Path] \| Dict[str, str] | Path to NextGen hydrofabric file. Can be: 1) a single file path (Path or str), e.g., 'vpu_01.gpkg' or 2) a dictionary mapping VPU strings to file paths, e.g., {'09': 'vpu_09.gpkg'} | required | vpu_09.gpkg |
| gage_divide_cwt_file | Path \| str | Path to CSV or parquet file with gage divide CWTs, with columns 'divide_id' and 'gage_id'. | required | calib_gage_divide_{domain}.parquet |
| donor_gage_file | Path \| str | Path to CSV file with donor gage information, including 'gage_id', 'longitude', and 'latitude'. | required | gages_nwm4_calib_all.csv |
| calval_stats_file | Path \| str | Path to file with calibration/validation statistics, e.g., 'stat_calval_all_conus.parquet'. | required | stat_calval_all_{domain}.parquet |
| calib_param_file | Path \| str | Path to file containing calibration parameters for all gages in the domain. | required | sampled_params_{domain}.csv |
| approach_calib_basins | str = regionalization \| summary_score | Strategy for assigning formulations to calibrated basins. | required | regionalization |
| id_col | FieldCrosswalk | Dictionary mapping column names for unique identifiers in all applicable files. | FieldCrosswalk | None |
| layer_name | LayerCrosswalk | Dictionary mapping layer names for hydrofabric files. | LayerCrosswalk | None |
| logging | LoggingConfig | Logging configuration for the application. | LoggingConfig | None |
| n_procs | int | Number of processors to use for parallel processing. Set to -1 to use all available processors. | 1 | -1 |
| attr_dataset_list | List[str = ngen \| hlr] | List of attribute dataset names to use. Valid options include 'ngen', 'hlr'. | [] | ['hlr'] |
| algorithm_list | List[str = gower \| urf \| kmeans \| kmedoids \| hdbscan \| birch] | Algorithms to use. Valid options ('gower', 'urf', 'kmeans', 'kmedoids', 'hdbscan', 'birch'). | [] | ['gower', 'kmeans'] |
### Schema Reference (donor)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| buffer_km | float \| NoneType | Size of buffer (in km) around current VPU to identify qualified donors. | 0.0 | 100.0 |
### Schema Reference (metric_eval_period)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| col_name | str | Name of the column in the donor stats file that contains the evaluation period. | required | evalPeriod |
| value | str | Value of the evaluation period to filter the donor stats file. | required | full |
### Schema Reference (metric_threshold)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| absolute | bool \| NoneType | If True, apply the absolute value of the metric before applying the thresholds. | False | False |
### Schema Reference (attr_datasets_config)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
### Schema Reference (snow_cover)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| consider_snowness | bool \| NoneType | Whether to consider snow cover data in the regionalization process. | False | False |
### Schema Reference (algorithms)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| algo_general | AlgoGeneral | Base config for all algorithms. | AlgoGeneral | None |
### Schema Reference (algorithm)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| min_snow_frac | float | No description provided | required |  |
| max_spa_dist | float | No description provided | required |  |
| max_attr_diff | Dict[str, float] | No description provided | required |  |
| n_donor_max | int | No description provided | required |  |
| min_var_pca | float | No description provided | required |  |
### Schema Reference (output)
| Field | Type(s) | Description | Default | Example(s) |
| --- | --- | --- | --- | --- |
| save | bool | No description provided | required |  |
| path | Path \| str | No description provided | required |  |



:::{toctree}
:maxdepth: 2
:hidden:

General<general>
Formulation Regionalization<formreg>
Parameter Regionalization<parreg>
:::
