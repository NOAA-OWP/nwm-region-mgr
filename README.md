# Formulation and Parameter Regionalization for the NextGen Framework
[![Build](https://img.shields.io/github/actions/workflow/status/ngwpc/nwm-region-mgr/ci.yaml?branch=main)](.github/workflows/ci.yml)
[![License: BSD 2-Clause](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/license/bsd-2-clause)
[![Release](https://img.shields.io/github/v/release/ngwpc/nwm-region-mgr)](https://github.com/NGWPC/nwm-region-mgr)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg)
![Linter: Ruff](https://img.shields.io/badge/linter-ruff-orange)

<img src="docs/source/_images/overview.png" alt="overview" width="600"/>


`nwm_region_mgr` is a Python package for identifying optimal model formulations and parameter values in ungauged catchments. It leverages calibration data from gauged catchments to improve hydrologic modeling and forecasting skill across regions, playing a key role in the NextGen and NWM ecosystem.


## Key Features

- **Formulation Regionalization** – Ranks NextGen model formulations for ungauged catchments based on similarity to gauged sites.
- **Parameter Regionalization** – Estimates parameter values by intelligently transferring calibrations across catchments.
- **Clustering Methods** – Groups catchments with shared hydrologic characteristics using multiple clustering approaches.
- **Diagnostic Plots** – Generates clear plots and maps that explain formulation and parameter choices.
- **Scalable Workflows** – Efficiently supports studies from individual watersheds to CONUS-wide applications.
- **Customizable Configurations** – Full control of workflows via human-readable config files.

```bash
cd [NGEN_REG_ROOT]
git clone -b development --recurse-submodules https://github.com/NGWPC/nwm-region-mgr.git
```

## Installation

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


## Usage

### 1) Set up configuration yaml files

Three yaml config files are needed to run regionalization
- **config_general.yaml**: general settings for the overall regionalization process.
- **onfig_formreg.yaml**: specific settings for the formulation regionalization process.
- **config_parreg.yaml**: specific settings for the parameter regionalization process.

Follow the sample config files (nwm_region_mgr/sample_files/configs) to set up the configurations
for your regionalization application as needed.

Sample input data can be downloaded from **s3://ngwpc-dev/Yuqiong.Liu/repos/nwm-region-mgr**


### 2) Run the regionalization script

```bash
python [NGEN_REG_ROOT]/nwm-region-mgr/regionalization.py [COFIG_DIR]
```
Where:
- [NGEN_REG_ROOT] refers to the directory where nwm-region-mgr is installed
- [COFIG_DIR] refers to the directory containing the three config files as noted in 1), e.g.,

```bash
python regionalization.py sample_files/configs
```

## STEP 2: Run NGEN simulation with regionalized parameters

- ### Run with container
  - #### 1. Edit MSWM config template as needed (see [sample template](https://github.com/NGWPC/nwm-region-mgr/blob/development/sample_files/configs/mswm.config.template.docker))
  - #### 2. Edit the [run script](https://github.com/NGWPC/nwm-region-mgr/blob/development/run_ngen_vpu_docker.sh) as needed
  - #### 3. download, load and run the docker image
    ```bash
    # download docker image from s3
    aws s3 cp s3://ngwpc-dev/jeff.wade/docker/mswm.tar.gz mswm.tar.gz
    # unpack
    gunzip mswm.tar.gz
    # load the image
    docker load -i mswm.tar
    # edit docker run script [run_msw_docker.sh](https://github.com/NGWPC/nwm-region-mgr/blob/development/run_msw_docker.sh) as needed
    # and then run the script:
    ./run_msw_docker.sh
    ```
  - #### 4. Run NGEN inside container
    ```bash
    nohup ./run_ngen_vpu_docker.sh > out 2>&1&
    ```
- ### Run natively in workspace
    - #### 1) Install [ngen](https://github.com/NGWPC/ngen) and all submodules in its own venv
        You may want to follow the following Confluence pages:
        - [Clone ngen](https://confluence.nextgenwaterprediction.com/display/NGWPC/Clone+NGWPC+GitHub+Code)
        - [Build ngen](https://confluence.nextgenwaterprediction.com/display/NGWPC/Build+ngen+completely)

    - #### 2) Install [mswm](https://github.com/NGWPC/nwm-msw-mgr) in its own venv

    - #### 3) Activate MSWM venv, e.g.
        ```bash
        source ~/repos/nwm-msw-mgr/venv/bin/activate
        ```
    - #### 4) Set up MSWM configuration as shown in [run_ngen_vpu.sh](https://github.com/NGWPC/nwm-region-mgr/blob/development/run_ngen_vpu.sh)

    - #### 5) Run MSWM and ngen simulation
        ```bash
        cd ~/repos/nwm-region-mgr
        ./run_ngen_vpu.sh
        ```
    - #### 6) Check inputs, outputs and logs
    All input, output and log files from running MSWM and NGEN can be found in *[work_dir]/regionalization/[run_name]/[vpu]*
(as defined in **run_ngen_vpu.sh**)

    - #### 7) If ngen fails at t-route
    Check if all NGEN cat-*.csv and nex-*.csv output files are generated; if yes,
    run t-route separately from the Output directory where ngen outputs are located, e.g.,
        ```bash
        python -m nwm_routing -f -V4 ../Input/vpu_09_troute_config_region.yaml
        ```

## STEP 3: Evaluate NGEN simulation with nwm.verf

### 1) Donwload and install [nwm.verf](https://github.com/NGWPC/nwm-verf)
It is recommentded you install nwm.verf in its own venv. Note [nwm.eval](https://github.com/NGWPC/nwm-eval-mgr) needs to installed as a dependency

### 2) Set up configurations for evaluation
Follow example config at [config_eval.yaml](https://github.com/NGWPC/nwm-region-mgr/blob/development/sample_files/configs/config_eval.yaml)

Check out what metrics are currently supported [here](https://confluence.nextgenwaterprediction.com/display/NGWPC/Forecast+Verification+%28ngen-verf%29%3A+Configuration)

Sample input data can be downloaded from **s3://ngwpc-dev/Yuqiong.Liu/repos/nwm-verf** and are also available in [Github](https://github.com/NGWPC/nwm-verf/tree/development/data)

### 3) Activate venv for nwm.verf
```bash
source ~/repos/nwm-verf/venv/bin/activate
```
### 4) Run evaluation
```bash
python -m nwm.verf config_eval.yaml
```
### 5) Check outputs
Outputs from evaluation can be found in *[output_dir]* as specified in **config_eval.yaml**


## Test regionalization for other VPUs or different formulations

- Create pseudo forcing data by recycling existing forcing files, using this [script](https://github.com/NGWPC/nwm-region-mgr/blob/yliu_NGPWC-6984/util_scripts/run_create_pseudo_forcing_csv.sh)
- Create new pseduo calibration/validation stats for different formulations, using this [script](https://github.com/NGWPC/nwm-region-mgr/blob/yliu_NGPWC-6984/util_scripts/run_create_pseudo_calval_stats.sh)
- Create geopackages for a new VPU using this [script](https://github.com/NGWPC/nwm-region-mgr/blob/yliu_NGPWC-6984/util_scripts/subset_conus_gpkg_by_vpu.py)
- Create gage list files and NGEN divide-gage crosswalk file for a new domain using this [script](https://github.com/NGWPC/nwm-verf/blob/yliu_NGWPC-6986/utils/create_ngen_crosswalk_regionalization.py)
