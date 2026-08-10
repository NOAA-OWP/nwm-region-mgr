Formulation Regionalization
============================

Introduction
------------

The formulation regionalization process identifies optimal NextGen formulations for calibrated (and/or uncalibrated)
catchments within each spatial unit defined by a given spatial discretization level (e.g., HUC8).

**Required input:**
   - Calibration and validation statistics for all calibration basins within the VPU (and nearby VPUs) for each candidate formulation.
   - NextGen divides hydrofabric (divides layer).
   - HUC12 - ngen catchment mapping.
   - Formulation computational cost data.
   - Configuration file (config_formreg.yaml) specifying the spatial unit for regionalization, metrics to use in summary score calculation, and method for selecting optimal formulation per spatial unit.

See the :doc:`Input Data <input_data>` page for details.

Process
--------
.. figure:: ../_images/formreg/1.png
   :alt: Example formulation regionalization HUC4.
   :height: 450px
   :align: center

   **Figure 1.** Example formulation regionalization for a HUC4.

1. Calculate summary score for every gage within the VPU that has calibration stats (Figure 2).
    - Metrics to use in composite summary score are specified in the config_formreg.yaml
    - Along with the metric, min and max values may be specified.  If none are specified, min and max values are derived from the data. If bounds are specified, values outside the bounds will be clipped to the bounds.
    - Whether to use absolute values for a given metric can be specified in the config_formreg.yaml
    - Direction of "better" metric values must be specified in the config_formreg.yaml
    - Metric weights must be provided in the config_formreg.yaml and sum to 1
    - The summary score for each formulation at each gage is calculated by multiplying each normalized metric by the specified weight and summing them.
2. Select best formulation at each gage (Figure 2).
    - A set of equivalent best formulations are first identified with a tolerance value (specified in config_formreg.yaml).
    - Final best formulation is then selected from the equivalent set, based on whether computational cost is considered.

3. **Optimal formulations are then assigned to all NextGen divides upstream of a given gage (Figure 2).**
Note in Figure 2, NextGen divides are labeled as "HUC12"

.. figure:: ../_images/formreg/2.png
   :alt: Calculating summary scores and selecting the best formulation.
   :height: 450px
   :align: center

   **Figure 2.** Calculating summary scores and selecting the best formulation.

4. **Divides are aggregated by spatial unit specified in spatial_unit.huc_level in config_formreg.yaml (Figure 3).**

.. figure:: ../_images/formreg/3.png
   :alt: Spatial units for aggregation.
   :height: 450px
   :align: center

   **Figure 3.** Spatial units for aggregation (HUC8 here).

5. An optimal formulation is then selected for each spatial unit (Figure 4).
    - If spatial_unit.best_formulation.method is "total_score", summary scores are **aggregated** by formulation across all catchments in the spatial unit and the formulation with the highest value is selected.
    - If spatial_unit.best_formulation.method is "average_score", summary scores are **averaged** by formulation across all catchments in the spatial unit and the formulation with the highest value is selected.

.. figure:: ../_images/formreg/4.png
   :alt: Aggregation to the spatial unit.
   :height: 450px
   :align: center

   **Figure 4.** Aggregation to the spatial unit.

6. Assign formulations to calibrated basins (Figure 5).
    - If general.approach_calib_basins is summary_score, then best formulation for all calibrated divides will be reset to the formulation with the highest summary score for each gage.
    - If general.approach_calib_basins is regionalization, then the best formulation selected for their spatial unit is retained as the best formulation for calibrated divides.

.. figure:: ../_images/formreg/5.png
   :alt: Optional re-designation of formulations at streamgauges.
   :height: 450px
   :align: center

   **Figure 5.** Optional re-designation of formulations at streamgauges.


Notes
-----
- Configuration for formulation regionalization is specified in `config_formreg.yaml`.

- The python module `nwm_region_mgr.formreg` contains functions for performing formulation regionalization.

- Formulation regionalization can be run independently, without requiring parameter regionalization. However,
  parameter regionalization requires formulation regionalization to be completed first.

- If `calib_basins_only` is set to True in the configuration file, only calibrated catchments will be assigned
  formulations. During parameter regionalization, donors will be selected for uncalibrated catchments
  without any formulation constraints, i.e., any calibrated catchment is eligible as a donor. Othwerwise, if
  `calib_basins_only` is set to False, eligible donors will be limited to only those calibrated catchments that
  share the same formulation as the uncalibrated catchment.

- Currently, formulation regionalization relies on calibration/validation statistics only. In the future,
  additional criteria (e.g., physiographic similarity) may be incorporated into the formulation selection process.


.. toctree::
   :maxdepth: 2
