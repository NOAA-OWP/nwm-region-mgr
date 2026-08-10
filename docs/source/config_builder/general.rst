General Configuration File
=============================================

Fill out the form below to create a parameter regionalization configuration file.
These are general settings for the formulation regionalization application.

.. raw:: html

   <div class="form-card">
    <form class="yaml-export-form" data-filename="config_general">

      <h3>General</h3>

      <form-field label="Run name"
                  name="run_name"
                  type="text"
                  placeholder="test1"
                  tooltip="Name of the run, used to create output folders and files"
                  data-yaml="general.run_name">
      </form-field>

      <form-field label="Domain"
                  name="domain"
                  type="select"
                  options="conus, ak, hi, pr"
                  data-default="conus"
                  tooltip="Define NWM domain"
                  data-yaml="general.domain"
                  required>
      </form-field>

      <form-field label="VPUs to process"
                  name="vpu_list"
                  type="select"
                  options="01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10L, 10U, 11, 12, 13, 14, 15, 16, 17, 18"
                  data-default="01"
                  tooltip="List of VPUs to process"
                  data-yaml="general.vpu_list"
                  multiple>
      </form-field>

      <form-field label="Base directory"
                  name="base_dir"
                  type="text"
                  placeholder="/ngen-app/nwm-region-mgr/data"
                  tooltip="Path to the directory with data and outputs"
                  data-yaml="general.base_dir">
      </form-field>

      <form-field label="NextGen hydrofabric file"
                  name="ngen_hydrofabric_file"
                  type="text"
                  placeholder="{base_dir}/inputs/region/hydrofabric/vpu_divides/vpu_{vpu_list}.gpkg"
                  tooltip="Path to hydrofabric geopackage file"
                  data-yaml="general.ngen_hydrofabric_file">
      </form-field>

      <form-field label="Gage divide cross-walk table file"
                  name="gage_divide_cwt_file"
                  type="text"
                  placeholder="{base_dir}/inputs/region/cwt_divide_gage/calib_gage_divide_{domain}.parquet"
                  tooltip="Path to a cross-walk table for divides and calibration gages"
                  data-yaml="general.gage_divide_cwt_file">
      </form-field>

      <form-field label="Donor gage file"
                  name="donor_gage_file"
                  type="text"
                  placeholder="{base_dir}/inputs/region/gages_nwm4_calib_all.csv"
                  tooltip="Path to a list of donor basins"
                  data-yaml="general.donor_gage_file">
      </form-field>

      <form-field label="Calibration & validation statistics file"
                  name="calval_stats_file"
                  type="text"
                  placeholder="{base_dir}/inputs/region/calval_stats/stat_calval_all_{domain}.parquet"
                  tooltip="Path to file where statistics from calibration and validation are stored"
                  data-yaml="general.calval_stats_file">
      </form-field>

      <form-field label="Regionalization approach for calibrated basins"
                  name="approach_calib_basins"
                  type="select"
                  options="regionalization, summary_score"
                  data-default="regionalization"
                  tooltip="Strategy for assigning formulations and parameters to calibrated basins"
                  data-yaml="general.approach_calib_basins"
                  required>
      </form-field>

      <form-field label="Manual pairing file to override algorithm-based regionalization"
                  name="manual_pairings_file"
                  type="text"
                  placeholder="{base_dir}/inputs/region/manual_pairings/manual_pairings_{domain}.csv"
                  tooltip="Strategy for assigning formulations and parameters to calibrated basins"
                  data-yaml="general.manual_pairings_file"
                  required>
      </form-field>

      <h4>ID Columns</h4>

      <form-field label="Divide"
                  name="divide"
                  type="text"
                  placeholder="divide_id"
                  tooltip="Name of column for catchment ID in all files"
                  data-yaml="general.id_col.divide">
      </form-field>

      <form-field label="Gage"
                  name="gage"
                  type="text"
                  placeholder="gage_id"
                  tooltip="Name of column for calibration basin ID in all files"
                  data-yaml="general.id_col.gage">
      </form-field>

      <form-field label="HUC12"
                  name="huc12"
                  type="text"
                  placeholder="huc_12"
                  tooltip="Name of column for HUC12 ID in all files"
                  data-yaml="general.id_col.huc12">
      </form-field>

      <form-field label="VPU ID"
                  name="vpu"
                  type="text"
                  placeholder="vpuid"
                  tooltip="Name of column for VPU ID in all files"
                  data-yaml="general.id_col.vpu">
      </form-field>

      <form-field label="Donor"
                  name="donor"
                  type="text"
                  placeholder="donor"
                  tooltip="Name of column for donor basin ID in all files"
                  data-yaml="general.id_col.donor">
      </form-field>

      <form-field label="Drainage area"
                  name="drainage_area"
                  type="text"
                  placeholder="areasqkm"
                  tooltip="Name of column for drainage area in all files"
                  data-yaml="general.id_col.drainage_area">
      </form-field>

      <h4>Layer Names</h4>

      <form-field label="NextGen catchments"
                  name="ngen"
                  type="text"
                  placeholder="divides"
                  tooltip="Name of catchments layer in hydrofabric file"
                  data-yaml="general.layer_name.ngen">
      </form-field>

      <form-field label="HUC12"
                  name="huc12"
                  type="text"
                  placeholder="WBDSnapshot_National"
                  tooltip="Name of HUC12 layer in all files"
                  data-yaml="general.layer_name.huc12">
      </form-field>

      <h4>Logging</h4>

      <form-field label="Level"
                  name="level"
                  type="select"
                  options="debug, info, warning, error, critical"
                  data-default="info"
                  tooltip="Logging level"
                  data-yaml="general.logging.level">
      </form-field>

      <form-field label="Log to file"
                  name="log_to_file"
                  type="checkbox"
                  data-yaml="general.logging.log_to_file"
                  data-default="true"
                  tooltip="Whether to log to a file">
      </form-field>

      <form-field label="File"
                  name="file"
                  type="text"
                  placeholder="{base_dir}/logs/{run_name}.log"
                  tooltip="Where to save log file"
                  data-yaml="general.logging.file">
      </form-field>


      <div class="form-actions">
        <button type="button" class="download-yaml btn btn-primary">Download YAML</button>
        <button type="button" class="btn btn-ghost fill-defaults">Fill Defaults</button>
        <button type="reset" class="btn btn-ghost">Reset</button>
      </div>
    </form>
   </div>

  <script>
  tippy('[data-tippy-content]', { theme: 'light', placement: 'right' });
  </script>
