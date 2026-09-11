Schemas
=======

.. _calib_param_file:

calib_param_file
----------------

Calibrated parameters for various modules for all gages in an NWM domain (e.g., CONUS)

Sample file path: ``inputs/region/pseudo_calib_params/sampled_params_conus.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "calibration_run_id", "validation_run_id", "gage_id", "formulation", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "15293", "98987", "01010000", "noah-owp-modular cfe-s smp sft t-route", "2.5681848800643285", "0.3286171733536613", "98.26779571658672", "12.345915915145532", "34.57680991125569", "4.064091503042371", "0.9712745199335464", "3.7414847994010367", "0.0009141315202519", "0.2682757844834037", "0.7532535832349109", "0.4130823012978584", "0.2589183149092599", "0.1352373803701926", "0.0004228761310245", "1.1540687515916113", "0.3326644885346328", "0.8494590266511353", "3.7047342427645367", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "44119", "52906", "01010000", "noah-owp-modular snow-17 lasam t-route", "1.7202166366984653", "0.2830454483663369", "55.7216447075499", "7.395125941680879", "64.91094869284314", "4.532964185028021", "0.839432321093368", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.2549536985740628", "0.1149808945005032", "3395.942668181262", "0.0402573508525195", "1.3993208237988155", "0.1860697866529445", "0.4344457454145048", "2.8034892811290693", "0.1682210213074931", "0.0212834071116516", "0.1391684172778563", "0.7052654753641924", "0.1892796609353877", "1.8393994158286835", "0.8245934418227354", "2.6163411478418066", "85.65653278592669", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "42461", "14785", "01010000", "noah-owp-modular ueb cfe-x smp sft t-route", "1.6984225027876014", "0.1138073585146865", "44.18211099270653", "10.7458769168222", "41.55877300879165", "2.6584257451986466", "0.9894877010479544", "6.451208746356487", "0.0009931305806678", "0.4331962074757012", "0.2281443013468404", "0.2915759136119435", "0.1545028069618073", "0.1101811687158985", "0.00173408132033", "4.603211031471964", "0.9632723151253538", "0.1889839116526389", "0.1175267001634975", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "1.451971818772199", "0.2253714587504531", "2.6267503130197287", "1.0381689683179314", "0.2723324489894099", "0.9878101435547773", "2.104278810378881", "0.0096068438949711", "346.4354100199481", "1291.644609708449", "6.939487504771504", "0.3945507373583731", "0.8990968927991766", "83059.92094090296", "-0.4349516338584633", "2.974069284705172", "4.643406523991181", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - calibration_run_id
     - calibration_run_id
     - int64

   * - validation_run_id
     - validation_run_id
     - int64

   * - gage_id
     - Unique identifier for each calibration gage.
     - object

   * - formulation
     - NextGen formulation calibrated for a given gage (e.g., nom-cfes, nom-sac)
     - object

   * - MFSNO
     - NOM parameter: Melt factor for snow depletion curve
     - float64

   * - CWP
     - NOM parameter: Canopy wind parameter for canopy wind profile formulation
     - float64

   * - VCMX25
     - NOM parameter: Maximum carboxylation at 25 deg C
     - float64

   * - MP
     - NOM parameter: Slope of Ball-Berry conductance relationship
     - float64

   * - RSURF_SNOW
     - NOM parameter: Soil surface resistance for snow
     - float64

   * - RSURF_EXP
     - NOM parameter: Exponent in the resistance equation for soil evaporation
     - float64

   * - SCAMAX
     - NOM parameter: Maximum fractional snow cover area
     - float64

   * - b
     - CFE parameter: beta exponent on Clapp-Hornberger (1978) soil water relations
     - float64

   * - satdk
     - CFE parameter: saturated hydraulic conductivity
     - float64

   * - satpsi
     - CFE parameter: saturated capillary head
     - float64

   * - slope
     - CFE parameter: this factor (0-1) modifies the gradient of the hydraulic head at the soil bottom. 0=no-flow
     - float64

   * - maxsmc
     - CFE parameter: maximum soil moisture content
     - float64

   * - wltsmc
     - CFE parameter: wilting point soil moisture content
     - float64

   * - max_gw_storage
     - CFE parameter: maximum storage in the conceptual reservoir
     - float64

   * - Cgw
     - CFE parameter: the primary outlet coefficient
     - float64

   * - expon
     - CFE parameter: exponent for nonlinear ground water reservoir (1.0 for linear reservoir)
     - float64

   * - Kn
     - CFE parameter: Nash Config param for lateral subsurface runoff (Nash discharge to storage ratio)
     - float64

   * - Klf
     - CFE parameter: Nash Config param - primary reservoir 
     - float64

   * - refkdt
     - CFE parameter: Reference Soil Infiltration Parameter (used in runoff formulation)
     - float64

   * - mfmax
     - snow-17 parameter: maximum non-rain melt factor
     - float64

   * - uadj
     - snow-17 parameter: Average wind function for rain on snow
     - float64

   * - si
     - snow-17 parameter: 	100% snow cover threshold
     - float64

   * - mfmin
     - snow-17 parameter: minimum non-rain melt factor
     - float64

   * - scf
     - snow-17 parameter: Snow Correction Factor
     - float64

   * - nmf
     - snow-17 parameter: maximum negative melt factor
     - float64

   * - tipm
     - snow-17 parameter: Antecedent snow temperature index
     - float64

   * - pxtemp
     - snow-17 parameter: Precipitation vs Snow threshold temperature
     - float64

   * - plwhc
     - snow-17 parameter: percent liquid water holding capacity
     - float64

   * - daygm
     - snow-17 parameter: daily ground melt
     - float64

   * - smcmin
     - lasam parameter: residual water content (theta_r), or the minimum volumetric water content that a soil layer can naturally attain
     - float64

   * - smcmax
     - lasam parameter: the maximum volumetric water content (theta_s) that a soil layer can naturally attain. Must be greater than theta_r
     - float64

   * - van_genuchten_alpha
     - lasam parameter: van_genuchten_alpha
     - float64

   * - van_genuchten_n
     - lasam parameter: van_genuchten_n
     - float64

   * - hydraulic_conductivity
     - lasam parameter: hydraulic_conductivity
     - float64

   * - ponded_depth_max
     - lasam parameter: the maximum amount of ponded water that is allowed to accumulate on the soil surface
     - float64

   * - field_capacity
     - lasam parameter: capillary head corresponding to volumetric water content at which gravity drainage becomes slower
     - float64

   * - df
     - UEB parameter: Drift multiplier
     - float64

   * - cc
     - UEB parameter: Canopy cover fraction
     - float64

   * - hcan
     - UEB parameter: Canopy height
     - float64

   * - lai
     - UEB parameter: Leaf area index
     - float64

   * - subalb
     - UEB parameter: Substrate albedo
     - float64

   * - ems
     - UEB parameter: Emissivity of snow
     - float64

   * - cg
     - UEB parameter: Ground heat capacity
     - float64

   * - zo
     - UEB parameter: Roughness length
     - float64

   * - rho
     - UEB parameter: Snow density
     - float64

   * - rhog
     - UEB parameter: Soil density
     - float64

   * - Ks
     - UEB parameter: Snow saturated hydraulic conductivity
     - float64

   * - de
     - UEB parameter: Thermally active soil depth
     - float64

   * - avo
     - UEB parameter: Visual new snow albedo
     - float64

   * - apr
     - UEB parameter: Atmospheric pressure
     - float64

   * - a_Xinanjiang_inflection_point_parameter
     - CFE-X parameter: Xinanjiang 'a' coefficient when surface_water_partitioning_scheme=Xinanjiang 
     - float64

   * - b_Xinanjiang_shape_parameter
     - CFE-X parameter: Xinanjiang 'b' coefficient when surface_water_partitioning_scheme=Xinanjiang
     - float64

   * - x_Xinanjiang_shape_parameter
     - CFE-X parameter: Xinanjiang 'x' coefficient when surface_water_partitioning_scheme=Xinanjiang 
     - float64

   * - uztwm
     - sac-sma parameter: Maximum upper zone tension water
     - float64

   * - uzfwm
     - sac-sma parameter: Maximum upper zone free water
     - float64

   * - lztwm
     - sac-sma parameter: Maximum lower zone tension water
     - float64

   * - lzfsm
     - sac-sma parameter: Maximum lower zone free water, secondary (aka supplemental)
     - float64

   * - lzfpm
     - sac-sma parameter: Maximum lower zone free water, primary
     - float64

   * - adimp
     - sac-sma parameter: Additional "impervious" area due to saturation
     - float64

   * - uzk
     - sac-sma parameter: Upper zone recession coefficient
     - float64

   * - lzpk
     - sac-sma parameter: Lower zone recession coefficient, primary
     - float64

   * - lzsk
     - sac-sma parameter: Lower zone recession coefficient, secondary (aka supplemental)
     - float64

   * - zperc
     - sac-sma parameter: Minimum percolation rate coefficient
     - float64

   * - rexp
     - sac-sma parameter: Percolation equation exponent
     - float64

   * - pctim
     - sac-sma parameter: Minimum percent impervious area
     - float64

   * - pfree
     - sac-sma parameter: Percent percolating directly to lower zone free wate
     - float64

   * - riva
     - sac-sma parameter: Percent of the basin that is riparian area
     - float64

   * - side
     - sac-sma parameter: Portion of the baseflow which does not go to the stream
     - float64




.. _calval_stats_file:

calval_stats_file
-----------------

Calibration and validation statistics for all gages in an NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/calval_stats/stat_calval_all_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "calibration_run_id", "validation_run_id", "formulation", "gage_id", "evalPeriod", "CSI", "Corr", "EVBIAS", "FAR", "KGE", "NSE", "NSELog", "NSEWt", "PBIAS", "PKBIAS", "PKTE", "POD", "RMSE"
   "93153", "62433", "noah-owp-modular cfe-s smp sft t-route", "01010000", "calib", "0.423426455738808", "0.688672993019667", "59.5400169741716", "0.467174925878865", "0.683557516268751", "0.352110886451316", "0.289938317202322", "0.3210246018268189", "-4.22313711118399", "120.710086685077", "8.1", "0.6734475374732329", "6.340465322534651"
   "26202", "22408", "noah-owp-modular cfe-s smp sft t-route", "01010000", "full", "0.393473684210526", "0.6929937073565079", "59.6583445486478", "0.3853995396251229", "0.654327254839115", "0.3606695975617929", "-0.0769408622647187", "0.141864367648537", "-15.5504575885424", "118.327573987421", "7.63414634146341", "0.522358859698155", "5.76809385974621"
   "15022", "68621", "noah-owp-modular cfe-s smp sft t-route", "01010000", "valid", "0.3434513771781899", "0.712848487187317", "38.3862353237379", "0.101470588235294", "0.527757083492435", "0.388788333058551", "-0.575071079915985", "-0.0931413734287169", "-37.4902702855678", "109.960685728188", "8.04", "0.3573099415204679", "4.54614536935466"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - calibration_run_id
     - calibration_run_id
     - int64

   * - validation_run_id
     - validation_run_id
     - int64

   * - formulation
     - NextGen formualtion calibrated for a given gage
     - object

   * - gage_id
     - Unique identifier for each gage
     - object

   * - evalPeriod
     - Evaluation period for the statistics (e.g., calibration, validation, and full periods)
     - object

   * - CSI
     - CSI
     - float64

   * - Corr
     - Corr
     - float64

   * - EVBIAS
     - EVBIAS
     - float64

   * - FAR
     - FAR
     - float64

   * - KGE
     - KGE
     - float64

   * - NSE
     - NSE
     - float64

   * - NSELog
     - NSELog
     - float64

   * - NSEWt
     - NSEWt
     - float64

   * - PBIAS
     - PBIAS
     - float64

   * - PKBIAS
     - PKBIAS
     - float64

   * - PKTE
     - PKTE
     - float64

   * - POD
     - POD
     - float64

   * - RMSE
     - RMSE
     - float64




.. _divide_huc12_cwt_file:

divide_huc12_cwt_file
---------------------

Catchment to HUC12 mapping file used in formulation regionalization. Each catchment may overlap with multiple HUC12 watersheds. It is desirable for the total overlap percentage for any given catchment to be as close to 100% as possible.

Sample file path: ``inputs/region/cwt_divide_huc12/cwt_huc12_divide_conus.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "huc_12", "overlap_area", "area_sqkm", "original_area", "overlap_percentage", "nearest_dist_m"
   "1285298364192153.0", "11000060403.0", "3.78", "3.82", "3.82", "98.95", "nan"
   "1285786005972482.0", "11000060403.0", "2.97", "3.0", "3.0", "98.93", "nan"
   "1285786037482086.0", "11000060403.0", "3.87", "4.62", "3.88", "99.51", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - int64

   * - huc_12
     - 12-digit Hydrologic Unit Code (HUC12) representing the watershed in which the catchment is located.
     - int64

   * - overlap_area
     - Area of overlap between the catchment and the HUC12 watershed.
     - float64

   * - area_sqkm
     - Area of the catchment in square kilometers.
     - float64

   * - original_area
     - Original area of the catchment before any processing or adjustments.
     - float64

   * - overlap_percentage
     - Percentage of the catchment area that overlaps with the HUC12 watershed.
     - float64

   * - nearest_dist_m
     - Nearest distance in meters between the catchment and the HUC12 watershed, when there is no overlap.
     - float64




.. _donor_gage_file:

donor_gage_file
---------------

List of all calibration gages accross all NWM domains. Note list of potential donor gages can be a subset of this list, depending on gages included in the cal/val stats file.

Sample file path: ``inputs/region/gages_nwm4_calib_all.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "nws_id", "agency", "station_name", "domain", "domain_id", "nwm_v3_calibration", "headwater_calibration", "latitude", "longitude"
   "01021480", "WSLM1", "USGS", "Old Stream near Wesley, Maine", "CONUS", "3", "True", "True", "44.9369444", "-67.7361111"
   "01029200", "SBSM1", "USGS", "Seboeis River near Shin Pond, Maine", "CONUS", "3", "True", "True", "46.14305556", "-68.6336111"
   "01029500", "GRNM1", "USGS", "East Branch Penobscot River at Grindstone, Maine", "CONUS", "3", "True", "True", "45.73027778", "-68.5894444"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each gage.
     - object

   * - nws_id
     - National Weather Service (NWS) gage identifier.
     - object

   * - agency
     - Agency responsible for the gage.
     - object

   * - station_name
     - Name of the gage station.
     - object

   * - domain
     - Hydrologic domain of the gage.
     - object

   * - domain_id
     - Identifier for the hydrologic domain.
     - int64

   * - nwm_v3_calibration
     - Indicates if the gage was used in NWM version 3 calibration.
     - bool

   * - headwater_calibration
     - Indicates if the gage is part of headwater calibration for NWM version 4.
     - bool

   * - latitude
     - Latitude of the gage location.
     - float64

   * - longitude
     - Longitude of the gage location.
     - float64




.. _formulation_cost:

formulation_cost
----------------

File containing computational costs (in seconds) for all formulations being evaluated.

Sample file path: ``inputs/region/formulation_costs_secs_per_catchment.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "formulation", " cost"
   "noah-owp-modular cfe-s t-route", "10"
   "noah-owp-modular cfe-s smp sft t-route", "15"
   "noah-owp-modular cfe-x t-route", "10"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - formulation
     - Name of the NextGen formulation being evaluated.
     - object

   * -  cost
     -  cost
     - int64




.. _gage_divide_cwt_file:

gage_divide_cwt_file
--------------------

Crosswalk table linking gages to catchments (i.e., divides).

Sample file path: ``inputs/region/cwt_divide_gage/calib_gage_divide_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "div_id", "area_sqkm", "vpu_id", "type"
   "05132000", "1279133717154269", "5.913000080998901", "09", "connectors"
   "05132000", "1279133768153088", "8.120700193500578", "09", "aggregate"
   "05132000", "1279132525241086", "6.0430497209997895", "09", "independent"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each gage.
     - object

   * - div_id
     - Unique identifier for each catchment.
     - string

   * - area_sqkm
     - Area of the catchment in square kilometers.
     - float64

   * - vpu_id
     - VPU the catchment belongs to.
     - object

   * - type
     - Type of catchment (e.g., connector, aggregate, independent).
     - object




.. _hlr-attr_data_file:

hlr.attr_data_file
------------------

File containing HLR attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/hlr/attr_hlr_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "AQPERMNEW", "SLOPE", "TAVE", "PPT", "PET", "PMPE", "SAND", "MINELE", "RELIEF", "PFLATTOT", "PFLATLOW", "PFLATUP"
   "1064370865799041", "1.0", "3.84021997452", "64.71099853516", "15.38490009308", "38.42850112915", "-23.0436000824", "36.46089935303", "752.0", "1072.0", "53.0", "53.0", "0.0"
   "1064370922315354", "1.0", "3.84021997452", "64.71099853516", "15.384900093080002", "38.42850112915", "-23.0436000824", "36.46089935303", "752.0", "1072.0", "53.0", "53.0", "0.0"
   "1064370926577410", "1.0", "3.8402199745199996", "64.71099853516", "15.38490009308", "38.42850112915", "-23.0436000824", "36.46089935303", "752.0", "1072.0", "53.0", "53.0", "0.0"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - string

   * - AQPERMNEW
     - aquifer permeability
     - float64

   * - SLOPE
     - mean slope
     - float64

   * - TAVE
     - mean annual temperature
     - float64

   * - PPT
     - mean annual precipitation
     - float64

   * - PET
     - mean annual potential evaporatranspiration
     - float64

   * - PMPE
     - mean annual precpitation minus PET
     - float64

   * - SAND
     - percentage of sand in the soil
     - float64

   * - MINELE
     - minimum elevation
     - float64

   * - RELIEF
     - relief
     - float64

   * - PFLATTOT
     - total percentage of flatland
     - float64

   * - PFLATLOW
     - percentage of flatland in the lowland area
     - float64

   * - PFLATUP
     - percentage of flatland in the upland area
     - float64




.. _hlr-attr_select_file:

hlr.attr_select_file
--------------------

File to configure the selection of HLR attributes for parameter regionalization.

Sample file path: ``inputs/region/attr_config/attr_selection_hlr.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "select", "attr_name", "description"
   "1", "AQPERMNEW", "Mean aquifer permeability (cm/hour) of soils (STATSGO) within catchment."
   "1", "SLOPE", "Mean slope (%) of catchment."
   "1", "TAVE", "Mean annual temperature (°C) within catchment."

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - select
     - Whether to select this attribute for parameter regionalization (1 for yes, 0 for no).
     - int64

   * - attr_name
     - Name of the HLR attribute to be selected for parameter regionalization.
     - object

   * - description
     - Description of the HLR attribute.
     - object




.. _hydroatlas-attr_data_file:

hydroatlas.attr_data_file
-------------------------

File containing HydroATLAS attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/hydroatlas/attr_hydroatlas_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "dis_m3_pyr", "dis_m3_pmn", "dis_m3_pmx", "run_mm_syr", "inu_pc_smn", "inu_pc_umn", "inu_pc_smx", "inu_pc_umx", "inu_pc_slt", "inu_pc_ult", "lka_pc_sse", "lka_pc_use", "lkv_mc_usu", "rev_mc_usu", "dor_pc_pva", "ria_ha_ssu", "ria_ha_usu", "riv_tc_ssu", "riv_tc_usu", "gwt_cm_sav", "ele_mt_sav", "ele_mt_uav", "ele_mt_smn", "ele_mt_smx", "slp_dg_sav", "slp_dg_uav", "sgr_dk_sav", "clz_cl_smj", "cls_cl_smj", "tmp_dc_syr", "tmp_dc_uyr", "tmp_dc_smn", "tmp_dc_smx", "tmp_dc_s01", "tmp_dc_s02", "tmp_dc_s03", "tmp_dc_s04", "tmp_dc_s05", "tmp_dc_s06", "tmp_dc_s07", "tmp_dc_s08", "tmp_dc_s09", "tmp_dc_s10", "tmp_dc_s11", "tmp_dc_s12", "pre_mm_syr", "pre_mm_uyr", "pre_mm_s01", "pre_mm_s02", "pre_mm_s03", "pre_mm_s04", "pre_mm_s05", "pre_mm_s06", "pre_mm_s07", "pre_mm_s08", "pre_mm_s09", "pre_mm_s10", "pre_mm_s11", "pre_mm_s12", "pet_mm_syr", "pet_mm_uyr", "pet_mm_s01", "pet_mm_s02", "pet_mm_s03", "pet_mm_s04", "pet_mm_s05", "pet_mm_s06", "pet_mm_s07", "pet_mm_s08", "pet_mm_s09", "pet_mm_s10", "pet_mm_s11", "pet_mm_s12", "aet_mm_syr", "aet_mm_uyr", "aet_mm_s01", "aet_mm_s02", "aet_mm_s03", "aet_mm_s04", "aet_mm_s05", "aet_mm_s06", "aet_mm_s07", "aet_mm_s08", "aet_mm_s09", "aet_mm_s10", "aet_mm_s11", "aet_mm_s12", "ari_ix_sav", "ari_ix_uav", "cmi_ix_syr", "cmi_ix_uyr", "cmi_ix_s01", "cmi_ix_s02", "cmi_ix_s03", "cmi_ix_s04", "cmi_ix_s05", "cmi_ix_s06", "cmi_ix_s07", "cmi_ix_s08", "cmi_ix_s09", "cmi_ix_s10", "cmi_ix_s11", "cmi_ix_s12", "snw_pc_syr", "snw_pc_uyr", "snw_pc_smx", "snw_pc_s01", "snw_pc_s02", "snw_pc_s03", "snw_pc_s04", "snw_pc_s05", "snw_pc_s06", "snw_pc_s07", "snw_pc_s08", "snw_pc_s09", "snw_pc_s10", "snw_pc_s11", "snw_pc_s12", "glc_cl_smj", "glc_pc_s01", "glc_pc_s02", "glc_pc_s03", "glc_pc_s04", "glc_pc_s05", "glc_pc_s06", "glc_pc_s07", "glc_pc_s08", "glc_pc_s09", "glc_pc_s10", "glc_pc_s11", "glc_pc_s12", "glc_pc_s13", "glc_pc_s14", "glc_pc_s15", "glc_pc_s16", "glc_pc_s17", "glc_pc_s18", "glc_pc_s19", "glc_pc_s20", "glc_pc_s21", "glc_pc_s22", "glc_pc_u01", "glc_pc_u02", "glc_pc_u03", "glc_pc_u04", "glc_pc_u05", "glc_pc_u06", "glc_pc_u07", "glc_pc_u08", "glc_pc_u09", "glc_pc_u10", "glc_pc_u11", "glc_pc_u12", "glc_pc_u13", "glc_pc_u14", "glc_pc_u15", "glc_pc_u16", "glc_pc_u17", "glc_pc_u18", "glc_pc_u19", "glc_pc_u20", "glc_pc_u21", "glc_pc_u22", "pnv_cl_smj", "pnv_pc_s01", "pnv_pc_s02", "pnv_pc_s03", "pnv_pc_s04", "pnv_pc_s05", "pnv_pc_s06", "pnv_pc_s07", "pnv_pc_s08", "pnv_pc_s09", "pnv_pc_s10", "pnv_pc_s11", "pnv_pc_s12", "pnv_pc_s13", "pnv_pc_s14", "pnv_pc_s15", "pnv_pc_u01", "pnv_pc_u02", "pnv_pc_u03", "pnv_pc_u04", "pnv_pc_u05", "pnv_pc_u06", "pnv_pc_u07", "pnv_pc_u08", "pnv_pc_u09", "pnv_pc_u10", "pnv_pc_u11", "pnv_pc_u12", "pnv_pc_u13", "pnv_pc_u14", "pnv_pc_u15", "wet_cl_smj", "wet_pc_sg1", "wet_pc_ug1", "wet_pc_sg2", "wet_pc_ug2", "wet_pc_s01", "wet_pc_s02", "wet_pc_s03", "wet_pc_s04", "wet_pc_s05", "wet_pc_s06", "wet_pc_s07", "wet_pc_s08", "wet_pc_s09", "wet_pc_u01", "wet_pc_u02", "wet_pc_u03", "wet_pc_u04", "wet_pc_u05", "wet_pc_u06", "wet_pc_u07", "wet_pc_u08", "wet_pc_u09", "for_pc_sse", "for_pc_use", "crp_pc_sse", "crp_pc_use", "pst_pc_sse", "pst_pc_use", "ire_pc_sse", "ire_pc_use", "gla_pc_sse", "gla_pc_use", "prm_pc_sse", "prm_pc_use", "pac_pc_sse", "pac_pc_use", "tbi_cl_smj", "tec_cl_smj", "fmh_cl_smj", "fec_cl_smj", "cly_pc_sav", "cly_pc_uav", "slt_pc_sav", "slt_pc_uav", "snd_pc_sav", "snd_pc_uav", "soc_th_sav", "soc_th_uav", "swc_pc_syr", "swc_pc_uyr", "swc_pc_s01", "swc_pc_s02", "swc_pc_s03", "swc_pc_s04", "swc_pc_s07", "swc_pc_s08", "swc_pc_s09", "swc_pc_s10", "swc_pc_s11", "swc_pc_s12", "lit_cl_smj", "kar_pc_sse", "kar_pc_use", "ero_kh_sav", "ero_kh_uav", "pop_ct_ssu", "pop_ct_usu", "ppd_pk_sav", "ppd_pk_uav", "urb_pc_sse", "urb_pc_use", "nli_ix_sav", "nli_ix_uav", "rdd_mk_sav", "rdd_mk_uav", "hft_ix_s93", "hft_ix_u93", "hft_ix_s09", "hft_ix_u09", "gad_id_smj", "gdp_ud_sav", "gdp_ud_ssu", "gdp_ud_usu", "hdi_ix_sav"
   "1062397347513500", "0.253", "0.015", "0.8380000000000001", "16.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "7.811", "12.798", "17.306", "23.528", "670.0", "1567.9999999999998", "2043.0", "819.0", "2461.0", "181.0", "169.0", "336.0", "13.999999999999998", "88.0", "180.0", "155.0", "136.0", "216.0", "136.0", "149.0", "165.0", "187.0", "207.0", "216.0", "213.0", "212.0", "200.0", "180.0", "159.0", "141.0", "555.0", "582.0", "20.0", "17.0", "13.999999999999998", "35.0", "58.0", "74.0", "57.0", "79.0", "105.0", "54.0", "21.0", "21.0", "1578.0", "1456.0", "88.0", "96.0", "133.0", "150.0", "174.0", "172.99999999999997", "174.0", "165.0", "136.0", "114.0", "92.0", "84.0", "470.0", "493.0", "27.999999999999996", "27.0", "31.0", "32.0", "40.0", "46.0", "48.99999999999999", "51.0", "53.0", "48.0", "36.0", "29.0", "35.0", "41.0", "-65.0", "-59.0", "-77.0", "-82.0", "-88.99999999999999", "-77.0", "-66.0", "-57.0", "-67.0", "-52.0", "-23.0", "-53.0", "-77.0", "-75.0", "0.0", "0.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "4.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "97.99999999999999", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.0", "0.0", "0.0", "0.0", "37.0", "0.0", "0.0", "0.0", "34.0", "0.0", "0.0", "29.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "24.0", "0.0", "0.0", "0.0", "61.0", "2.0", "0.0", "13.0", "0.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "97.99999999999999", "5.0", "3.0", "20.0", "15.0", "2.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "3.0", "327.0", "4.0", "138.0", "23.0", "23.0", "30.0", "30.0", "46.0", "48.0", "48.0", "59.0", "31.0", "35.0", "32.0", "29.0", "24.0", "21.0", "27.999999999999996", "30.0", "37.0", "42.0", "39.0", "35.0", "3.0", "100.0", "100.0", "7895.0", "4929.0", "0.676", "1.898", "3.9909999999999997", "5.171", "0.0", "0.0", "159.0", "100.0", "162.0", "177.0", "31.0", "35.0", "25.0", "31.0", "145.0", "29948.0", "38033812.0", "56939232.0", "814.0"
   "1062398455086668", "0.12", "0.011", "0.38600000000000007", "15.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.986", "4.986", "6.222", "6.222", "697.0", "2450.0", "2450.0", "1728.0", "3596.0", "159.0", "159.0", "352.0", "11.0", "71.0", "133.0", "133.0", "95.0", "161.0", "95.0", "103.0", "121.99999999999999", "142.0", "159.0", "161.0", "156.0", "155.0", "148.0", "129.0", "123.00000000000001", "106.0", "605.0", "605.0", "29.0", "22.0", "21.0", "32.0", "63.0", "78.0", "70.0", "84.0", "99.0", "55.99999999999999", "24.999999999999996", "26.0", "1351.0", "1351.0", "74.0", "80.0", "114.0", "131.0", "155.0", "146.0", "142.0", "138.0", "118.0", "98.0", "84.0", "72.0", "513.0", "513.0", "31.000000000000004", "31.000000000000004", "39.0", "39.0", "46.00000000000001", "49.0", "52.0", "55.0", "55.0", "49.0", "39.0", "31.000000000000004", "44.99999999999999", "44.99999999999999", "-55.0", "-55.0", "-60.0", "-72.0", "-81.0", "-75.0", "-60.0", "-46.00000000000001", "-49.99999999999999", "-38.0", "-16.0", "-43.0", "-69.0", "-63.0", "0.0", "0.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.0", "0.0", "0.0", "0.0", "97.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "97.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "8.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "84.0", "4.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "84.0", "4.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "97.0", "97.0", "1.0", "1.0", "10.0", "10.0", "1.0", "1.0", "0.0", "0.0", "0.0", "0.0", "1.0", "1.0", "3.0", "327.0", "4.0", "138.0", "22.0", "22.0", "29.0", "29.0", "49.0", "49.0", "68.0", "68.0", "39.0", "39.0", "42.0", "40.0", "35.0", "30.0", "36.0", "40.0", "46.00000000000001", "49.99999999999999", "47.0", "43.0", "3.0", "99.99999999999999", "99.99999999999999", "2390.0", "2390.0", "1.222", "1.222", "6.181", "6.181", "0.0", "0.0", "84.0", "99.99999999999999", "191.0", "190.0", "37.0", "37.0", "36.0", "36.0", "145.0", "29948.0", "18905430.0", "18905428.0", "814.0"
   "1062398518868817", "0.12", "0.011", "0.386", "15.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.986", "4.986", "6.222", "6.222", "696.9999999999999", "2450.0", "2450.0", "1728.0", "3596.0", "159.0", "159.0", "352.0", "11.0", "71.0", "133.0", "133.0", "95.0", "161.0", "95.0", "103.0", "122.0", "142.0", "159.0", "161.0", "156.0", "155.0", "148.0", "129.0", "123.0", "106.0", "605.0", "605.0", "29.000000000000004", "22.0", "21.0", "32.0", "63.0", "78.0", "70.0", "84.0", "99.0", "56.0", "25.0", "26.0", "1351.0", "1351.0", "74.0", "80.0", "114.0", "131.0", "155.0", "146.0", "142.0", "138.0", "118.0", "98.0", "84.0", "72.0", "513.0", "513.0", "31.000000000000004", "31.000000000000004", "39.0", "39.0", "46.0", "49.0", "52.0", "54.99999999999999", "54.99999999999999", "49.0", "39.0", "31.000000000000004", "45.0", "45.0", "-54.99999999999999", "-54.99999999999999", "-60.0", "-72.0", "-81.0", "-75.0", "-60.0", "-46.0", "-50.0", "-38.0", "-16.0", "-43.00000000000001", "-69.0", "-63.0", "0.0", "0.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.0", "0.0", "0.0", "0.0", "97.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "97.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "8.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "84.0", "4.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "84.0", "4.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "97.00000000000001", "97.00000000000001", "1.0", "1.0", "10.0", "10.0", "1.0", "1.0", "0.0", "0.0", "0.0", "0.0", "1.0", "1.0", "3.0", "327.0", "4.0", "138.0", "22.0", "22.0", "29.000000000000004", "29.000000000000004", "49.0", "49.0", "68.0", "68.0", "39.0", "39.0", "42.0", "40.0", "35.0", "30.0", "36.0", "40.0", "46.0", "50.0", "47.00000000000001", "43.00000000000001", "3.0", "100.0", "100.0", "2390.0", "2390.0", "1.222", "1.222", "6.181", "6.181", "0.0", "0.0", "84.0", "100.0", "191.0", "190.0", "37.0", "37.0", "36.0", "36.0", "145.0", "29948.0", "18905430.0", "18905428.0", "814.0"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - string

   * - dis_m3_pyr
     - annual average natural discharge (m3/year)
     - float64

   * - dis_m3_pmn
     - annual minimum naturaldischarge (m3/month)
     - float64

   * - dis_m3_pmx
     - annual maximum natural discharge (m3/month)
     - float64

   * - run_mm_syr
     - sub-basin annual average land surface runoff (mm/year)
     - float64

   * - inu_pc_smn
     - sub-basin annual minimum inundation extent (percent)
     - float64

   * - inu_pc_umn
     - total watershed annual minimum inundation extent (percent)
     - float64

   * - inu_pc_smx
     - sub-basin annual maximum inundation extent (percent)
     - float64

   * - inu_pc_umx
     - total watershed annual maximum inundation extent (percent)
     - float64

   * - inu_pc_slt
     - sub-basin long-term maximum inundation extent (percent)
     - float64

   * - inu_pc_ult
     - total watershed long-term maximum inundation extent (percent)
     - float64

   * - lka_pc_sse
     - sub-basin lake area (percent)
     - float64

   * - lka_pc_use
     - total watershed lake area (percent)
     - float64

   * - lkv_mc_usu
     - total watershed lake volume (million m3)
     - float64

   * - rev_mc_usu
     - total watershed reservoir volume (million m3)
     - float64

   * - dor_pc_pva
     - sub-basin degree of regulation (percent)
     - float64

   * - ria_ha_ssu
     - sub-basin river area (hectares)
     - float64

   * - ria_ha_usu
     - total watershed river area (hectares)
     - float64

   * - riv_tc_ssu
     - sub-basin river volume (thousand m3)
     - float64

   * - riv_tc_usu
     - total watershed river volume (thousand m3)
     - float64

   * - gwt_cm_sav
     - sub-basin average groundwater table depth (cm)
     - float64

   * - ele_mt_sav
     - sub-basin average elevation (meters above sea level)
     - float64

   * - ele_mt_uav
     - total watershed average elevation (meters above sea level)
     - float64

   * - ele_mt_smn
     - sub-basin minimum elevation (meters above sea level)
     - float64

   * - ele_mt_smx
     - sub-basin maximum elevation (meters above sea level)
     - float64

   * - slp_dg_sav
     - sub-basin average slope (degrees)
     - float64

   * - slp_dg_uav
     - total watershed average slope (degrees)
     - float64

   * - sgr_dk_sav
     - sub-basin stream gradient (decimeters per kilometer)
     - float64

   * - clz_cl_smj
     - sub-basin spatial majority climate zone (classes 18)
     - float64

   * - cls_cl_smj
     - sub-basin spatial majority climate strata (classes 125)
     - float64

   * - tmp_dc_syr
     - sub-basin annual average temperature (degrees C x10)
     - float64

   * - tmp_dc_uyr
     - total watershed annual average temperature (degrees C x10)
     - float64

   * - tmp_dc_smn
     - sub-basin annual minimum temperature (degrees C x10)
     - float64

   * - tmp_dc_smx
     - sub-basin annual maximum temperature (degrees C x10)
     - float64

   * - tmp_dc_s01
     - sub-basin average January temperature (degrees C x10)
     - float64

   * - tmp_dc_s02
     - sub-basin average February temperature (degrees C x10)
     - float64

   * - tmp_dc_s03
     - sub-basin average March temperature (degrees C x10)
     - float64

   * - tmp_dc_s04
     - sub-basin average April temperature (degrees C x10)
     - float64

   * - tmp_dc_s05
     - sub-basin average May temperature (degrees C x10)
     - float64

   * - tmp_dc_s06
     - sub-basin average June temperature (degrees C x10)
     - float64

   * - tmp_dc_s07
     - sub-basin average July temperature (degrees C x10)
     - float64

   * - tmp_dc_s08
     - sub-basin average August temperature (degrees C x10)
     - float64

   * - tmp_dc_s09
     - sub-basin average September temperature (degrees C x10)
     - float64

   * - tmp_dc_s10
     - sub-basin average October temperature (degrees C x10)
     - float64

   * - tmp_dc_s11
     - sub-basin average November temperature (degrees C x10)
     - float64

   * - tmp_dc_s12
     - sub-basin average December temperature (degrees C x10)
     - float64

   * - pre_mm_syr
     - sub-basin annual average precipitation (mm/year)
     - float64

   * - pre_mm_uyr
     - total watershed annual average precipitation (mm/year)
     - float64

   * - pre_mm_s01
     - sub-basin average January precipitation (mm)
     - float64

   * - pre_mm_s02
     - sub-basin average February precipitation (mm)
     - float64

   * - pre_mm_s03
     - sub-basin average March precipitation (mm)
     - float64

   * - pre_mm_s04
     - sub-basin average April precipitation (mm)
     - float64

   * - pre_mm_s05
     - sub-basin average May precipitation (mm)
     - float64

   * - pre_mm_s06
     - sub-basin average June precipitation (mm)
     - float64

   * - pre_mm_s07
     - sub-basin average July precipitation (mm)
     - float64

   * - pre_mm_s08
     - sub-basin average August precipitation (mm)
     - float64

   * - pre_mm_s09
     - sub-basin average September precipitation (mm)
     - float64

   * - pre_mm_s10
     - sub-basin average October precipitation (mm)
     - float64

   * - pre_mm_s11
     - sub-basin average November precipitation (mm)
     - float64

   * - pre_mm_s12
     - sub-basin average December precipitation (mm)
     - float64

   * - pet_mm_syr
     - sub-basin annual average potential evapotranspiration (mm/year)
     - float64

   * - pet_mm_uyr
     - total watershed annual average potential evapotranspiration (mm/year)
     - float64

   * - pet_mm_s01
     - sub-basin average January potential evapotranspiration (mm)
     - float64

   * - pet_mm_s02
     - sub-basin average February potential evapotranspiration (mm)
     - float64

   * - pet_mm_s03
     - sub-basin average March potential evapotranspiration (mm)
     - float64

   * - pet_mm_s04
     - sub-basin average April potential evapotranspiration (mm)
     - float64

   * - pet_mm_s05
     - sub-basin average May potential evapotranspiration (mm)
     - float64

   * - pet_mm_s06
     - sub-basin average June potential evapotranspiration (mm)
     - float64

   * - pet_mm_s07
     - sub-basin average July potential evapotranspiration (mm)
     - float64

   * - pet_mm_s08
     - sub-basin average August potential evapotranspiration (mm)
     - float64

   * - pet_mm_s09
     - sub-basin average September potential evapotranspiration (mm)
     - float64

   * - pet_mm_s10
     - sub-basin average October potential evapotranspiration (mm)
     - float64

   * - pet_mm_s11
     - sub-basin average November potential evapotranspiration (mm)
     - float64

   * - pet_mm_s12
     - sub-basin average December potential evapotranspiration (mm)
     - float64

   * - aet_mm_syr
     - sub-basin annual average actual evapotranspiration (mm/year)
     - float64

   * - aet_mm_uyr
     - total watershed annual average actual evapotranspiration (mm/year)
     - float64

   * - aet_mm_s01
     - sub-basin average January actual evapotranspiration (mm)
     - float64

   * - aet_mm_s02
     - sub-basin average February actual evapotranspiration (mm)
     - float64

   * - aet_mm_s03
     - sub-basin average March actual evapotranspiration (mm)
     - float64

   * - aet_mm_s04
     - sub-basin average April actual evapotranspiration (mm)
     - float64

   * - aet_mm_s05
     - sub-basin average May actual evapotranspiration (mm)
     - float64

   * - aet_mm_s06
     - sub-basin average June actual evapotranspiration (mm)
     - float64

   * - aet_mm_s07
     - sub-basin average July actual evapotranspiration (mm)
     - float64

   * - aet_mm_s08
     - sub-basin average August actual evapotranspiration (mm)
     - float64

   * - aet_mm_s09
     - sub-basin average September actual evapotranspiration (mm)
     - float64

   * - aet_mm_s10
     - sub-basin average October actual evapotranspiration (mm)
     - float64

   * - aet_mm_s11
     - sub-basin average November actual evapotranspiration (mm)
     - float64

   * - aet_mm_s12
     - sub-basin average December actual evapotranspiration (mm)
     - float64

   * - ari_ix_sav
     - sub-basin average global arid index (index value)
     - float64

   * - ari_ix_uav
     - total watershed average global arid index (index value)
     - float64

   * - cmi_ix_syr
     - sub-basin annual average climate moisture index (index value)
     - float64

   * - cmi_ix_uyr
     - total watershed annual average climate moisture index (index value)
     - float64

   * - cmi_ix_s01
     - sub-basin average January climate moisture index (index value)
     - float64

   * - cmi_ix_s02
     - sub-basin average February climate moisture index (index value)
     - float64

   * - cmi_ix_s03
     - sub-basin average March climate moisture index (index value)
     - float64

   * - cmi_ix_s04
     - sub-basin average April climate moisture index (index value)
     - float64

   * - cmi_ix_s05
     - sub-basin average May climate moisture index (index value)
     - float64

   * - cmi_ix_s06
     - sub-basin average June climate moisture index (index value)
     - float64

   * - cmi_ix_s07
     - sub-basin average July climate moisture index (index value)
     - float64

   * - cmi_ix_s08
     - sub-basin average August climate moisture index (index value)
     - float64

   * - cmi_ix_s09
     - sub-basin average September climate moisture index (index value)
     - float64

   * - cmi_ix_s10
     - sub-basin average October climate moisture index (index value)
     - float64

   * - cmi_ix_s11
     - sub-basin average November climate moisture index (index value)
     - float64

   * - cmi_ix_s12
     - sub-basin average December climate moisture index (index value)
     - float64

   * - snw_pc_syr
     - sub-basin annual average snow cover extent (percent)
     - float64

   * - snw_pc_uyr
     - total watershed annual average snow cover extent (percent)
     - float64

   * - snw_pc_smx
     - sub-basin annual maximum snow cover extent (percent)
     - float64

   * - snw_pc_s01
     - sub-basin average January snow cover extent (percent)
     - float64

   * - snw_pc_s02
     - sub-basin average February snow cover extent (percent)
     - float64

   * - snw_pc_s03
     - sub-basin average March snow cover extent (percent)
     - float64

   * - snw_pc_s04
     - sub-basin average April snow cover extent (percent)
     - float64

   * - snw_pc_s05
     - sub-basin average May snow cover extent (percent)
     - float64

   * - snw_pc_s06
     - sub-basin average June snow cover extent (percent)
     - float64

   * - snw_pc_s07
     - sub-basin average July snow cover extent (percent)
     - float64

   * - snw_pc_s08
     - sub-basin average August snow cover extent (percent)
     - float64

   * - snw_pc_s09
     - sub-basin average September snow cover extent (percent)
     - float64

   * - snw_pc_s10
     - sub-basin average October snow cover extent (percent)
     - float64

   * - snw_pc_s11
     - sub-basin average November snow cover extent (percent)
     - float64

   * - snw_pc_s12
     - sub-basin average December snow cover extent (percent)
     - float64

   * - glc_cl_smj
     - sub-basin spatial majority land cover classes (classes 22)
     - float64

   * - glc_pc_s01
     - sub-basin percentage of forest land cover class 1 (broadleaf evergreen forest)
     - float64

   * - glc_pc_s02
     - sub-basin percentage of forest land cover class 2 (needleleaf evergreen forest)
     - float64

   * - glc_pc_s03
     - sub-basin percentage of forest land cover class 3 (broadleaf deciduous forest)
     - float64

   * - glc_pc_s04
     - sub-basin percentage of forest land cover class 4 (needleleaf deciduous forest)
     - float64

   * - glc_pc_s05
     - sub-basin percentage of forest land cover class 5 (mixed forest)
     - float64

   * - glc_pc_s06
     - sub-basin percentage of forest land cover class 6 (shrubland)
     - float64

   * - glc_pc_s07
     - sub-basin percentage of forest land cover class 7 (grassland)
     - float64

   * - glc_pc_s08
     - sub-basin percentage of forest land cover class 8 (wetland)
     - float64

   * - glc_pc_s09
     - sub-basin percentage of forest land cover class 9 (tundra)
     - float64

   * - glc_pc_s10
     - sub-basin percentage of forest land cover class 10 (desert)
     - float64

   * - glc_pc_s11
     - sub-basin percentage of forest land cover class 11 (urban)
     - float64

   * - glc_pc_s12
     - sub-basin percentage of forest land cover class 12 (water)
     - float64

   * - glc_pc_s13
     - sub-basin percentage of forest land cover class 13 (ice)
     - float64

   * - glc_pc_s14
     - sub-basin percentage of forest land cover class 14 (bare soil)
     - float64

   * - glc_pc_s15
     - sub-basin percentage of forest land cover class 15 (agricultural)
     - float64

   * - glc_pc_s16
     - sub-basin percentage of forest land cover class 16 (plantation)
     - float64

   * - glc_pc_s17
     - sub-basin percentage of forest land cover class 17 (mangrove)
     - float64

   * - glc_pc_s18
     - sub-basin percentage of forest land cover class 18 (bamboo)
     - float64

   * - glc_pc_s19
     - sub-basin percentage of forest land cover class 19 (savanna)
     - float64

   * - glc_pc_s20
     - sub-basin percentage of forest land cover class 20 (tropical rainforest)
     - float64

   * - glc_pc_s21
     - sub-basin percentage of forest land cover class 21 (temperate rainforest)
     - float64

   * - glc_pc_s22
     - sub-basin percentage of forest land cover class 22 (unknown)
     - float64

   * - glc_pc_u01
     - total watershed percentage of forest land cover class 1 (broadleaf evergreen forest)
     - float64

   * - glc_pc_u02
     - total watershed percentage of forest land cover class 2 (needleleaf evergreen forest)
     - float64

   * - glc_pc_u03
     - total watershed percentage of forest land cover class 3 (broadleaf deciduous forest)
     - float64

   * - glc_pc_u04
     - total watershed percentage of forest land cover class 4 (needleleaf deciduous forest)
     - float64

   * - glc_pc_u05
     - total watershed percentage of forest land cover class 5 (mixed forest)
     - float64

   * - glc_pc_u06
     - total watershed percentage of forest land cover class 6 (shrubland)
     - float64

   * - glc_pc_u07
     - total watershed percentage of forest land cover class 7 (grassland)
     - float64

   * - glc_pc_u08
     - total watershed percentage of forest land cover class 8 (wetland)
     - float64

   * - glc_pc_u09
     - total watershed percentage of forest land cover class 9 (tundra)
     - float64

   * - glc_pc_u10
     - total watershed percentage of forest land cover class 10 (desert)
     - float64

   * - glc_pc_u11
     - total watershed percentage of forest land cover class 11 (urban)
     - float64

   * - glc_pc_u12
     - total watershed percentage of forest land cover class 12 (water)
     - float64

   * - glc_pc_u13
     - total watershed percentage of forest land cover class 13 (ice)
     - float64

   * - glc_pc_u14
     - total watershed percentage of forest land cover class 14 (bare soil)
     - float64

   * - glc_pc_u15
     - total watershed percentage of forest land cover class 15 (agricultural)
     - float64

   * - glc_pc_u16
     - total watershed percentage of forest land cover class 16 (plantation)
     - float64

   * - glc_pc_u17
     - total watershed percentage of forest land cover class 17 (mangrove)
     - float64

   * - glc_pc_u18
     - total watershed percentage of forest land cover class 18 (bamboo)
     - float64

   * - glc_pc_u19
     - total watershed percentage of forest land cover class 19 (savanna)
     - float64

   * - glc_pc_u20
     - total watershed percentage of forest land cover class 20 (tropical rainforest)
     - float64

   * - glc_pc_u21
     - total watershed percentage of forest land cover class 21 (temperate rainforest)
     - float64

   * - glc_pc_u22
     - total watershed percentage of forest land cover class 22 (unknown)
     - float64

   * - pnv_cl_smj
     - sub-basin potential natural vegetation spatial majority classes (classes 15)
     - float64

   * - pnv_pc_s01
     - sub-basin percentage of potential natural vegetation class 1 (broadleaf evergreen forest)
     - float64

   * - pnv_pc_s02
     - sub-basin percentage of potential natural vegetation class 2 (needleleaf evergreen forest)
     - float64

   * - pnv_pc_s03
     - sub-basin percentage of potential natural vegetation class 3 (broadleaf deciduous forest)
     - float64

   * - pnv_pc_s04
     - sub-basin percentage of potential natural vegetation class 4 (needleleaf deciduous forest)
     - float64

   * - pnv_pc_s05
     - sub-basin percentage of potential natural vegetation class 5 (mixed forest)
     - float64

   * - pnv_pc_s06
     - sub-basin percentage of potential natural vegetation class 6 (shrubland)
     - float64

   * - pnv_pc_s07
     - sub-basin percentage of potential natural vegetation class 7 (grassland)
     - float64

   * - pnv_pc_s08
     - sub-basin percentage of potential natural vegetation class 8 (wetland)
     - float64

   * - pnv_pc_s09
     - sub-basin percentage of potential natural vegetation class 9 (tundra)
     - float64

   * - pnv_pc_s10
     - sub-basin percentage of potential natural vegetation class 10 (desert)
     - float64

   * - pnv_pc_s11
     - sub-basin percentage of potential natural vegetation class 11 (urban)
     - float64

   * - pnv_pc_s12
     - sub-basin percentage of potential natural vegetation class 12 (water)
     - float64

   * - pnv_pc_s13
     - sub-basin percentage of potential natural vegetation class 13 (ice)
     - float64

   * - pnv_pc_s14
     - sub-basin percentage of potential natural vegetation class 14 (bare soil)
     - float64

   * - pnv_pc_s15
     - sub-basin percentage of potential natural vegetation class 15 (agricultural)
     - float64

   * - pnv_pc_u01
     - total watershed percentage of potential natural vegetation class 1 (broadleaf evergreen forest)
     - float64

   * - pnv_pc_u02
     - total watershed percentage of potential natural vegetation class 2 (needleleaf evergreen forest)
     - float64

   * - pnv_pc_u03
     - total watershed percentage of potential natural vegetation class 3 (broadleaf deciduous forest)
     - float64

   * - pnv_pc_u04
     - total watershed percentage of potential natural vegetation class 4 (needleleaf deciduous forest)
     - float64

   * - pnv_pc_u05
     - total watershed percentage of potential natural vegetation class 5 (mixed forest)
     - float64

   * - pnv_pc_u06
     - total watershed percentage of potential natural vegetation class 6 (shrubland)
     - float64

   * - pnv_pc_u07
     - total watershed percentage of potential natural vegetation class 7 (grassland)
     - float64

   * - pnv_pc_u08
     - total watershed percentage of potential natural vegetation class 8 (wetland)
     - float64

   * - pnv_pc_u09
     - total watershed percentage of potential natural vegetation class 9 (tundra)
     - float64

   * - pnv_pc_u10
     - total watershed percentage of potential natural vegetation class 10 (desert)
     - float64

   * - pnv_pc_u11
     - total watershed percentage of potential natural vegetation class 11 (urban)
     - float64

   * - pnv_pc_u12
     - total watershed percentage of potential natural vegetation class 12 (water)
     - float64

   * - pnv_pc_u13
     - total watershed percentage of potential natural vegetation class 13 (ice)
     - float64

   * - pnv_pc_u14
     - total watershed percentage of potential natural vegetation class 14 (bare soil)
     - float64

   * - pnv_pc_u15
     - total watershed percentage of potential natural vegetation class 15 (agricultural)
     - float64

   * - wet_cl_smj
     - sub-basin spatial majority wetland classes (classes 12)
     - float64

   * - wet_pc_sg1
     - sub-basin percentage of wetland cover for class group 1
     - float64

   * - wet_pc_ug1
     - total watershed percentage of wetland cover for class group 1
     - float64

   * - wet_pc_sg2
     - sub-basin percentage of wetland cover for class group 2
     - float64

   * - wet_pc_ug2
     - total watershed percentage of wetland cover for class group 2
     - float64

   * - wet_pc_s01
     - sub-basin percentage of wetland cover for class group 1
     - float64

   * - wet_pc_s02
     - sub-basin percentage of wetland cover for class group 2
     - float64

   * - wet_pc_s03
     - sub-basin percentage of wetland cover for class group 3
     - float64

   * - wet_pc_s04
     - sub-basin percentage of wetland cover for class group 4
     - float64

   * - wet_pc_s05
     - sub-basin percentage of wetland cover for class group 5
     - float64

   * - wet_pc_s06
     - sub-basin percentage of wetland cover for class group 6
     - float64

   * - wet_pc_s07
     - sub-basin percentage of wetland cover for class group 7
     - float64

   * - wet_pc_s08
     - sub-basin percentage of wetland cover for class group 8
     - float64

   * - wet_pc_s09
     - sub-basin percentage of wetland cover for class group 9
     - float64

   * - wet_pc_u01
     - total watershed percentage of wetland cover for class group 1
     - float64

   * - wet_pc_u02
     - total watershed percentage of wetland cover for class group 2
     - float64

   * - wet_pc_u03
     - total watershed percentage of wetland cover for class group 3
     - float64

   * - wet_pc_u04
     - total watershed percentage of wetland cover for class group 4
     - float64

   * - wet_pc_u05
     - total watershed percentage of wetland cover for class group 5
     - float64

   * - wet_pc_u06
     - total watershed percentage of wetland cover for class group 6
     - float64

   * - wet_pc_u07
     - total watershed percentage of wetland cover for class group 7
     - float64

   * - wet_pc_u08
     - total watershed percentage of wetland cover for class group 8
     - float64

   * - wet_pc_u09
     - total watershed percentage of wetland cover for class group 9
     - float64

   * - for_pc_sse
     - sub-basin forest cover extent (percentage)
     - float64

   * - for_pc_use
     - total watershed forest cover extent (percentage)
     - float64

   * - crp_pc_sse
     - sub-basin crop cover extent (percentage)
     - float64

   * - crp_pc_use
     - total watershed crop cover extent (percentage)
     - float64

   * - pst_pc_sse
     - sub-basin pasture cover extent (percentage)
     - float64

   * - pst_pc_use
     - total watershed pasture cover extent (percentage)
     - float64

   * - ire_pc_sse
     - sub-basin irrigated area extent (percentage)
     - float64

   * - ire_pc_use
     - total watershed irrigated area extent (percentage)
     - float64

   * - gla_pc_sse
     - sub-basin glacier cover (percentage)
     - float64

   * - gla_pc_use
     - total watershed glacier cover (percentage)
     - float64

   * - prm_pc_sse
     - sub-basin permafrost cover (percentage)
     - float64

   * - prm_pc_use
     - total watershed permafrost cover (percentage)
     - float64

   * - pac_pc_sse
     - sub-basin protected area cover (percentage)
     - float64

   * - pac_pc_use
     - total watershed protected area cover (percentage)
     - float64

   * - tbi_cl_smj
     - sub-basin terrestrial biome spatial majority classes (classes 14)
     - float64

   * - tec_cl_smj
     - sub-basin terrestrial ecoregion spatial majority classes (classes 14)
     - float64

   * - fmh_cl_smj
     - sub-basin spatial majority of freshwater major habitat classes (classes 13)
     - float64

   * - fec_cl_smj
     - sub-basin spatial majority of freshwater ecoregions (classes 426)
     - float64

   * - cly_pc_sav
     - sub-basin average clay content (percentage)
     - float64

   * - cly_pc_uav
     - total watershed average clay content (percentage)
     - float64

   * - slt_pc_sav
     - sub-basin average silt content (percentage)
     - float64

   * - slt_pc_uav
     - total watershed average silt content (percentage)
     - float64

   * - snd_pc_sav
     - sub-basin average sand content (percentage)
     - float64

   * - snd_pc_uav
     - total watershed average sand content (percentage)
     - float64

   * - soc_th_sav
     - sub-basin average soil organic carbon (percentage)
     - float64

   * - soc_th_uav
     - total watershed average soil organic carbon (percentage)
     - float64

   * - swc_pc_syr
     - sub-basin average soil water content (percentage)
     - float64

   * - swc_pc_uyr
     - total watershed average soil water content (percentage)
     - float64

   * - swc_pc_s01
     - sub-basin soil water content for January (percentage)
     - float64

   * - swc_pc_s02
     - sub-basin soil water content for February (percentage)
     - float64

   * - swc_pc_s03
     - sub-basin soil water content for March (percentage)
     - float64

   * - swc_pc_s04
     - sub-basin soil water content for April (percentage)
     - float64

   * - swc_pc_s07
     - sub-basin soil water content for July (percentage)
     - float64

   * - swc_pc_s08
     - sub-basin soil water content for August (percentage)
     - float64

   * - swc_pc_s09
     - sub-basin soil water content for September (percentage)
     - float64

   * - swc_pc_s10
     - sub-basin soil water content for October (percentage)
     - float64

   * - swc_pc_s11
     - sub-basin soil water content for November (percentage)
     - float64

   * - swc_pc_s12
     - sub-basin soil water content for December (percentage)
     - float64

   * - lit_cl_smj
     - sub-basin spatial majority lithology classes (classes 16)
     - float64

   * - kar_pc_sse
     - sub-basin spatial extent of karst cover (percentage)
     - float64

   * - kar_pc_use
     - total watershed spatial extent of karst cover (percentage)
     - float64

   * - ero_kh_sav
     - sub-basin soil erosion (kg/hectare/yr)
     - float64

   * - ero_kh_uav
     - total watershed soil erosion (kg/hectare/yr)
     - float64

   * - pop_ct_ssu
     - sub-basin population count (count thousands)
     - float64

   * - pop_ct_usu
     - total watershed population count (count thousands)
     - float64

   * - ppd_pk_sav
     - sub-basin population density (people/km2)
     - float64

   * - ppd_pk_uav
     - total watershed population density (people/km2)
     - float64

   * - urb_pc_sse
     - sub-basin urban cover (percentage)
     - float64

   * - urb_pc_use
     - total watershed urban cover (percentage)
     - float64

   * - nli_ix_sav
     - sub-basin average nighttime lights index (index value)
     - float64

   * - nli_ix_uav
     - total watershed average nighttime lights index (index value)
     - float64

   * - rdd_mk_sav
     - sub-basin road density (m/km2)
     - float64

   * - rdd_mk_uav
     - total watershed road density (m/km2)
     - float64

   * - hft_ix_s93
     - sub-basin human footprint index for 1993 (index value)
     - float64

   * - hft_ix_u93
     - total watershed human footprint index for 2009 (index value)
     - float64

   * - hft_ix_s09
     - sub-basin human footprint index for 2009 (index value)
     - float64

   * - hft_ix_u09
     - total watershed human footprint index for 2009 (index value)
     - float64

   * - gad_id_smj
     - sub-basin administrative unit spatial majority (ID number)
     - float64

   * - gdp_ud_sav
     - sub-basin average gross domestic product (USD)
     - float64

   * - gdp_ud_ssu
     - sub-basin total gross domestic product (USD)
     - float64

   * - gdp_ud_usu
     - total watershed gross domestic product (USD)
     - float64

   * - hdi_ix_sav
     - sub-basin human development index (index value)
     - float64




.. _hydroatlas-attr_select_file:

hydroatlas.attr_select_file
---------------------------

File to configure the selection of HydroATLAS attributes for parameter regionalization.

Sample file path: ``inputs/region/attr_config/attr_selection_hydroatlas.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "select", "attr_name", "description"
   "1", "dis_m3_pyr", "annual average natural discharge (m3/year)"
   "1", "dis_m3_pmn", "annual minimum naturaldischarge (m3/month)"
   "1", "dis_m3_pmx", "annual maximum natural discharge (m3/month)"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - select
     - Whether to select this attribute for parameter regionalization (1 for yes, 0 for no).
     - int64

   * - attr_name
     - Name of the HydroATLAS attribute to be selected for parameter regionalization.
     - object

   * - description
     - Description of the HydroATLAS attribute.
     - object




.. _manual_pairings:

manual_pairings
---------------

File containing manual pairings to update algorithm based donor-receiver pairs.

Sample file path: ``inputs/region/manual_pairs/manual_pairs_vpu03S_nhf.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "receiver_div_id", "receiver_gage_id", "donor_div_id", "donor_gage_id"
   "164565.0", "nan", "635016.0", "nan"
   "164568.0", "nan", "nan", "02245500"
   "nan", "02207385", "nan", "02314500"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - receiver_div_id
     - Unique identifier for the receiver catchment (i.e., divide).
     - float64

   * - receiver_gage_id
     - Unique identifier for the receiver gage.
     - object

   * - donor_div_id
     - Unique identifier for the donor catchment (i.e., divide).
     - float64

   * - donor_gage_id
     - Unique identifier for the donor gage.
     - object




.. _ngen-attr_data_file:

ngen.attr_data_file
-------------------

File containing NGEN attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/ngen/attr_ngen_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "area_sqkm", "elevation_mean", "slope250m_mean", "aspect_circmean", "lat", "lon", "glacier_percent", "bexp_mode", "isltyp_mode", "ivgtyp_mode", "dksat_geomean", "psisat_geomean", "cwpvt_mean", "mp_mean", "mfsno_mean", "quartz_mean", "refkdt_mean", "slope1km_mean", "smcmax_mean", "smcwlt_mean", "vcmx_mean", "cgw", "expon", "max_gw_storage", "imperv_mean", "a_xinanjiang_inflection_point_parameter", "b_xinanjiang_shape_parameter", "x_xinanjiang_shape_parameter", "twi_q25", "twi_q50", "twi_q75", "twi_q100", "twi_q10", "twi_q20", "twi_q30", "twi_q40", "twi_q60", "twi_q70", "twi_q80", "twi_q90", "lzfpm_mean", "lzpk_mean", "lztwm_mean", "rexp_mean", "uzk_mean", "zperc_mean", "lzfsm_mean", "lzsk_mean", "pfree_mean", "uzfwm_mean", "uztwm_mean", "mfmin_mean", "mfmax_mean", "uadj_mean", "temp_delta_jan_mean", "temp_delta_feb_mean", "temp_delta_mar_mean", "temp_delta_apr_mean", "temp_delta_may_mean", "temp_delta_jun_mean", "temp_delta_jul_mean", "temp_delta_aug_mean", "temp_delta_sep_mean", "temp_delta_oct_mean", "temp_delta_nov_mean", "temp_delta_dec_mean"
   "1289012700708937", "11.239999102529051", "185.77283221446217", "2.3662304190478687", "163.40149963074526", "47.077058995339804", "-67.79463457394353", "0.0", "9.165840148925781", "6.0", "5.0", "2.9118978728815845e-05", "0.28127546075392973", "0.3507773604592752", "10.588505735184416", "0.8304194114077973", "0.4504210433621705", "2.0", "0.01433713669131892", "0.4760510254837101", "0.06121000120190986", "90.6794702254743", "0.0049999998882412884", "3.64037275314331", "0.10812441253662124", "0.012646771694569401", "-0.018336246824008095", "0.9297370494636552", "1.54185792994688", "4.066648483276367", "4.695955753326416", "5.730521202087402", "18.53713607788086", "3.574476718902588", "3.8834261894226074", "4.15705680847168", "4.44460916519165", "4.8837080001831055", "5.320420265197754", "6.100194454193115", "6.852163791656494", "146.19238084844008", "0.0379357703184254", "259.2077860112577", "1.9522023469892436", "0.4047116766184893", "301.9838625640972", "25.210097794268368", "0.1488220925512261", "0.1546803376104585", "29.73913464920321", "52.21157858618951", "0.2916407986171984", "1.5285257512766817", "0.03798329762241453", "11.014422391868266", "11.971328244304406", "10.979587786189589", "10.205577608131733", "12.437211195934132", "12.2", "11.6238778626008", "12.324727735366263", "12.364183206098796", "10.178910941465068", "7.820544529267467", "8.65764885488919"
   "1289012709475965", "0.13364525621490148", "141.5147418757551", "1.7178736523534244", "58.74129623335019", "47.07856676764578", "-67.81401480483588", "0.0", "9.165840148925781", "6.0", "5.0", "2.7311261874274334e-05", "0.354999989271164", "0.35660746693611145", "10.57097053527832", "0.7838379740715027", "0.4000000059604645", "2.0", "0.008432386896200732", "0.4784286618232727", "0.06599999964237213", "83.99993896484375", "0.004999999888241291", "3.6403727531433105", "0.1081244125366211", "5.5836538529875443e-05", "-0.029008781537413597", "1.0477995872497559", "1.7999998331069946", "4.496644973754883", "6.890119552612305", "13.059494972229004", "19.228870391845703", "4.009361743927002", "4.290122985839844", "4.703166961669922", "5.116210460662842", "9.357870101928711", "11.8256196975708", "14.293370246887207", "16.761119842529297", "138.2631072998047", "0.014805309474468231", "247.81222534179688", "1.924048900604248", "0.40970563888549805", "350.5870056152344", "20.363422393798828", "0.15013833343982697", "0.1428825706243515", "33.435523986816406", "58.766075134277344", "0.29108453298081655", "1.5070099797100518", "0.03700448959396729", "11.019999999999996", "11.986666666666666", "10.943333333333335", "10.2", "12.44", "12.200000000000001", "11.62666666666667", "12.323333333333327", "12.359999999999998", "10.173333333333334", "7.823333333333332", "8.620000000000001"
   "1289012797097104", "11.938492309502166", "224.8518209145945", "1.630821816845848", "188.07425291522463", "47.10981692859889", "-67.7922225910657", "0.0", "9.165840148925781", "6.0", "5.0", "1.541664586413886e-05", "0.3549999892711639", "0.2840700916163955", "10.789141057883418", "1.363397749938271", "0.40000000596046453", "2.0", "0.08189846401833407", "0.4659383581608203", "0.06599999964237213", "88.32861873629184", "0.00499999988824129", "3.64037275314331", "0.10812441253662138", "0.0", "0.07578029715181446", "1.222176076728234", "1.411225561371027", "4.505222797393799", "5.031597137451172", "6.726294040679932", "19.228870391845703", "3.8376150131225586", "4.243478775024414", "4.62615966796875", "4.849382400512695", "5.629532814025879", "6.353250026702881", "7.264786243438721", "8.720602035522461", "141.18046790688354", "0.015969319685261732", "261.0802934006195", "1.925426430363956", "0.4087072850715632", "392.6805852762888", "19.98991907770407", "0.14930573716454087", "0.141715206452149", "35.26513768047632", "64.0870176782277", "0.2959874708795997", "1.5810114827598931", "0.04060493213622715", "11.019774332046007", "12.025093665989504", "11.079701996144392", "10.257601768150328", "12.425426227312347", "12.23413194756046", "11.664573825215907", "12.335887067917868", "12.417016122596092", "10.192169183107218", "7.81395972937459", "8.75587480296981"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - string

   * - area_sqkm
     - area in square kilometers
     - float64

   * - elevation_mean
     - mean elevation
     - float64

   * - slope250m_mean
     - mean slope calculated from 250m DEM
     - float64

   * - aspect_circmean
     - circular mean of aspect
     - float64

   * - lat
     - latitude
     - float64

   * - lon
     - longitude
     - float64

   * - glacier_percent
     - percentage of glacier area
     - float64

   * - bexp_mode
     - NWM parameter: beta exponent on Clapp-Hornberger (1978) soil water relations (mode)
     - float64

   * - isltyp_mode
     - NWM parameter: soil type (mode)
     - float64

   * - ivgtyp_mode
     - NWM parameter: vegetation type (mode)
     - float64

   * - dksat_geomean
     - NWM parameter: saturated hydraulic conductivity (geometric mean)
     - float64

   * - psisat_geomean
     - NWM parameter: saturated capillary head (geometric mean)
     - float64

   * - cwpvt_mean
     - NWM parameter: canopy wind parameter for canopy wind profile formulation (mean)
     - float64

   * - mp_mean
     - NWM parameter: Slope of Ball-Berry conductance relationship (mean)
     - float64

   * - mfsno_mean
     - NWM parameter: minimum snow water equivalent (mean)
     - float64

   * - quartz_mean
     - NWM parameter: quartz content (mean)
     - float64

   * - refkdt_mean
     - NWM parameter: Soil infiltration parameter (mean)
     - float64

   * - slope1km_mean
     - NWM parameter: Coeffecient controlling the drainage out of the soil bottom (0=no-flow)
     - float64

   * - smcmax_mean
     - NWM parameter: maximum soil moisture content (mean)
     - float64

   * - smcwlt_mean
     - NWM parameter: soil moisture content at wilting point (mean)
     - float64

   * - vcmx_mean
     - NWM parameter: Maximum carboxylation at 25 degC (mean)
     - float64

   * - cgw
     - NWM parameter: channel groundwater storage
     - float64

   * - expon
     - NWM parameter: exponent for nonlinear ground water reservoir (1.0 for linear reservoir)
     - float64

   * - max_gw_storage
     - NWM parameter: maximum groundwater storage
     - float64

   * - imperv_mean
     - NWM parameter: impervious area fraction (mean)
     - float64

   * - a_xinanjiang_inflection_point_parameter
     - NWM parameter: Xinanjiang inflection point parameter
     - float64

   * - b_xinanjiang_shape_parameter
     - NWM parameter: Xinanjiang shape parameter
     - float64

   * - x_xinanjiang_shape_parameter
     - NWM parameter: Xinanjiang shape parameter
     - float64

   * - twi_q25
     - 25th percentile of topographic wetness index
     - float64

   * - twi_q50
     - 50th percentile of topographic wetness index
     - float64

   * - twi_q75
     - 75th percentile of topographic wetness index
     - float64

   * - twi_q100
     - 100th percentile of topographic wetness index
     - float64

   * - twi_q10
     - 10th percentile of topographic wetness index
     - float64

   * - twi_q20
     - 20th percentile of topographic wetness index
     - float64

   * - twi_q30
     - 30th percentile of topographic wetness index
     - float64

   * - twi_q40
     - 40th percentile of topographic wetness index
     - float64

   * - twi_q60
     - 60th percentile of topographic wetness index
     - float64

   * - twi_q70
     - 70th percentile of topographic wetness index
     - float64

   * - twi_q80
     - 80th percentile of topographic wetness index
     - float64

   * - twi_q90
     - 90th percentile of topographic wetness index
     - float64

   * - lzfpm_mean
     - SAC-SMA parameter: Maximum lower zone free water, primary(mean)
     - float64

   * - lzpk_mean
     - SAC-SMA parameter: Lower zone recession coefficient, primary (mean)
     - float64

   * - lztwm_mean
     - SAC-SMA parameter: Maximum lower zone tension water (mean)
     - float64

   * - rexp_mean
     - SAC-SMA parameter: Percolation equation exponent (mean)
     - float64

   * - uzk_mean
     - SAC-SMA parameter: Upper zone recession coefficient (mean)
     - float64

   * - zperc_mean
     - SAC-SMA parameter: Minimum percolation rate coefficient (mean)
     - float64

   * - lzfsm_mean
     - SAC-SMA parameter: Maximum lower zone free water, secondary or supplemental (mean)
     - float64

   * - lzsk_mean
     - SAC-SMA parameter: Lower zone recession coefficient, secondary or supplemental (mean)
     - float64

   * - pfree_mean
     - SAC-SMA parameter: Percent percolating directly to lower zone free water (mean)
     - float64

   * - uzfwm_mean
     - SAC-SMA parameter: Maximum upper zone free water (mean)
     - float64

   * - uztwm_mean
     - SAC-SMA parameter: Maximum upper zone tension water (mean)
     - float64

   * - mfmin_mean
     - SNOW-17 parameter: Minimum non-rain melt factor (mean)
     - float64

   * - mfmax_mean
     - SNOW-17 parameter: Maximum non-rain melt factor (mean)
     - float64

   * - uadj_mean
     - SNOW-17 parameter: Average wind function for rain on snow (mean)
     - float64

   * - temp_delta_jan_mean
     - Temperature delta for January (mean)
     - float64

   * - temp_delta_feb_mean
     - Temperature delta for February (mean)
     - float64

   * - temp_delta_mar_mean
     - Temperature delta for March (mean)
     - float64

   * - temp_delta_apr_mean
     - Temperature delta for April (mean)
     - float64

   * - temp_delta_may_mean
     - Temperature delta for May (mean)
     - float64

   * - temp_delta_jun_mean
     - Temperature delta for June (mean)
     - float64

   * - temp_delta_jul_mean
     - Temperature delta for July (mean)
     - float64

   * - temp_delta_aug_mean
     - Temperature delta for August (mean)
     - float64

   * - temp_delta_sep_mean
     - Temperature delta for September (mean)
     - float64

   * - temp_delta_oct_mean
     - Temperature delta for October (mean)
     - float64

   * - temp_delta_nov_mean
     - Temperature delta for November (mean)
     - float64

   * - temp_delta_dec_mean
     - Temperature delta for December (mean)
     - float64




.. _ngen-attr_select_file:

ngen.attr_select_file
---------------------

File to configure the selection of NGEN attributes for parameter regionalization.

Sample file path: ``inputs/region/attr_config/attr_selection_ngen.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "select", "attr_name", "description"
   "1", "area_sqkm", " "area in square kilometers""
   "1", "elevation_mean", " "mean elevation""
   "1", "slope250m_mean", " "mean slope calculated from 250m DEM""

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - select
     - Whether to select this attribute for parameter regionalization (1 for yes, 0 for no).
     - int64

   * - attr_name
     - Name of the NGEN attribute to be selected for parameter regionalization.
     - object

   * - description
     - Description of the NGEN attribute.
     - object




.. _ngen_hydrofabric_file-layer-flowpaths:

ngen_hydrofabric_file (layer: flowpaths)
----------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "fp_id", "dn_nex_id", "up_nex_id", "div_id", "vpu_id", "length_km", "area_sqkm", "total_da_sqkm", "mainstem_lp", "path_length", "dn_hydroseq", "hydroseq", "stream_order", "mean_elevation", "slope", "n", "r", "y", "ncc", "btmwdth", "chslp", "musx", "musk", "topwdth", "topwdthcc", "topwdthcc_ml", "topwdth_ml", "y_ml", "r_ml", "fp_to_id", "gid", "terminalpa"
   "1073625600290331", "1073625600265387", "nan", "1073625600290331", "03S", "0.12622339396322607", "0.239849982001549", "0.239849982001549", "4985", "0.0", "0", "11015", "1", "-0.5811592638492584", "0.0024175001668526115", "0.096", "nan", "nan", "0.192", "1.6", "0.03", "0.2", "3600", "1.5016520766156676", "4.504956229847003", "133.4000587463379", "44.4666862487793", "1.3400835990905762", "3.4363529682159424", "nan", "76RWG223+R7RH", "11015"
   "1073625637040207", "1073601250260032", "1073626944871078.0", "1073625637040207", "03S", "9.941883006906545", "92.58839979749507", "3736.578157487904", "4986", "0.0", "0", "11016", "3", "-1.011073738336563", "5.7858849160222174e-05", "0.06", "nan", "nan", "0.12", "3.5", "0.03", "0.2", "3600", "39.99733084683427", "119.99199254050279", "1579.2822875976562", "526.4274291992188", "3.6210639476776123", "2.7048046588897705", "nan", "76RWG2HH+G2G9", "11016"
   "1073626961303593", "1073626944871078", "1073626974848275.0", "1073626961303593", "03S", "3.1062795495062994", "10.963349810997265", "3643.9897576904086", "4986", "9.941883006906545", "11016", "11017", "3", "-0.5244999974966049", "0.0001624473698308016", "0.06", "nan", "nan", "0.12", "3.5", "0.03", "0.2", "3600", "39.657566077514765", "118.9726982325443", "4069.064208984375", "1356.354736328125", "4.895653247833252", "3.4849252700805664", "1073625637040207.0", "76RWH37C+4WXM", "11016"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - fp_id
     - Unique identifier for the flowpath. Shares the same value with the corresponding catchment's div_id.
     - int64

   * - dn_nex_id
     - Unique identifier for the downstream nexus that the catchment flows to.
     - int64

   * - up_nex_id
     - Unique identifier for the upstream nexus that flows to the catchment.
     - float64

   * - div_id
     - Unique identifier for each catchment.
     - int64

   * - vpu_id
     - VPU identifier.
     - object

   * - length_km
     - flowpath length in kilometers.
     - float64

   * - area_sqkm
     - Area in square kilometers.
     - float64

   * - total_da_sqkm
     - total_da_sqkm
     - float64

   * - mainstem_lp
     - mainstem_lp
     - int64

   * - path_length
     - path_length
     - float64

   * - dn_hydroseq
     - dn_hydroseq
     - int64

   * - hydroseq
     - hydroseq
     - int64

   * - stream_order
     - stream_order
     - int64

   * - mean_elevation
     - mean_elevation
     - float64

   * - slope
     - slope
     - float64

   * - n
     - n
     - float64

   * - r
     - r
     - float32

   * - y
     - y
     - float32

   * - ncc
     - ncc
     - float64

   * - btmwdth
     - btmwdth
     - float64

   * - chslp
     - chslp
     - float64

   * - musx
     - musx
     - float64

   * - musk
     - musk
     - int64

   * - topwdth
     - topwdth
     - float64

   * - topwdthcc
     - topwdthcc
     - float64

   * - topwdthcc_ml
     - topwdthcc_ml
     - float64

   * - topwdth_ml
     - topwdth_ml
     - float64

   * - y_ml
     - y_ml
     - float32

   * - r_ml
     - r_ml
     - float32

   * - fp_to_id
     - fp_to_id
     - float64

   * - gid
     - gid
     - object

   * - terminalpa
     - terminalpa
     - int64

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-nexus:

ngen_hydrofabric_file (layer: nexus)
------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "nex_id", "dn_fp_id", "vpu_id", "gid"
   "1073625600265387", "nan", "03S", "76RWG223+M5F9"
   "1073601250260032", "nan", "03S", "76RVGXGP+4G3J"
   "1073626944871078", "1073625637040207.0", "03S", "76RWH327+CVMW"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - nex_id
     - nex_id
     - int64

   * - dn_fp_id
     - dn_fp_id
     - float64

   * - vpu_id
     - VPU identifier.
     - object

   * - gid
     - gid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-divides:

ngen_hydrofabric_file (layer: divides)
--------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "vpu_id", "type", "area_sqkm", "bexp_mode", "isltyp_mode", "ivgtyp_mode", "dksat_geomean", "psisat_geomean", "cwpvt_mean", "mp_mean", "mfsno_mean", "quartz_mean", "refkdt_mean", "slope1km_mean", "smcmax_mean", "smcwlt_mean", "vcmx_mean", "imperv_mean", "twi_q25", "twi_q50", "twi_q75", "twi_q100", "twi_q10", "twi_q20", "twi_q30", "twi_q40", "twi_q60", "twi_q70", "twi_q80", "twi_q90", "elevation_mean", "slope250m_mean", "aspect_circmean", "lzfpm_mean", "lzpk_mean", "lztwm_mean", "rexp_mean", "uzk_mean", "zperc_mean", "lzfsm_mean", "lzsk_mean", "pfree_mean", "uzfwm_mean", "uztwm_mean", "mfmin_mean", "mfmax_mean", "uadj_mean", "a_xinanjiang_inflection_point_parameter", "b_xinanjiang_shape_parameter", "x_xinanjiang_shape_parameter", "temp_delta_jan_mean", "temp_delta_feb_mean", "temp_delta_mar_mean", "temp_delta_apr_mean", "temp_delta_may_mean", "temp_delta_jun_mean", "temp_delta_jul_mean", "temp_delta_aug_mean", "temp_delta_sep_mean", "temp_delta_oct_mean", "temp_delta_nov_mean", "temp_delta_dec_mean", "lat", "lon", "glacier_percent", "cgw", "expon", "max_gw_storage", "gid"
   "1073625600290331", "03S", "aggregate", "0.239849982001549", "3.818035364151001", "1.0", "1.0", "3.6914939498829117e-06", "0.09338372026720441", "0.0928061231970787", "12.360313415527344", "2.0", "0.7845002490817423", "2.0", "0.012976297708553007", "0.4200838979884917", "0.02566716016949276", "69.99994659423828", "0.15954700840730673", "5.972740173339844", "6.26715612411499", "6.371448993682861", "7.470083713531494", "5.796090602874756", "5.9138569831848145", "6.031623363494873", "6.149389743804932", "6.371435642242432", "6.371444225311279", "6.371453285217285", "6.632567882537842", "0.06030126203576657", "0.08029816577959442", "236.4273452993607", "214.25912164943603", "0.05888670554283108", "123.76491332175843", "1.4380440872773759", "0.7630407749297897", "20.150517400395312", "11.805358714058677", "0.270208988512994", "0.0942817413303882", "25.912842136563075", "12.990550240619662", "0.7099999785423279", "1.3899999856948853", "0.03298269957304001", "-0.018742965534329414", "0.538235980192303", "0.001675244529961307", "11.930000000000001", "12.016666666666662", "12.07333333333334", "12.263333333333318", "11.919999999999998", "10.196666666666669", "9.68333333333333", "9.769999999999982", "9.31666666666666", "10.116666666666653", "11.193333333333328", "11.49666666666666", "26.504135073101544", "-81.99470405488476", "0.0", "0.004999999888241291", "2.460475206375122", "0.24713890075683592", "76RWG223+R7RH"
   "1073625637040207", "03S", "aggregate", "92.58839979749507", "3.818035364151001", "1.0", "1.0", "7.1393186012168985e-06", "0.0757241496505964", "0.09355893014858675", "12.35240330332629", "2.0", "0.8249747435334212", "2.0", "0.013506275137727657", "0.3873380562165833", "0.014742980032647488", "69.3113811175164", "0.2681815689814034", "6.775866508483887", "7.436667442321777", "8.163203239440918", "12.75737190246582", "6.083558559417725", "6.371192932128906", "6.776295185089111", "6.776730060577393", "7.469760417938232", "7.875497817993164", "8.567959785461426", "9.578204154968262", "1.1705845839469562", "0.05471055200576598", "182.69958537368797", "251.65506707996698", "0.06720892995085322", "148.33030455580314", "1.3785512409541387", "0.763481840972403", "18.812386270792654", "12.661191360208207", "0.269209957312484", "0.08560360420629382", "25.860781478713143", "12.946150439572325", "0.7030492082268506", "1.383298338570957", "0.032967794448183006", "-0.0017540666718045658", "0.437571486362854", "0.0021546517341892", "11.998111802156364", "12.139404828168265", "12.206548282167693", "12.33347787200574", "12.074152164902452", "10.247593100152574", "9.758970181127765", "9.747677996871822", "9.313428885197439", "10.09069742805398", "11.347756611342497", "11.479379267979002", "26.551327278187205", "-81.96011228766315", "0.0", "0.004999999888241293", "2.627503925111515", "0.23326157123771907", "76RWG2HH+G2G9"
   "1073626961303593", "03S", "connectors", "10.963349810997265", "6.486554145812988", "14.0", "1.0", "1.5567018469057003e-06", "0.1238224889323819", "0.0928061231970787", "12.360313415527344", "2.0", "0.6293138658206437", "2.0", "0.012976297708553004", "0.46162880639818954", "0.04027407602415274", "nan", "0.178267505207074", "6.371095657348633", "6.776533126831055", "7.959933757781982", "12.87630844116211", "6.083254337310791", "6.083381652832031", "6.776321887969971", "6.776401042938232", "7.4695611000061035", "7.874942779541016", "8.532188415527344", "12.224349021911621", "0.6238719058729318", "0.07445809437180916", "208.92124239877825", "294.9365238032896", "0.07723051736761308", "184.40320436674781", "1.2951377429691782", "0.7627148096328631", "18.080432273768118", "15.053886229353582", "0.2665620886809283", "0.06611827004643328", "20.963326896424032", "10.506909830539314", "0.7064571040959576", "1.3899999856948853", "0.03298269957304001", "-0.01047828084825627", "0.6652115741821025", "0.0020704525690610803", "12.013345092080874", "12.2246578546686", "12.265492475311806", "12.42468378000156", "12.139542226608636", "10.23062167957686", "9.714505240720483", "9.726972564304162", "9.286588200926168", "10.077415800915151", "11.340210066017368", "11.536120300517457", "26.562789199487746", "-81.92652525723875", "0.0", "0.004999999888241292", "2.4604752063751216", "0.24713890075683687", "76RWH37C+4WXM"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - int64

   * - vpu_id
     - VPU identifier.
     - object

   * - type
     -  Type of catchment (e.g., independent, connector, aggregate).
     - object

   * - area_sqkm
     - Area in square kilometers.
     - float64

   * - bexp_mode
     - Beta exponent on Clapp-Hornberger (1978) soil water relations.
     - float64

   * - isltyp_mode
     - isltyp_mode
     - float64

   * - ivgtyp_mode
     - ivgtyp_mode
     - float64

   * - dksat_geomean
     - dksat_geomean
     - float64

   * - psisat_geomean
     - psisat_geomean
     - float64

   * - cwpvt_mean
     - cwpvt_mean
     - float64

   * - mp_mean
     - mp_mean
     - float64

   * - mfsno_mean
     - mfsno_mean
     - float64

   * - quartz_mean
     - quartz_mean
     - float64

   * - refkdt_mean
     - refkdt_mean
     - float64

   * - slope1km_mean
     - slope1km_mean
     - float64

   * - smcmax_mean
     - smcmax_mean
     - float64

   * - smcwlt_mean
     - smcwlt_mean
     - float64

   * - vcmx_mean
     - vcmx_mean
     - float64

   * - imperv_mean
     - imperv_mean
     - float64

   * - twi_q25
     - twi_q25
     - float64

   * - twi_q50
     - twi_q50
     - float64

   * - twi_q75
     - twi_q75
     - float64

   * - twi_q100
     - twi_q100
     - float64

   * - twi_q10
     - twi_q10
     - float64

   * - twi_q20
     - twi_q20
     - float64

   * - twi_q30
     - twi_q30
     - float64

   * - twi_q40
     - twi_q40
     - float64

   * - twi_q60
     - twi_q60
     - float64

   * - twi_q70
     - twi_q70
     - float64

   * - twi_q80
     - twi_q80
     - float64

   * - twi_q90
     - twi_q90
     - float64

   * - elevation_mean
     - elevation_mean
     - float64

   * - slope250m_mean
     - slope250m_mean
     - float64

   * - aspect_circmean
     - aspect_circmean
     - float64

   * - lzfpm_mean
     - lzfpm_mean
     - float64

   * - lzpk_mean
     - lzpk_mean
     - float64

   * - lztwm_mean
     - lztwm_mean
     - float64

   * - rexp_mean
     - rexp_mean
     - float64

   * - uzk_mean
     - uzk_mean
     - float64

   * - zperc_mean
     - zperc_mean
     - float64

   * - lzfsm_mean
     - lzfsm_mean
     - float64

   * - lzsk_mean
     - lzsk_mean
     - float64

   * - pfree_mean
     - pfree_mean
     - float64

   * - uzfwm_mean
     - uzfwm_mean
     - float64

   * - uztwm_mean
     - uztwm_mean
     - float64

   * - mfmin_mean
     - mfmin_mean
     - float64

   * - mfmax_mean
     - mfmax_mean
     - float64

   * - uadj_mean
     - uadj_mean
     - float64

   * - a_xinanjiang_inflection_point_parameter
     - a_xinanjiang_inflection_point_parameter
     - float64

   * - b_xinanjiang_shape_parameter
     - b_xinanjiang_shape_parameter
     - float64

   * - x_xinanjiang_shape_parameter
     - x_xinanjiang_shape_parameter
     - float64

   * - temp_delta_jan_mean
     - temp_delta_jan_mean
     - float64

   * - temp_delta_feb_mean
     - temp_delta_feb_mean
     - float64

   * - temp_delta_mar_mean
     - temp_delta_mar_mean
     - float64

   * - temp_delta_apr_mean
     - temp_delta_apr_mean
     - float64

   * - temp_delta_may_mean
     - temp_delta_may_mean
     - float64

   * - temp_delta_jun_mean
     - temp_delta_jun_mean
     - float64

   * - temp_delta_jul_mean
     - temp_delta_jul_mean
     - float64

   * - temp_delta_aug_mean
     - temp_delta_aug_mean
     - float64

   * - temp_delta_sep_mean
     - temp_delta_sep_mean
     - float64

   * - temp_delta_oct_mean
     - temp_delta_oct_mean
     - float64

   * - temp_delta_nov_mean
     - temp_delta_nov_mean
     - float64

   * - temp_delta_dec_mean
     - temp_delta_dec_mean
     - float64

   * - lat
     - lat
     - float64

   * - lon
     - lon
     - float64

   * - glacier_percent
     - glacier_percent
     - float64

   * - cgw
     - cgw
     - float64

   * - expon
     - expon
     - float64

   * - max_gw_storage
     - max_gw_storage
     - float64

   * - gid
     - gid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-virtual_nexus:

ngen_hydrofabric_file (layer: virtual_nexus)
--------------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "virtual_nex_id", "dn_virtual_fp_id", "vpu_id", "gid"
   "1073625603369834", "1073625600290348.0", "03S", "76RWG233+36HP"
   "1073625600265404", "nan", "03S", "76RWG223+M5G6"
   "1073625638488751", "1073601254009571.0", "03S", "76RWG2J2+H3VH"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - virtual_nex_id
     - virtual_nex_id
     - int64

   * - dn_virtual_fp_id
     - dn_virtual_fp_id
     - float64

   * - vpu_id
     - VPU identifier.
     - object

   * - gid
     - gid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-virtual_flowpaths:

ngen_hydrofabric_file (layer: virtual_flowpaths)
------------------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "virtual_fp_id", "dn_virtual_nex_id", "up_virtual_nex_id", "segment_order", "length_km", "area_sqkm", "percentage_area_contribution", "vpu_id", "gid"
   "1073625603433989", "1073625603369834", "nan", "0", "0.22945766942412782", "0.024299959500044346", "0.10131315957275082", "03S", "76RWG233+F6XF"
   "1073625600290348", "1073625600265404", "1073625603369834.0", "0", "0.12622339396322607", "0.21555002250150465", "0.8986868404272491", "03S", "76RWG223+R7VC"
   "1073625648634080", "1073625638488751", "nan", "0", "2.8547755376581905", "4.12830031049159", "0.044587662380177334", "03S", "76RWG2Q5+X762"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - virtual_fp_id
     - virtual_fp_id
     - int64

   * - dn_virtual_nex_id
     - dn_virtual_nex_id
     - int64

   * - up_virtual_nex_id
     - up_virtual_nex_id
     - float64

   * - segment_order
     - segment_order
     - int64

   * - length_km
     - flowpath length in kilometers.
     - float64

   * - area_sqkm
     - Area in square kilometers.
     - float64

   * - percentage_area_contribution
     - percentage_area_contribution
     - float64

   * - vpu_id
     - VPU identifier.
     - object

   * - gid
     - gid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-gages:

ngen_hydrofabric_file (layer: gages)
------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "site_no", "status", "hy_id", "USGS_basin_km2", "ref_fp_id", "method_fp_to_gage", "fp_id", "virtual_fp_id", "div_id", "dn_nex_id", "dn_virtual_nex_id", "mainstem_virtual_fp_id", "segment_order", "gid"
   "02228500", "USGS-active", "4692", "560.6082270794653", "18258887", "nldi_area", "1270208980455354.0", "1270208980455355.0", "1270208980455354.0", "1270208968180698.0", "1270208968180716.0", "1270208980455355.0", "0.0", "862VGQ89+RW9P"
   "02229000", "USGS-discontinued", "4693", "302.88413106308013", "18260281", "nldi_area", "1270206365122818.0", "1270206365122819.0", "1270206365122818.0", "1270206391622231.0", "1270206391622568.0", "1270206365122819.0", "0.0", "862VCPF4+292W"
   "02229250", "USGS-discontinued", "4694", "484.1818008805909", "18260257", "nldi_area", "1270206433877251.0", "1270206433877268.0", "1270206433877251.0", "1270206428314545.0", "1270206428314546.0", "1270206433877268.0", "0.0", "862VCQGH+PM4H"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - site_no
     - USGS gage ID.
     - object

   * - status
     - Status of the gage (e.g., active, discontinued).
     - object

   * - hy_id
     - hy_id
     - int64

   * - USGS_basin_km2
     - USGS_basin_km2
     - float64

   * - ref_fp_id
     - ref_fp_id
     - int64

   * - method_fp_to_gage
     - method_fp_to_gage
     - object

   * - fp_id
     - Unique identifier for the flowpath. Shares the same value with the corresponding catchment's div_id.
     - float64

   * - virtual_fp_id
     - virtual_fp_id
     - float64

   * - div_id
     - Unique identifier for each catchment.
     - float64

   * - dn_nex_id
     - Unique identifier for the downstream nexus that the catchment flows to.
     - float64

   * - dn_virtual_nex_id
     - dn_virtual_nex_id
     - float64

   * - mainstem_virtual_fp_id
     - mainstem_virtual_fp_id
     - float64

   * - segment_order
     - segment_order
     - float64

   * - gid
     - gid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-lakes:

ngen_hydrofabric_file (layer: lakes)
------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "nhf_lake_id", "ref_fp_id", "hy_id", "fp_id", "virtual_fp_id", "dn_nex_id", "dn_virtual_nex_id", "div_id", "lake_id", "res_id", "LkArea", "LkMxE", "WeirC", "WeirL", "WeirE", "OrificeC", "OrificeA", "OrificeE", "Dam_Length", "ifd", "reservoir_index_AnA", "reservoir_index_Extended_AnA", "reservoir_index_GDL_AK", "reservoir_index_Medium_Range", "reservoir_index_Short_Range", "dam_id", "nidid"
   "1271727565918156", "6331632", "27535", "1271727562255298.0", "1271727562255299", "1271727569480461.0", "1271727569480462", "1271727562255298", "9954464.0", "None", "0.3132413923740387", "244.04933166503906", "0.4000000059604645", "563.0", "242.44932556152344", "0.10000000149011612", "0.8999999761581421", "236.89999389648438", "563.0", "0.8989999890327454", "nan", "nan", "nan", "nan", "nan", "ls-52374", "GA06854"
   "1271730275961252", "24110441", "27537", "1271730275923486.0", "1271730285118559", "1271730260650685.0", "1271730275952754", "1271730275923486", "1048623.0", "None", "0.7542736530303955", "263.0191345214844", "0.4000000059604645", "1068.0", "263.0191345214844", "0.10000000149011612", "0.8999999761581421", "263.0191345214844", "1068.0", "0.8989999890327454", "nan", "nan", "nan", "nan", "nan", "ls-52503", "GA01921"
   "1271692424907145", "6338198", "27560", "1271692421891217.0", "1271692421891218", "1271692427966886.0", "1271692427966887", "1271692421891217", "6337132.0", "None", "0.2783222198486328", "263.54998779296875", "0.4000000059604645", "746.0", "263.54998779296875", "0.10000000149011612", "1.5", "263.54998779296875", "746.0", "0.8989999890327454", "nan", "nan", "nan", "nan", "nan", "ls-51655", "GA04532"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - nhf_lake_id
     - nhf_lake_id
     - int64

   * - ref_fp_id
     - ref_fp_id
     - int64

   * - hy_id
     - hy_id
     - int64

   * - fp_id
     - Unique identifier for the flowpath. Shares the same value with the corresponding catchment's div_id.
     - float64

   * - virtual_fp_id
     - virtual_fp_id
     - int64

   * - dn_nex_id
     - Unique identifier for the downstream nexus that the catchment flows to.
     - float64

   * - dn_virtual_nex_id
     - dn_virtual_nex_id
     - int64

   * - div_id
     - Unique identifier for each catchment.
     - int64

   * - lake_id
     - lake_id
     - float64

   * - res_id
     - res_id
     - object

   * - LkArea
     - LkArea
     - float64

   * - LkMxE
     - LkMxE
     - float64

   * - WeirC
     - WeirC
     - float64

   * - WeirL
     - WeirL
     - float64

   * - WeirE
     - WeirE
     - float64

   * - OrificeC
     - OrificeC
     - float64

   * - OrificeA
     - OrificeA
     - float64

   * - OrificeE
     - OrificeE
     - float64

   * - Dam_Length
     - Dam_Length
     - float64

   * - ifd
     - ifd
     - float64

   * - reservoir_index_AnA
     - reservoir_index_AnA
     - float64

   * - reservoir_index_Extended_AnA
     - reservoir_index_Extended_AnA
     - float64

   * - reservoir_index_GDL_AK
     - reservoir_index_GDL_AK
     - float64

   * - reservoir_index_Medium_Range
     - reservoir_index_Medium_Range
     - float64

   * - reservoir_index_Short_Range
     - reservoir_index_Short_Range
     - float64

   * - dam_id
     - dam_id
     - object

   * - nidid
     - nidid
     - object

   * - geometry
     - geometry
     - geometry



.. _ngen_hydrofabric_file-layer-reference_flowpaths:

ngen_hydrofabric_file (layer: reference_flowpaths)
--------------------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "ref_fp_id", "fp_id", "virtual_fp_id", "div_id", "mainstem_virtual_fp_id", "segment_order", "gid"
   "10245973", "1073625600290331.0", "1073625600290348", "1073625600290331", "1073625600290348", "0", "76RWG223+R7RH"
   "10247857", "nan", "1073625603433989", "1073625600290331", "1073625600290348", "0", "None"
   "10249847", "1073625637040207.0", "1073601254009571", "1073625637040207", "1073601254009571", "1", "76RWG2HH+G2G9"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - ref_fp_id
     - ref_fp_id
     - int64

   * - fp_id
     - Unique identifier for the flowpath. Shares the same value with the corresponding catchment's div_id.
     - float64

   * - virtual_fp_id
     - virtual_fp_id
     - int64

   * - div_id
     - Unique identifier for each catchment.
     - int64

   * - mainstem_virtual_fp_id
     - mainstem_virtual_fp_id
     - int64

   * - segment_order
     - segment_order
     - int64

   * - gid
     - gid
     - object



.. _ngen_hydrofabric_file-layer-hydrolocations:

ngen_hydrofabric_file (layer: hydrolocations)
---------------------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "hy_id", "dn_nex_id", "dn_virtual_nex_id"
   "4692.0", "1270208968180698.0", "1270208968180716.0"
   "4693.0", "1270206391622231.0", "1270206391622568.0"
   "4694.0", "1270206428314545.0", "1270206428314546.0"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - hy_id
     - hy_id
     - int64

   * - dn_nex_id
     - Unique identifier for the downstream nexus that the catchment flows to.
     - float64

   * - dn_virtual_nex_id
     - dn_virtual_nex_id
     - float64



.. _ngen_hydrofabric_file-layer-nhd:

ngen_hydrofabric_file (layer: nhd)
----------------------------------

NGEN Hydrofabric for a VPU.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - nhd_feature_id
     - nhd_feature_id
     - int64

   * - ref_id
     - ref_id
     - int64

   * - percent_inside
     - percent_inside
     - float64




.. _streamcat-attr_data_file:

streamcat.attr_data_file
------------------------

File containing StreamCat attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/streamcat/attr_streamcat_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "BFI", "CanalDens", "DamDens", "DamNIDStor", "DamNrmStor", "Elev", "Perm", "Om", "RckDep", "WtDep", "AgKffact", "Kffact", "PctAlkIntruVol", "PctAlluvCoast", "PctCarbResid", "PctCoastCrs", "PctColluvSed", "PctEolCrs", "PctEolFine", "PctExtruVol", "PctGlacLakeCrs", "PctGlacLakeFine", "PctGlacTilClay", "PctGlacTilCrs", "PctGlacTilLoam", "PctHydric", "PctNonCarbResid", "PctSalLake", "PctSilicic", "PctWater", "Precip", "Tmax", "Tmean", "Tmin", "RdDens", "Runoff", "Clay", "Sand", "Precip_Minus_EVT"
   "1062397347513500", "9.0", "0.0", "0.015499999999999998", "4295.9815", "1265.7803", "941.7036", "4.7678", "0.8045", "141.0672", "181.5667", "0.1199", "0.3051", "0.0", "88.78999999999999", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "11.21", "0.0", "0.0", "0.0", "499.1131932460042", "30.20575664900043", "23.68772554454508", "7.796952694350473", "3.6119", "5.0", "29.9103", "27.316", "-62.4617"
   "1062398455086668", "9.0", "0.0", "0.015499999999999998", "4295.9815", "1265.7803", "941.7036", "4.7678", "0.8045", "141.0672", "181.5667", "0.11990000000000002", "0.3051", "0.0", "88.79", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "11.21", "0.0", "0.0", "0.0", "499.11319324600413", "30.20575664900043", "23.687725544545085", "7.796952694350473", "3.6119", "5.0", "29.9103", "27.316000000000003", "-62.4617"
   "1062398518868817", "9.0", "0.0", "0.0155", "4295.9815", "1265.7803", "941.7036", "4.7678", "0.8045", "141.0672", "181.5667", "0.11989999999999999", "0.3051", "0.0", "88.78999999999999", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "11.21", "0.0", "0.0", "0.0", "499.1131932460042", "30.20575664900043", "23.687725544545085", "7.796952694350473", "3.6119", "5.0", "29.910299999999996", "27.316", "-62.4617"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - string

   * - BFI
     - Baseflow is the component of streamflow that can be attributed to ground-water discharge into streams. The Baseflow Index (BFI) is the ratio of baseflow to total flow, expressed as a percentage, within catchment.
     - float64

   * - CanalDens
     - Density of NHDPlus line features classified as canal, ditch, or pipeline within the catchment or watershed.
     - float64

   * - DamDens
     - Density of georeferenced dams within catchment (dams/ square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - DamNIDStor
     - Total possible volume of all reservoirs (NID_STORA in NID) per unit area of catchment (cubic meters/square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - DamNrmStor
     - Normal (most common) volume of all reservoirs (NORM_STORA in NID) per unit area of catchment (cubic meters/square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - Elev
     - Mean catchment elevation in meters.
     - float64

   * - Perm
     - Mean permeability (cm/hour) of soils (STATSGO) within catchment.
     - float64

   * - Om
     - Mean organic matter content (% by weight) of soils (STATSGO) within catchment.
     - float64

   * - RckDep
     - Mean depth (cm) to bedrock of soils (STATSGO) within catchment.
     - float64

   * - WtDep
     - Mean seasonal water table depth (cm) of soils (STATSGO) within catchment.
     - float64

   * - AgKffact
     - Mean soil erodibility (Kf) factor (unitless) of soils within catchment on agricultural land. The Kf factor is used in the Universal Soil Loss Equation (USLE) and represents a relative index of susceptibility of bare, cultivated soil to particle detachment and transport by rainfall.
     - float64

   * - Kffact
     - Mean soil erodibility (Kf) factor (unitless) of soils within catchment. The Kf factor is used in the Universal Soil Loss Equation (USLE) and represents a relative index of susceptibility of bare, cultivated soil to particle detachment and transport by rainfall.
     - float64

   * - PctAlkIntruVol
     - % of catchment area classified as lithology type: alkaline intrusive volcanic rock
     - float64

   * - PctAlluvCoast
     - % of catchment area classified as lithology type: alluvium and fine-textured coastal zone sediment
     - float64

   * - PctCarbResid
     - % of catchment area classified as lithology type: carbonate residual material
     - float64

   * - PctCoastCrs
     - % of catchment area classified as lithology type: coastal zone sediment, coarse-textured
     - float64

   * - PctColluvSed
     - % of catchment area classified as lithology type: colluvial sediment
     - float64

   * - PctEolCrs
     - % of catchment area classified as lithology type: eolian sediment, coarse-textured (sand dunes)
     - float64

   * - PctEolFine
     - % of catchment area classified as lithology type: eolian sediment, fine-textured (glacial loess)
     - float64

   * - PctExtruVol
     - % of catchment area classified as lithology type: extrusive volcanic rock
     - float64

   * - PctGlacLakeCrs
     - % of catchment area classified as lithology type: glacial outwash and glacial lake sediment, coarse-textured
     - float64

   * - PctGlacLakeFine
     - % of catchment area classified as lithology type: glacial lake sediment, fine-textured
     - float64

   * - PctGlacTilClay
     - % of catchment area classified as lithology type: glacial till, clayey
     - float64

   * - PctGlacTilCrs
     - % of catchment area classified as lithology type: glacial till, coarse-textured
     - float64

   * - PctGlacTilLoam
     - % of catchment area classified as lithology type: glacial till, loamy
     - float64

   * - PctHydric
     - % of catchment area classified as lithology type: hydric, peat and muck
     - float64

   * - PctNonCarbResid
     - % of catchment area classified as lithology type: non-carbonate residual material
     - float64

   * - PctSalLake
     - % of catchment area classified as lithology type: saline like sediment
     - float64

   * - PctSilicic
     - % of catchment area classified as lithology type: silicic residual material
     - float64

   * - PctWater
     - % of catchment area classified as lithology type: water
     - float64

   * - Precip
     - PRISM climate data - 30-year normal mean precipitation (mm): Annual period: 1981-2010 within catchment
     - float64

   * - Tmax
     - PRISM climate data - 30-year normal maximum temperature (Â°C): Annual period: 1981-2010 within catchment
     - float64

   * - Tmean
     - PRISM climate data - 30-year normal mean temperature (Â°C): Annual period: 1981-2010 within the catchment
     - float64

   * - Tmin
     - PRISM climate data - 30-year normal minimum temperature (Â°C): Annual period: 1981-2010 within catchment
     - float64

   * - RdDens
     - Density of roads (2010 Census Tiger Lines) within catchment (km/square km)
     - float64

   * - Runoff
     - Mean runoff (mm) within catchment
     - float64

   * - Clay
     - Mean % clay content of soils (STATSGO) within catchment.
     - float64

   * - Sand
     - Mean % sand content of soils (STATSGO) within catchment.
     - float64

   * - Precip_Minus_EVT
     - This dataset represents surplus precipitation (mm): precipitation minus potential evaporation described in DOI: 10.1016/j.scitotenv.2020.137661 within individual,  local NHDPlusV2 catchments and upstream, contributing watersheds.
     - float64




.. _streamcat-attr_select_file:

streamcat.attr_select_file
--------------------------

File to configure the selection of StreamCat attributes for parameter regionalization.

Sample file path: ``inputs/region/attr_config/attr_selection_streamcat.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "select", "attr_name", "description"
   "1", "BFI", "Baseflow is the component of streamflow that can be attributed to ground-water discharge into streams. The Baseflow Index (BFI) is the ratio of baseflow to total flow, expressed as a percentage, within catchment."
   "0", "CanalDens", "Density of NHDPlus line features classified as canal, ditch, or pipeline within the catchment or watershed."
   "1", "DamDens", "Density of georeferenced dams within catchment (dams/ square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - select
     - Whether to select this attribute for parameter regionalization (1 for yes, 0 for no).
     - int64

   * - attr_name
     - Name of the StreamCat attribute to be selected for parameter regionalization.
     - object

   * - description
     - Description of the StreamCat attribute.
     - object




.. toctree::
   :maxdepth: 2