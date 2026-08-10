# User Guide

## Run regionalization with NWM-RTE on INT/EA/UAT Clusters

On the INT/EA/UAT clusters, all software dependencies for regionalization are installed and managed through 
NWM-RTE (Run Time Environment). Follow the steps below to run the regionalization workflow, which includes three steps:
 - formulation & parameter regionalization (via nwm-region-mgr)
 - regionalized NGEN simulation setup (via nwm-mswm-mgr) and execution
 - evaluation of regionalized simulations (via nwm-verf and nwm-eval-mgr)

### Test the sample regionalization workflow

First, make sure you cd to the root directory of nwm-rte, e.g.,

```bash
cd /ngen-app/nwm-rte
```

#### Step 1: Run regionalization
```bash
# run parameter regionalization (this also runs formulation regionalization first, if not done already)
time ./ngen_rte_run_region.sh --parreg

# if only formulation regionalization is desired, use the following command instead
time ./ngen_rte_run_region.sh --formreg
```

#### Step 2: Run NGEN simulation
```bash
time ./ngen_rte_run_region.sh --ngen
```

#### Step 3: Run evaluation
```bash
time ./ngen_rte_run_region.sh --eval
```

#### Alternatively: Run all steps in one command
```bash
time ./ngen_rte_run_region.sh --parreg --ngen --eval
``` 

### Customize and run your own regionalization workflow
 - If necessary/applicable, prepare input data files (e.g., calibration/validation statistics, catchment 
attributes, etc.). Refer to the [Input Data](tech_reference/input_data.rst) subsection for details. 
   - Calibration/validation statistics can be collected from earlier calibration runs using the commands below, which will generate a csv file containing the statistics for all specified calibration job IDs, along with another csv file listing the corresponding calibrated parameter sets. These files can then be used in the regionalization configuration files.
      ```bash
        ngencerf regionalization 609 610 # where 609 and 610 are example calibration job IDs

        # or specify a list of calibration job IDs in a text file
        ngencerf regionalization --id-file job_ids.txt
      ```
 - Adjust configuration files in `configs/` to set up your desired regionalization experiment. Refer to the 
[Configuration](config_builder/index.md) tab for details on each config file and available options.
 - Follow Steps 0-3 above to execute the customized workflow.

### Example application: comparing different regionalization methods
In this section, we will walk through an example application where we compare gower vs. kmeans clustering for 
parameter regionalization in VPU 09, using selected ngen and StreamCat attributes.

#### 0. Prepare configuration files
We will start from the sample workflow above. First save a copy of the sample configuration files in a new folder 
to avoid overwriting the original files, e.g.:

```bash
cp -r configs/ sample_configs/
```

#### 0.1 Update `configs/config_general.yaml`
 - Set **general.vpu_list** to ['09']
 - Set **general.run_id** to a new name: *test1*. This will be used to name the output folder for this experiment
  (e.g., `outputs/region/test1/`)

#### 0.2 Update `configs/config_parreg.yaml`
 - Set **general.attr_dataset_list** to *['ngen','streamcat']* as the attribute datasets for computing catchment similarity
 - Set **general.algorithm_list** to *['gower', 'kmeans']*. This will run parameter regionalization using both algorithms sequentially.
 - Set **donor.buffer_km** to 100 (instead of 200) to use a smaller donor pool for this experiment
 - Select specific attributes from each dataset using the attribution selection file
   - For **ngen**: use the file defined by the field **attr_datasets.ngen.attr_select_file** (e.g., `inputs/region/attr_config/attr_selection_ngen.csv`). Set the **select** column to 1 for desired attributes and to 0 for others. Here we select all available ngen attributes except for centroid_x, centroid_y, impervious, ISLTPY, and IVGTYP.
   - For **streamcat**: use the file defined by the field **attr_datasets.streamcat.attr_select_file** (e.g., `inputs/region/attr_config/attr_selection_streamcat.csv`). Set the **select** column to 1 for desired attributes and to 0 for others. Here we select the following attributes: BFI, DamDens, Perm, RckDep, WtDep, PctCarbResid, PctEolCrs, PctWater, Precip, Tmax, Tmean, Tmin, RdDens, Runoff, Clay, Sand, Precip_Minus_EVT.
   - Alternatively, we can also specify selected attributes directly in the config file by editing the fields **attr_datasets.ngen.attr_list** and **attr_datasets.streamcat.attr_list**, respectively, for ngen and StreamCat. 
 - Set **donor.metric_eval_period.value** to 'valid' to use validation period statistics for donor selection
 - Set **snow_cover.threshold** to 10 to define catchment snowiness category based on 10% (mean annual) snowfall
 - Edit **output.params.plots.columns_to_plot** to include a couple of CFE parameters to visualize spatial patterns (e.g., 'b' and 'slope')
 - Edit **output.attr_data_final.plots.columns_to_plot** to include some selected attributes to visualize spatial patterns. Specifically, 
   - remove the HLR attributes, since HLR is not chosen for this experiment
   - change *streamcat_Elev* to *streamcat_Perm*, since *Elev* is not selected in **attr_datasets.streamcat.attr_list** 
   - add a few ngen attributes: *ngen_slope*, *ngen_aspect*, *ngen_elevation*
    Note here the attribute names should be prefixed by their dataset names (e.g., 'ngen_' or 'streamcat_').
 - Set **algorithm.algo_general.max_spa_dist** to 1000 to limit the maximum spatial distance for donor selection to 1000 km
 - Set **algorithm.gower.max_attr_dist** to 0.3 to allow a larger maximum attribute distance for donor selection when using gower method. Attribute distances ranges from 0 to 1, with smaller values indicating higher similarity.
 - Set **algorithm.kmeans.n_init** to 5 to increase the number of random initializations for more robust clustering results (with slightly increased computational cost).

#### 1. Run regionalization

Run the regionalization step as in Step 1 above, using the updated configuration files in `configs/`.


```bash
time ./ngen_rte_run_region.sh --parreg 
```

Execution time will take 10-20 minutes depending on available computational resources. While running,
intermediate log messages will be printed to the terminal, while also being written to the log file
`outputs/region/test1.log`, as specified in config_general.yaml.

After completion, check the output folder `outputs/region/test1/`, which contains sub-folders for
 - `attr_data_final/`: files and plots for catchment attributes used in regionalization
 - `formulations/`: regionalized formulation files and diagnostic plots
 - `params/`: regionalized formulation and parameter files and plots for each algorithm, with file names indicating the algorithm used
 - `pairs/`: donor-receiver pair files for each algorithm
 - `spatial_distance/`: matrices of spatial distances between receiver (row) and donor (column) catchments
 - `summary_score/`: summary score for all donor candidates
 - `config_formreg_final.yaml` and `config_parreg_final.yaml`: the final (expanded) configuration files used in this run.

See the **Output Directory Structure** subsection in the [Technical Reference](tech_reference/index.md#output-directory-structure) tab for details on output files and plots.

See the [Output Tables](tech_reference/output_data.rst) and [Output Plots](tech_reference/output_plot.rst) subsections in the [Technical Reference](tech_reference/index.md) tab for details on output files and plots.

#### 2. Run NGEN simulations

In this experiment, we will run NGEN simulations using the parameter sets derived from both gower and kmeans methods, respectively. 

First, update the `configs/config_ngen.yaml` file as follows:
 - Set **vpu** to "09"
 - Set **run_name** to *test1*
 - Set **algorithm** to 'gower' for the first run
 - Set **start_time** and **end_time** to define the simulation period (e.g., '2022-10-01T00:00:00' to '2022-10-10T00:00:00'). Here for demonstration purposes we use a 10-day period in October 2022.
 - The other fields can remain unchanged.

Run the NGEN simulation step as in Step 2 above.

```bash
time ./ngen_rte_run_region.sh --ngen
```

After completion, the simulation outputs will be saved in the folder
`data/outputs/ngen/regionalization/test1_gower/vpu09/Output/`, where the streamflow outputs can be found in the file `troute_output_202210010000.nc`. Note that the sub-folder name `test1_gower` includes the run_name (here *test1*) and the algorithm used (here *gower*).

Next, update the `configs/config_ngen.yaml` file again to set **algorithm** to 'kmeans' for the second run, while keeping other fields unchanged. Reun the NGEN simulation step again.

```bash
time ./ngen_rte_run_region.sh --ngen
```

After completion, the simulation outputs will be saved in the folder
`data/outputs/ngen/regionalization/test1_kmeans/vpu09/Output/`, where the streamflow outputs can be found in the file `troute_output_202210010000.nc`.

Depending on available computational resources, each NGEN simulation may take an hour or more to complete.

#### 3. Run evaluation

Finally, we will evaluate the two NGEN simulations against observed streamflow data.

Update the `configs/config_eval.yaml` file as follows:
 - Set **general.location_set_name** to *vpu_09*
 - Set **general.dataset_name** to *[test1_kmeans, test1_gower]*. This defines the names of the two datasets to be evaluated and intercompared, corresponding to the two algorithms used in parameter regionalization.
 - Set **general.nwm_version** to *[ngen, ngen]*. Both simulations use the ngen configuration.
 - Set **general.fcst_start_date** and **general.fcst_end_date** to define the simulation period (e.g., '2022-10-01T00:00:00' to '2022-10-10T00:00:00'), consistent with the simulation period used above. Both fields should be lists with the same length as **dataset_name**.
 - Set **general.eval_start_date** and **general.eval_end_date** to define the evaluation period (e.g., '2022-10-03T00:00:00' to '2022-10-10T00:00:00'). Here we use an 8-day evaluation period starting from October 3, 2022, to allow a 2-day spin-up period. Both fields should be lists with the same length as **dataset_name**.
 - Set **file_paths.output_dir** to point to the directory where evaluation outputs should be saved. Here we add the **run_name** from regionalization `test1` (e.g., '{base_dir}/outputs/eval/test1/{location_set_name}'), to ensure evaluation outputs are also organized by regionalization runs.
 - Update fields in metics and plotting sections as desired. Here we will compute and plot a set of default evaluation metrics: KGE (Kling-Gupta Efficiency), NSE (Nash-Sutcliffe Efficiency), NNSE (Normalized NSE), and Correlation (CORR). Note the **lead_times** fields are not applicable here since we are evaluating simulations.

Note: if you would like explore other configuration options for evaluation, refer to the [nwm.verf documentation](
https://confluence.nextgenwaterprediction.com/spaces/NGWPC/pages/54132769/Forecast+Verification+nwm-verf+Configuration)

Run the evaluation step as in Step 3 above.
```bash
time ./ngen_rte_run_region.sh --eval
```
After completion, evaluation results will be saved in the folder `data/outputs/eval/regionalization/test1/vpu_09/`, including
 - `joined/`: combined observed and simulated streamflow data for all locations in parquet format; each file corresponds to one dataset (i.e., algorithm)
 - `metrics/`: evaluation metrics tables for all locations in parquet format; each file corresponds to one dataset (i.e., algorithm)
 - `plots/ngen_simulation/`: evaluation plots for all locations, comparing the two algorithms
   - `boxplot/`: boxplots of evaluation metrics across all locations
   - `historgram/`: histograms of evaluation metrics across all locations
   - `spatial_map/`: spatial maps of evaluation metrics for each algorithm
 - `test1_gower/ngen_simulation/`: streamflow time series data for all locations using gower method
 - `test1_kmeans/ngen_simulation/`: streamflow time series data for all locations using kmeans method
 - `usgs/`: observed streamflow time series data for all locations
 - `nwm_verf_config_expanded.yaml`: the final (expanded) configuration file used in this run.

Check the metrics and plots to compare/analyze the performance of the two algorithms in parameter regionalization.

## Run nwm_region_mgr in local environment
The steps below walk through package installation and workflow configuration in local (non-containerized) environments.

### Installation

Installing nwm_region_mgr requires

 - Python 3.11
 - Python venv (typically included with Python)
 - git

Since nwm_region_mgr is not currently on PyPI, it must be installed from source. To download this repository, run

```bash
git clone https://github.com/NGWPC/nwm-region-mgr.git
cd nwm-region-mgr
```

To get the most up-to-date code, switch to the development branch.

```bash
git checkout development
```

Next, create a virtual environment to isolate the dependencies of this library from your base Python environment.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

You will then be able to install nwm_region_mgr. There are a few download variants that users may be interested in.

```bash
# Regular package install
pip install .
# Install the package in edit mode (for development)
pip install -e .
# Install the additional dependencies for parameter regionalization
pip install .[parreg]
```

### STEP 1: Run regionalization to produce regionalized parameters and formulations

#### 1) Set up configuration yaml files

Three yaml config files are needed to run regionalization
- **config_general.yaml**: general settings for the overall regionalization process.
- **onfig_formreg.yaml**: specific settings for the formulation regionalization process.
- **config_parreg.yaml**: specific settings for the parameter regionalization process.

Follow the sample config files (nwm_region_mgr/configs) to set up the configurations
for your regionalization application as needed.

Sample input data can be downloaded from **s3://ngwpc-dev/regionalization/inputs**


#### 2) Run the regionalization script

```bash
python [NGEN_REG_ROOT]/nwm-region-mgr/regionalization.py [COFIG_DIR] [REG_TYPE]
```
Where:
- [NGEN_REG_ROOT] refers to the directory where nwm-region-mgr is installed
- [COFIG_DIR] refers to the directory containing the three config files as noted in 1), e.g.,
- [REG_TYPE] refers to the type of regionalization to run, either 'formreg' (formulation regionalization only) or 'region' (parameter regionalization, which also runs formulation regionalization first if not done already). If not specified, the default is 'region'.

```bash
python regionalization.py configs formreg # to run formulation regionalization only
python regionalization.py configs region # to run parameter regionalization (and formulation regionalization if not done already)
```

### STEP 2: Run NGEN simulation with regionalized parameters

To void complications from building ngen and its submodules locally, we recommend you always run NGEN simulation 
with regionalized parameters and formulations from a Docker container. Follow instructions from the **Docker Run Time Environment (RTE)** section above. 

### STEP 3: Evaluate NGEN simulation with nwm.verf

#### 1) Donwload and install [nwm.verf](https://github.com/NGWPC/nwm-verf)
It is recommentded you install nwm.verf in its own venv. Note [nwm.eval](https://github.com/NGWPC/nwm-eval-mgr) needs to installed as a dependency

#### 2) Set up configurations for evaluation
Follow example config at [config_eval.yaml](https://github.com/NGWPC/nwm-region-mgr/blob/development/sample_files/configs/config_eval.yaml)

Check out what metrics are currently supported [here](https://confluence.nextgenwaterprediction.com/display/NGWPC/Forecast+Verification+%28ngen-verf%29%3A+Configuration)

Sample input data can be downloaded from **s3://ngwpc-dev/regionalization/data/inputs/eval** 

#### 3) Activate venv for nwm.verf
```bash
source ~/repos/nwm-verf/venv/bin/activate
```
#### 4) Run evaluation
```bash
python -m nwm.verf config_eval.yaml
```
#### 5) Check outputs
Outputs from evaluation can be found in *[output_dir]* as specified in **config_eval.yaml**



