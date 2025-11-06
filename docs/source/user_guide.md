# User Guide

The steps below walk through package installation and workflow configuration.

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

## Configuration Files

Users may control regionalization behavior by adjusting several configuration files.

 - config_general.yaml: contains general settings for the regionalization process.
 - config_formreg.yaml: contains specific settings for the formulation regionalization process.
 - config_parreg.yaml: contains specific settings for the parameter regionalization process.

Examples are available in `sample_files/configs` or they may be developed with the [Config Builder](config_builder/index.md) on this website.

## Executing nwm_region_mgr

To run the regionalization script, you can use the following command.

```bash
python regionalization.py sample_files/configs
```

## Output Structure

```bash
.
├── attr_data_final                     # Catchment-level attribute datasets used for regionalization
│   ├── attr_conus_vpu01.parquet        # Final attribute table for CONUS VPU 01
│   └── plots                           # Diagnostic plots summarizing attribute distributions
│       ├── bar_attr_missing_count_conus_vpu01.png    # Bar chart of missing attribute counts
│       ├── hist_attr_conus_vpu01.png                 # Histogram of attribute distributions
│       └── map_attr_conus_vpu01.png                  # Spatial visualization of attribute values
├── config_formreg_final.yaml           # Log of configuration settings used for formulation regionalization
├── config_parreg_final.yaml            # Log of configuration settings used for parameter regionalization
├── formulations                        # Selected NextGen formulations (combinations of hydrologic models)
│   ├── form_conus_vpu01.parquet        # Selected formulations for CONUS VPU 01 divides
│   ├── form_conus_vpu01_slim.parquet   # Slimmed version containing only essential formulation fields
│   ├── form_conus_vpu02.parquet        # Selected formulations for CONUS VPU 02 divides
│   ├── form_conus_vpu02_slim.parquet   # Slimmed version containing only essential formulation fields
│   └── plots                           # Visual diagnostics of formulation selection
│       ├── hist_form_conus_vpu01.png                  # Histogram of formulation frequencies (VPU 01)
│       ├── hist_form_conus_vpu02.png                  # Histogram of formulation frequencies (VPU 02)
│       ├── map_form_conus_vpu01.png                   # Spatial distribution of selected formulations (VPU 01)
│       └── map_form_conus_vpu02.png                   # Spatial distribution of selected formulations (VPU 02)
├── pairs                               # Donor–receiver catchment pairings based on chosen algorithms
│   ├── pairs_gower_conus_vpu01.parquet # Table of attribute-based similarity scores (VPU 01)
│   └── plots                           # Diagnostics for donor–receiver pairing analysis
│       ├── hist_pairs_gower_conus_vpu01.png            # Histogram of Gower distances between pairs
│       ├── map_donors_conus_vpu01.png                  # Map of donor catchments (VPU 01)
│       └── map_pairs_gower_conus_vpu01.png             # Map showing donor–receiver pair linkages
├── spatial_distance                    # Purely geographic distances between donor and receiver catchments
│   └── donor_receiver_dist_conus_vpu01.parquet          # Centroid-to-centroid distances (VPU 01)
└── summary_score                       # Performance metrics of selected formulations
    ├── plots                           # Visual summaries of formulation performance
    │   ├── hist_score_conus_vpu01.png                   # Histogram of formulation scores (VPU 01)
    │   ├── hist_score_conus_vpu02.png                   # Histogram of formulation scores (VPU 02)
    │   ├── map_score_conus_vpu01.png                    # Spatial map of formulation scores (VPU 01)
    │   └── map_score_conus_vpu02.png                    # Spatial map of formulation scores (VPU 02)
    ├── score_conus_all_gages.parquet   # Combined formulation performance metrics across all gages
    ├── score_conus_vpu01.parquet       # Performance metrics by formulation (VPU 01)
    └── score_conus_vpu02.parquet       # Performance metrics by formulation (VPU 02)

```

