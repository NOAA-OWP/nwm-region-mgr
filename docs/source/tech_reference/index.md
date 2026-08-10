# Technical Reference

The following pages contain detailed descriptions of process workflow and algorithms.

:::{toctree}
:maxdepth: 1
:caption: Subsections

Formulation Regionalization<formreg>
Parameter Regionalization<parreg>

Input Data<input_data>
Output Tables<output_data>
Output Plots<output_plot>
:::

### Output Directory Structure

```bash
.
├── attr_data_final                     # Catchment-level attribute datasets used for regionalization
│   ├── attr_conus_vpu01.parquet        # Final attribute table for CONUS VPU 01
|   ├── attr_conus_vpu02.parquet        # Final attribute table for CONUS VPU 02
│   └── plots                           # Diagnostic plots summarizing attribute distributions
│       ├── bar_attr_missing_count_conus_vpu01.png   # Bar chart of missing attribute counts (VPU 01)
│       ├── hist_attr_conus_vpu01.png                 # Histogram of attribute distributions (VPU 01)
│       └── map_attr_conus_vpu01.png                  # Spatial visualization of attribute values (VPU 01)
│       ├── bar_attr_missing_count_conus_vpu02.png   # Bar chart of missing attribute counts (VPU 02)
│       ├── hist_attr_conus_vpu02.png                 # Histogram of attribute distributions (VPU 02)
│       └── map_attr_conus_vpu02.png                  # Spatial visualization of attribute values (VPU 02)
├── config_formreg_final.yaml           # Log of configuration settings used for formulation regionalization
├── config_parreg_final.yaml            # Log of configuration settings used for parameter regionalization
├── formulations                        # Selected NextGen formulations (combinations of hydrologic modules)
│   ├── form_conus_vpu01.parquet        # Selected formulations for CONUS VPU 01 divides
│   ├── form_conus_vpu01_pars.parquet   # Selected formulations with optimal parameter values for donor gages in VPU 01
│   ├── form_conus_vpu02.parquet        # Selected formulations for CONUS VPU 02 divides
│   ├── form_conus_vpu02_pars.parquet   # Selected formulations with optimal parameter values for donor gages in VPU 02
│   └── plots                           # Visual diagnostics of formulation selection
│       ├── hist_form_conus_vpu01.png                  # Histogram of formulation frequencies (VPU 01)
│       ├── hist_form_conus_vpu02.png                  # Histogram of formulation frequencies (VPU 02)
│       ├── map_form_conus_vpu01.png                   # Spatial distribution of selected formulations (VPU 01)
│       └── map_form_conus_vpu02.png                   # Spatial distribution of selected formulations (VPU 02)
├── pairs                                   # Donor–receiver catchment pairings based on chosen algorithms
│   ├── pairs_gower_conus_vpu01_mswm.csv    # Donor-receiver pairings for gower to be used by MSWM (VPU 01)
│   ├── pairs_gower_conus_vpu01.parquet     # Donor-receiver pairings for gower (VPU 01)
│   ├── pairs_gower_conus_vpu01_mswm.csv    # Donor-receiver pairings for gower to be used by MSWM (VPU 02)
│   ├── pairs_gower_conus_vpu02.parquet     # Donor-receiver pairings for gower (VPU 02)
│   ├── pairs_kmeans_conus_vpu01_mswm.csv    # Donor-receiver pairings for kmeans to be used by MSWM (VPU 01)
│   ├── pairs_kmeans_conus_vpu01.parquet    # Donor-receiver pairings for kmeans (VPU 01)
│   ├── pairs_kmeans_conus_vpu02_mswm.csv    # Donor-receiver pairings for kmeans to be used by MSWM (VPU 02)
│   ├── pairs_kmeans_conus_vpu02.parquet    # Donor-receiver pairings for kmeans (VPU 02)
│   └── plots                                    # Diagnostics for donor–receiver pairing analysis
│       ├── hist_pairs_gower_conus_vpu01.png     # Histogram of distances between pairs for gower (VPU 01)
│       ├── hist_pairs_gower_conus_vpu02.png     # Histogram of distances between pairs for gower (VPU 02)
│       ├── hist_pairs_kmeans_conus_vpu01.png    # Histogram of distances between pairs for kmeans (VPU 01)
│       ├── hist_pairs_kmeans_conus_vpu02.png    # Histogram of distances between pairs for kmeans (VPU 02)
│       ├── map_donors_conus_vpu01.png           # Map of donor basins (VPU 01)
│       ├── map_donors_conus_vpu02.png           # Map of donor basins (VPU 02)
│       ├── map_pairs_gower_conus_vpu01.png      # Map showing spatial distribution donor–receiver distances (gower, VPU 01)
│       ├── map_pairs_gower_conus_vpu02.png      # Map showing spatial distribution donor–receiver distances (kmeans, VPU 01)
│       ├── map_pairs_kmeans_conus_vpu01.png     # Map showing spatial distribution donor–receiver distances (gower, VPU 01)
│       └── map_pairs_kmeans_conus_vpu02.png     # Map showing spatial distribution donor–receiver distances (kmeans, VPU 02)
├── spatial_distance                             # Purely geographic distances between donor and receiver catchments
│   ├── donor_receiver_dist_conus_vpu01.parquet  # Centroid-to-centroid distances (VPU 01)
│   └── donor_receiver_dist_conus_vpu02.parquet  # Centroid-to-centroid distances (VPU 02)
├── params                                            # Formulation parameters to be used by MSWM
│   ├── plots                                              # spatial visualizations of selected regionalized parameters
    │   ├── map_formulation_params_kmeans_conus_vpu01.png  # spatial map of regionalized parameters (kmeans,VPU 01)
    │   ├── map_formulation_params_kmeans_conus_vpu02.png  # spatial map of regionalized parameters (kmeans,VPU 02)
    │   ├── map_formulation_params_gower_conus_vpu01.png   # spatial map of regionalized parameters (gower, VPU 01)
    │   └── map_formulation_params_gower_conus_vpu02.png   # spatial map of regionalized parameters (gower, VPU 02)
│   ├── formulation_params_gower_conus_vpu01.csv  # Formulation parameter file (gower, VPU 01)
│   ├── formulation_params_gower_conus_vpu02.csv  # Formulation parameter file (gower, VPU 02)
│   ├── formulation_params_kmeans_conus_vpu01.csv  # Formulation parameter file (kmeans, VPU 01)
│   └── formulation_params_kmeans_conus_vpu02.csv # Formulation parameter file (kmeans,VPU 02)
└── summary_score                       # Performance metrics of selected formulations
    ├── plots                           # Visual summaries of formulation performance
    │   ├── hist_score_conus_vpu01.png  # Histogram of formulation summary scores (VPU 01)
    │   ├── hist_score_conus_vpu02.png  # Histogram of formulation summary scores (VPU 02)
    │   ├── map_score_conus_vpu01.png   # Spatial map of formulation summary scores (VPU 01)
    │   └── map_score_conus_vpu02.png    # Spatial map of formulation summary scores (VPU 02)
    ├── score_conus_all_gages.parquet   # Summary scores for all calibrated formulations and basins in CONUS.
    ├── score_conus_vpu01.parquet       # Summary scores for all calibrated formulations and basins in VPU 01.
    └── score_conus_vpu02.parquet       # Summary scores for all calibrated formulations and basins in VPU 02.

```
