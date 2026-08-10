---
html_theme.sidebar_secondary.remove:
sd_hide_title: true
---

<!-- CSS overrides on the homepage only -->
<style>
.bd-main .bd-content .bd-article-container {
  max-width: 70rem; /* Make homepage a little wider instead of 60em */
}
/* Override all h1 headers except for the hidden ones */
h1:not(.sd-d-none) {
  font-weight: bold;
  font-size: 48px;
  text-align: center;
  margin-bottom: 4rem;
}
/* Override all h3 headers that are not in hero */
h3:not(#hero h3) {
  font-weight: bold;
  text-align: center;
}
</style>

(homepage)=
# NWM Regionalization

# Formulation and Parameter Regionalization for NextGen

![overview](_images/overview.png)

The National Water Model (NWM) NextGen framework is a modular hydrologic modeling system that links compatible models into flexible formulations for different spatial domains. This flexibility makes it challenging to determine which formulations and parameters perform best across regions, particularly in ungauged basins. `nwm_region_mgr` is a Python package that automates this process by using calibration/validation data and various catchment attributes to identify optimal model formulations and parameter sets at the regional scale.

----

# Role in the NWM Ecosystem


![framework](_images/framework.png)

## A critical tool for forecast skill
Hydrologic models benefit strongly from calibration. Tools in this repository
make the most out of limited observational data to intelligently transfer optimal
parameter sets beyond calibrated catchments. This tool depends on data from a calibration and validation
run of NextGen, as well as various catchment attributes characterizing local climate, topography, landcover, 
soil, geology, and anthropogenic influence. Once the tool has been run, the optimal formulation and 
parameter sets may be used by
the [Model Setup Workflow Manager](https://github.com/NGWPC/nwm-msw-mgr) to set up NextGen simulation runs 
and performance may be assessed with [NWM Evaluation Manager](https://github.com/NGWPC/nwm-verf).

----

# Key Features

:::::{grid} 1 1 2 2
:gutter: 5

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/formulation.svg
:::

:::{div} key-features-text
<strong>Formulation Regionalization</strong><br/>
Identifies best-performing NextGen formulation across all catchments (calibrate and uncalibrated) 
using calibration/validation statistics.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/parameterization.svg
:::

:::{div} key-features-text
<strong>Parameterization Regionalization</strong><br/>
Estimates parameter values for uncalibrated catchments by leveraging calibrations from similar calibrated catchments.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/cluster.svg
:::

:::{div} key-features-text
<strong>Clustering</strong><br/>
Multiple methods available to group calibrated catchments into clusters based on shared catchment characteristics.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/cluster.svg
:::

:::{div} key-features-text
<strong>Distance_based</strong><br/>
Multiple methods available to identify similar catchments based on `attribute distance` calculated from catchment characteristics.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/diagnostic.svg
:::

:::{div} key-features-text
<strong>Diagnostic Plots</strong><br/>
Generates plots and maps that explain why specific formulations and parameters were chosen.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/config.svg
:::

:::{div} key-features-text
<strong>Customizable</strong><br/>
Gives users full control over every step through easily editable configuration files.
:::
::::

::::{grid-item-card}
:shadow: none
:class-card: sd-border-0

:::{image} _static/index/scale.svg
:::

:::{div} key-features-text
<strong>Scalable</strong><br/>
Efficiently allocates computational resources to handle workflows from small watersheds up to CONUS-wide analyses.
:::
::::
:::::

:::{toctree}
:maxdepth: 1
:hidden:

User Guide<user_guide.rst>
FAQ<faq.rst>
Configuration<config_builder/index.rst>
Technical Reference <tech_reference/index.md>
API </API/index.rst>
:::
