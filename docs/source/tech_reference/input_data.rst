Schemas
=======

.. _calib_param_file:

calib_param_file
----------------

Calibrated parameters for various modules for all gages in an NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/pseudo_calib_params/sampled_params_conus.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "01010000", "noah-owp-modular cfe-s t-route", "2.5681848800643285", "0.3286171733536613", "98.26779571658672", "12.345915915145532", "34.57680991125569", "4.064091503042371", "0.9712745199335464", "3.7414847994010367", "0.0009141315202519", "0.2682757844834037", "0.7532535832349109", "0.4130823012978584", "0.2589183149092599", "0.1352373803701926", "0.0004228761310245", "1.1540687515916113", "0.3326644885346328", "0.8494590266511353", "3.7047342427645367", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "01010000", "noah-owp-modular snow-17 lasam t-route", "1.7202166366984653", "0.2830454483663369", "55.7216447075499", "7.395125941680879", "64.91094869284314", "4.532964185028021", "0.839432321093368", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.2549536985740628", "0.1149808945005032", "3395.942668181262", "0.0402573508525195", "1.3993208237988155", "0.1860697866529445", "0.4344457454145048", "2.8034892811290693", "0.1682210213074931", "0.0212834071116516", "0.1391684172778563", "0.7052654753641924", "0.1892796609353877", "1.8393994158286835", "0.8245934418227354", "2.6163411478418066", "85.65653278592669", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "01010000", "noah-owp-modular ueb cfe-x t-route", "1.6984225027876014", "0.1138073585146865", "44.18211099270653", "10.7458769168222", "41.55877300879165", "2.6584257451986466", "0.9894877010479544", "6.451208746356487", "0.0009931305806678", "0.4331962074757012", "0.2281443013468404", "0.2915759136119435", "0.1545028069618073", "0.1101811687158985", "0.00173408132033", "4.603211031471964", "0.9632723151253538", "0.1889839116526389", "0.1175267001634975", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "1.451971818772199", "0.2253714587504531", "2.6267503130197287", "1.0381689683179314", "0.2723324489894099", "0.9878101435547773", "2.104278810378881", "0.0096068438949711", "346.4354100199481", "1291.644609708449", "6.939487504771504", "0.3945507373583731", "0.8990968927991766", "83059.92094090296", "-0.4349516338584633", "2.974069284705172", "4.643406523991181", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each calibration gage.
     - object

   * - formulation
     - NextGen formualtion calibrated for a given gage (e.g., nom-cfes, nom-sac)
     - object

   * - MFSNO
     - NOM parameter: Melt factor for snow depletion curve
     - float64

   * - CWP
     - NOM parameter: Canopy water capacity
     - float64

   * - VCMX25
     - NOM parameter: Maximum canopy storage
     - float64

   * - MP
     - NOM parameter: MP
     - float64

   * - RSURF_SNOW
     - NOM parameter: Snow surface roughness
     - float64

   * - RSURF_EXP
     - NOM parameter: Snow surface roughness exponent
     - float64

   * - SCAMAX
     - NOM parameter: SCAMAX
     - float64

   * - b
     - CFE parameter: b
     - float64

   * - satdk
     - CFE parameter: satdk
     - float64

   * - satpsi
     - CFE parameter: satpsi
     - float64

   * - slope
     - CFE parameter: slope
     - float64

   * - maxsmc
     - CFE parameter: maxsmc
     - float64

   * - wltsmc
     - CFE parameter: wltsmc
     - float64

   * - max_gw_storage
     - CFE parameter: max_gw_storage
     - float64

   * - Cgw
     - CFE parameter: Cgw
     - float64

   * - expon
     - CFE parameter: expon
     - float64

   * - Kn
     - CFE parameter: Kn
     - float64

   * - Klf
     - CFE parameter: Klf
     - float64

   * - refkdt
     - CFE parameter: refkdt
     - float64

   * - mfmax
     - snow-17 parameter: mfmax
     - float64

   * - uadj
     - snow-17 parameter: uadj
     - float64

   * - si
     - snow-17 parameter: si
     - float64

   * - mfmin
     - snow-17 parameter: mfmin
     - float64

   * - scf
     - snow-17 parameter: scf
     - float64

   * - nmf
     - snow-17 parameter: nmf
     - float64

   * - tipm
     - snow-17 parameter: tipm
     - float64

   * - pxtemp
     - snow-17 parameter: pxtemp
     - float64

   * - plwhc
     - snow-17 parameter: plwhc
     - float64

   * - daygm
     - snow-17 parameter: daygm
     - float64

   * - smcmin
     - lasam parameter: smcmin
     - float64

   * - smcmax
     - lasam parameter: smcmax
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
     - lasam parameter: ponded_depth_max
     - float64

   * - field_capacity
     - lasam parameter: field_capacity
     - float64

   * - df
     - UEB parameter: df
     - float64

   * - cc
     - UEB parameter: cc
     - float64

   * - hcan
     - UEB parameter: hcan
     - float64

   * - lai
     - UEB parameter: lai
     - float64

   * - subalb
     - UEB parameter: subalb
     - float64

   * - ems
     - UEB parameter: ems
     - float64

   * - cg
     - UEB parameter: cg
     - float64

   * - zo
     - UEB parameter: zo
     - float64

   * - rho
     - UEB parameter: rho
     - float64

   * - rhog
     - UEB parameter: rhog
     - float64

   * - Ks
     - UEB parameter: Ks
     - float64

   * - de
     - UEB parameter: de
     - float64

   * - avo
     - UEB parameter: avo
     - float64

   * - apr
     - UEB parameter: apr
     - float64

   * - a_Xinanjiang_inflection_point_parameter
     - CFE-X parameter: a_Xinanjiang_inflection_point_parameter
     - float64

   * - b_Xinanjiang_shape_parameter
     - CFE-X parameter: b_Xinanjiang_shape_parameter
     - float64

   * - x_Xinanjiang_shape_parameter
     - CFE-X parameter: x_Xinanjiang_shape_parameter
     - float64

   * - uztwm
     - sac-sma parameter: uztwm
     - float64

   * - uzfwm
     - sac-sma parameter: uzfwm
     - float64

   * - lztwm
     - sac-sma parameter: lztwm
     - float64

   * - lzfsm
     - sac-sma parameter: lzfsm
     - float64

   * - lzfpm
     - sac-sma parameter: lzfpm
     - float64

   * - adimp
     - sac-sma parameter: adimp
     - float64

   * - uzk
     - sac-sma parameter: uzk
     - float64

   * - lzpk
     - sac-sma parameter: lzpk
     - float64

   * - lzsk
     - sac-sma parameter: lzsk
     - float64

   * - zperc
     - sac-sma parameter: zperc
     - float64

   * - rexp
     - sac-sma parameter: rexp
     - float64

   * - pctim
     - sac-sma parameter: pctim
     - float64

   * - pfree
     - sac-sma parameter: pfree
     - float64

   * - riva
     - sac-sma parameter: riva
     - float64

   * - side
     - sac-sma parameter: side
     - float64




.. _calval_stats_file:

calval_stats_file
-----------------

Calibration and validation statistics for all gages in an NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/calval_stats/stat_calval_all_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "formulation", "gage_id", "evalPeriod", "bias", "rmse", "cor", "nse", "nselog", "nseWt", "kge", "msof", "hyperResMultiObj", "nnsesq", "eventmultiobj", "lbem", "lbemprime", "corr1", "pod", "far", "csi", "nnse", "peak_bias", "peak_tm_err_hr", "event_volume_bias"
   "noah-owp-modular cfe-s t-route", "01010000", "calib", "-4.22313711118399", "6.340465322534651", "0.688672993019667", "0.352110886451316", "0.289938317202322", "0.3210246018268189", "0.683557516268751", "1197.87649904829", "0.3407426694755759", "0.3525668325301929", "96.2420588007148", "-14.6322865028915", "-2.3165845788185697", "0.614269192322281", "0.6734475374732329", "0.467174925878865", "0.423426455738808", "0.606836947812907", "120.710086685077", "8.1", "59.5400169741716"
   "noah-owp-modular cfe-s t-route", "01010000", "full", "-15.5504575885424", "5.76809385974621", "0.6929937073565079", "0.3606695975617929", "-0.0769408622647187", "0.141864367648537", "0.654327254839115", "1357.91116071561", "0.3847846675916339", "0.360173479418255", "94.85988221191192", "-5.0865720336511", "-0.888828280571734", "0.6233670936801109", "0.522358859698155", "0.3853995396251229", "0.393473684210526", "0.610005157296345", "118.327573987421", "7.63414634146341", "59.6583445486478"
   "noah-owp-modular cfe-s t-route", "01010000", "valid", "-37.4902702855678", "4.54614536935466", "0.712848487187317", "0.388788333058551", "-0.575071079915985", "-0.0931413734287169", "0.527757083492435", "640.108086710608", "0.302740552732747", "0.471794395615111", "81.3309055664079", "-100.72445737502", "-8.38400037333542", "0.623214128732094", "0.3573099415204679", "0.101470588235294", "0.3434513771781899", "0.6206509178885811", "109.960685728188", "8.04", "38.3862353237379"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - formulation
     - NextGen formualtion calibrated for a given gage
     - object

   * - gage_id
     - Unique identifier for each gage
     - object

   * - evalPeriod
     - Evaluation period for the statistics (e.g., calibration, validation, and full periods)
     - object

   * - bias
     - Metric: bias
     - float64

   * - rmse
     - Metric: root mean square error
     - float64

   * - cor
     - Metric: Pearson correlation
     - float64

   * - nse
     - Metric: Nash-Sutcliffe efficiency
     - float64

   * - nselog
     - Metric: Nash-Sutcliffe efficiency (logarithmic)
     - float64

   * - nseWt
     - Metric: weighted Nash-Sutcliffe efficiency    
     - float64

   * - kge
     - Metric: Kling-Gupta efficiency
     - float64

   * - msof
     - Metric: mean squared error of the forecast
     - float64

   * - hyperResMultiObj
     - Metric: hyper-resolution multi-objective
     - float64

   * - nnsesq
     - Metric: normalized Nash-Sutcliffe efficiency squared
     - float64

   * - eventmultiobj
     - Metric: event-based multi-objective
     - float64

   * - lbem
     - Metric: log bias error metric
     - float64

   * - lbemprime
     - Metric: modified log bias error metric
     - float64

   * - corr1
     - Metric: correlation coefficient 1
     - float64

   * - pod
     - Metric: probability of detection
     - float64

   * - far
     - Metric: false alarm ratio
     - float64

   * - csi
     - Metric: critical success index
     - float64

   * - nnse
     - Metric: normalized Nash-Sutcliffe efficiency
     - float64

   * - peak_bias
     - Metric: event peak bias
     - float64

   * - peak_tm_err_hr
     - Metric: event peak time error in hours
     - float64

   * - event_volume_bias
     - Metric: event volume bias
     - float64




.. _divide_huc12_cwt_file:

divide_huc12_cwt_file
---------------------

Catchment to HUC12 mapping file used in formulation regionalization. Each catchment may overlap with multiple HUC12 watersheds. It is desirable for the total overlap percentage for any given catchment to be as close to 100% as possible.

Sample file path: ``inputs/region/cwt_divide_huc12/cwt_divide_huc12_conus.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "huc_12", "overlap_area", "areasqkm", "original_area", "overlap_percentage", "nearest_dist_m"
   "cat-1", "11000060401", "0.1", "0.07", "0.12", "86.07", "nan"
   "cat-10", "11000030301", "0.0", "0.0", "0.0", "31.13", "nan"
   "cat-100", "10900020107", "97.01", "57.42", "103.64", "93.61", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - huc_12
     - 12-digit Hydrologic Unit Code (HUC12) representing the watershed in which the catchment is located.
     - int64

   * - overlap_area
     - Area of overlap between the catchment and the HUC12 watershed.
     - float64

   * - areasqkm
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
   "noah-owp-modular cfe-x t-route", "10"
   "noah-owp-modular lasam t-route", "15"

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

   "gage_id", "divide_id", "toid", "areasqkm", "vpuid", "type"
   "02365470", "cat-503034", "nex-503035", "16.58834950949662", "03W", "network"
   "02365470", "cat-503032", "nex-503033", "11.973599720998799", "03W", "network"
   "02365470", "cat-503033", "nex-503034", "10.24515036450065", "03W", "network"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each gage.
     - object

   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - toid
     - Unique identifier for the nexus that the catchment flows to.
     - object

   * - areasqkm
     - Area of the catchment in square kilometers.
     - float64

   * - vpuid
     - VPU the catchment belongs to.
     - object

   * - type
     - type
     - object




.. _hlr-attr_data_file:

hlr.attr_data_file
------------------

File containing HLR attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/hlr/attr_hlr_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "AQPERMNEW", "SLOPE", "TAVE", "PPT", "PET", "SAND", "PMPE", "MINELE", "RELIEF", "PFLATTOT", "PFLATLOW", "PFLATUP"
   "cat-10", "1.0", "0.98096299171", "49.68560028076", "47.39239883423", "25.74370002747", "47.66790008545", "21.64870071411", "0.0", "91.0", "47.0", "36.0", "11.0"
   "cat-100", "4.062233885523227", "0.7358617228741067", "49.32496685256188", "47.28242879080685", "25.56762630800962", "75.67956712022041", "21.714803633677842", "0.0", "98.86110218981413", "64.08453199974686", "59.65283519760585", "4.431696802141013"
   "cat-1000", "1.0", "5.13249015808", "39.36360168457", "39.26169967651", "20.641599655150003", "27.19339942932", "18.62010002136", "203.00000000000003", "761.9999999999999", "8.0", "8.0", "0.0"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - divide_id
     - object

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

   * - SAND
     - percentage of sand in the soil
     - float64

   * - PMPE
     - mean annual precpitation minus PET
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
   "1", "AQPERMNEW", "aquifer permeability"
   "0", "SLOPE", "mean slope"
   "1", "TAVE", "mean annual temperature"

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
   "1", "0.043", "0.005", "0.139", "2.0", "0.0", "0.0", "0.0", "1.0", "0.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.952", "4.809", "2.73", "5.018", "848.0", "223.0", "281.0", "82.0", "917.0", "31.0", "44.0", "72.0", "15.0", "103.0", "223.0", "222.00000000000003", "115.00000000000001", "339.0", "115.00000000000001", "142.0", "169.0", "210.00000000000003", "255.0", "306.0", "339.0", "332.0", "295.0", "232.0", "159.0", "116.0", "95.0", "99.0", "13.0", "10.0", "10.0", "4.0", "1.0", "1.0", "8.0", "17.0", "11.0", "6.0", "6.0", "10.0", "1740.0000000000002", "1712.9999999999998", "60.0", "77.0", "119.00000000000001", "159.0", "206.0", "236.0", "240.0", "216.0", "172.0", "124.0", "74.0", "56.0", "78.0", "82.0", "4.0", "7.0", "10.0", "11.0", "9.0", "6.0", "5.0", "8.0", "7.0", "5.0", "3.0", "3.0", "6.0", "6.0", "-94.0", "-94.0", "-78.0", "-87.0", "-92.0", "-98.0", "-100.0", "-100.0", "-97.0", "-92.0", "-94.0", "-95.0", "-92.0", "-82.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "14.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "17.0", "34.0", "0.0", "49.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "10.0", "71.0", "0.0", "19.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.0", "1.0", "58.0", "53.0", "5.0", "1.0", "0.0", "0.0", "0.0", "0.0", "9.0", "10.0", "13.0", "435.00000000000006", "4.0", "130.0", "18.0", "18.0", "31.0", "30.0", "51.0", "51.0", "5.0", "4.0", "5.0", "5.0", "8.0", "9.0", "9.0", "7.0", "2.0", "3.0", "4.0", "4.0", "4.0", "5.0", "1.0", "0.0", "1.0", "2710.0", "3269.0000000000005", "0.034", "0.036", "0.324", "0.092", "0.0", "0.0", "172.0", "0.0", "174.0", "68.0", "43.0", "35.0", "55.0", "45.0", "240.0", "55767.99999999999", "708852.0", "815795.0", "951.0"
   "2", "0.105", "0.011", "0.333", "2.0", "5.0", "2.0", "20.0", "7.0", "28.0", "10.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.669", "11.064", "8.674", "14.927", "380.0", "133.0", "221.0", "71.0", "824.0", "11.000000000000002", "32.0", "29.0", "15.0", "103.0", "225.0", "222.99999999999997", "116.0", "341.0", "117.0", "144.0", "173.0", "213.0", "258.0", "307.0", "341.0", "334.0", "298.0", "234.0", "161.0", "117.0", "84.0", "94.0", "12.0", "9.0", "9.0", "3.0", "0.0", "0.0", "6.0", "16.0", "10.0", "5.0", "5.0", "9.0", "1777.0", "1740.0", "62.0", "79.00000000000001", "123.0", "163.0", "210.99999999999997", "240.0", "244.0", "219.0", "176.00000000000003", "127.0", "76.00000000000001", "58.0", "68.0", "77.0", "4.0", "6.0", "9.0", "10.0", "8.0", "5.0", "4.0", "7.0", "6.0", "4.0", "3.0", "2.0", "5.0", "5.0", "-95.0", "-95.0", "-81.0", "-89.0", "-93.0", "-98.0", "-100.0", "-100.0", "-97.0", "-93.0", "-94.0", "-96.0", "-93.0", "-85.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "2.0", "33.0", "7.0", "26.0", "0.0", "30.0", "0.0", "0.0", "0.0", "0.0", "0.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "8.0", "57.0", "3.0", "21.0", "0.0", "11.000000000000002", "0.0", "0.0", "0.0", "0.0", "0.0", "1.0", "12.0", "0.0", "0.0", "0.0", "1.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "99.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "41.00000000000001", "16.0", "42.0", "54.0", "31.0", "14.0", "0.0", "0.0", "0.0", "0.0", "2.0", "9.0", "13.0", "435.0", "4.0", "130.0", "19.000000000000004", "18.0", "33.0", "30.0", "48.0", "49.0", "5.0", "5.0", "4.0", "5.0", "7.0", "8.0", "7.0", "6.0", "1.0", "2.0", "3.0", "3.0", "4.0", "4.0", "1.0", "0.0", "1.0", "1272.0", "2506.0", "3.283", "3.518", "14.116", "4.776", "1.0", "0.0", "956.0", "400.0", "451.0", "220.0", "99.0", "62.0", "108.0", "72.0", "240.0", "55768.0", "125292296.0", "138469984.0", "951.0"
   "3", "0.043", "0.005", "0.139", "2.0", "0.0", "0.0", "0.0", "1.0", "0.0", "2.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1.952", "4.809", "2.73", "5.018", "848.0", "223.00000000000003", "281.0", "82.0", "917.0", "31.0", "44.0", "72.0", "15.000000000000002", "103.00000000000001", "223.00000000000003", "222.0", "115.0", "339.0", "115.0", "142.0", "169.0", "210.0", "254.99999999999997", "306.0", "339.0", "332.0", "295.0", "232.0", "159.0", "116.0", "95.0", "99.0", "13.0", "10.0", "10.0", "4.0", "1.0", "1.0", "8.0", "17.0", "11.0", "6.0", "6.0", "10.0", "1740.0", "1713.0000000000002", "60.00000000000001", "77.0", "118.99999999999999", "159.0", "206.00000000000003", "236.0", "240.00000000000003", "215.99999999999997", "172.0", "124.0", "74.0", "56.0", "78.0", "82.0", "4.0", "7.0", "10.0", "11.0", "9.0", "6.0", "5.0", "8.0", "7.0", "5.0", "3.0", "3.0", "6.0", "6.0", "-94.0", "-94.0", "-78.0", "-87.0", "-92.00000000000001", "-98.00000000000001", "-100.0", "-100.0", "-96.99999999999999", "-92.00000000000001", "-94.0", "-95.0", "-92.00000000000001", "-82.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "14.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "17.0", "34.0", "0.0", "49.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "10.0", "71.0", "0.0", "19.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "12.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "-999.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "4.0", "1.0", "58.0", "53.0", "5.0", "1.0", "0.0", "0.0", "0.0", "0.0", "9.0", "10.0", "13.0", "435.0", "4.0", "130.0", "18.0", "18.0", "31.0", "30.000000000000004", "51.0", "51.0", "5.0", "4.0", "5.0", "5.0", "8.0", "9.0", "9.0", "7.0", "2.0", "3.0", "4.0", "4.0", "4.0", "5.0", "1.0", "0.0", "1.0", "2710.0", "3269.0", "0.034", "0.036", "0.324", "0.092", "0.0", "0.0", "172.0", "0.0", "174.0", "68.0", "43.0", "35.0", "55.0", "45.0", "240.00000000000003", "55768.0", "708852.0", "815794.9999999999", "951.0"

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

Sample file path: ``inputs/region/manual_pairs/manual_pairs_vpu03S.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "receiver_divide_id", "receiver_gage_id", "donor_divide_id", "donor_gage_id"
   "cat-410687", "nan", "cat-423550", "nan"
   "cat-410688", "nan", "cat-423550", "nan"
   "cat-423248", "nan", "nan", "023177483"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - receiver_divide_id
     - Unique identifier for the receiver catchment (i.e., divide).
     - object

   * - receiver_gage_id
     - Unique identifier for the receiver gage.
     - object

   * - donor_divide_id
     - Unique identifier for the donor catchment (i.e., divide).
     - object

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

   "divide_id", "dksat", "psisat", "smcmax", "smcwlt", "bexp", "ISLTYP", "IVGTYP", "cwpvt", "mfsno", "mp", "refkdt", "slope_1km", "vcmx25", "Coeff", "Zmax", "Expon", "centroid_x", "centroid_y", "impervious", "elevation", "slope", "aspect", "dist_4.twi", "vpuid"
   "cat-1", "3.7706361505216364e-06", "0.002322390575570931", "0.4108227789402008", "0.02800000086426735", "5.263515949249268", "2.0", "1.0", "0.29736316204071045", "1.529200792312622", "9.065110206604004", "2.0", "0.0017215368570759892", "0.0", "0.005", "65.92072", "4.0", "1855582.4996999947", "2222804.9979", "29.595956802368164", "405.9750577980771", "55.29506972992221", "132.27767251668186", "[{"v":0.3278,"frequency":0.25},{"v":1.84,"frequency":0.25},{"v":3.919,"frequency":0.25},{"v":5.827,"frequency":0.25}]", "01"
   "cat-10", "nan", "nan", "1.0", "0.0", "0.0", "14.0", "16.0", "0.2067982256412506", "0.7340455651283264", "8.536454200744629", "2.0", "0.0029178785625845194", "0.0", "0.005", "10.0", "4.0", "1974030.0036747975", "2288970.0", "81.0", "25.0", "26.443111419677734", "128.63633728027344", "[{"frequency":1}]", "01"
   "cat-100", "9.827454355434566e-07", "0.03887496207551378", "0.37793877720832825", "0.035677388310432434", "9.00599479675293", "3.0", "15.0", "0.23038434982299805", "2.9677577018737793", "11.994601249694824", "2.0", "0.40510448813438416", "49.06135559082031", "0.005", "17.37548", "4.0", "2071312.4998500296", "2375550.0027", "6.967351913452148", "2446.5645319672017", "69.54921143318134", "156.96108212234347", "[{"v":6.308,"frequency":0.2498},{"v":7.553,"frequency":0.2498},{"v":8.647,"frequency":0.2498},{"v":13.72,"frequency":0.2506}]", "01"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - divide_id
     - object

   * - dksat
     - dksat
     - float64

   * - psisat
     - psisat
     - float64

   * - smcmax
     - smcmax
     - float64

   * - smcwlt
     - smcwlt
     - float64

   * - bexp
     - bexp
     - float64

   * - ISLTYP
     - ISLTYP
     - float64

   * - IVGTYP
     - IVGTYP
     - float64

   * - cwpvt
     - cwpvt
     - float64

   * - mfsno
     - mfsno
     - float64

   * - mp
     - mp
     - float64

   * - refkdt
     - refkdt
     - float64

   * - slope_1km
     - slope_1km
     - float64

   * - vcmx25
     - vcmx25
     - float64

   * - Coeff
     - Coeff
     - float64

   * - Zmax
     - Zmax
     - float64

   * - Expon
     - Expon
     - float64

   * - centroid_x
     - centroid_x
     - float64

   * - centroid_y
     - centroid_y
     - float64

   * - impervious
     - impervious
     - float64

   * - elevation
     - elevation
     - float64

   * - slope
     - slope
     - float64

   * - aspect
     - aspect
     - float64

   * - dist_4.twi
     - dist_4.twi
     - object

   * - vpuid
     - vpuid
     - object




.. _ngen-attr_select_file:

ngen.attr_select_file
---------------------

File to configure the selection of NGEN attributes for parameter regionalization.

Sample file path: ``inputs/region/attr_config/attr_selection_ngen.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "select", "attr_name", "description"
   "1", "dksat", "NWM parameter | saturated hydraulic conductivity"
   "1", "psisat", "NWM parameter | saturated capillary head"
   "1", "smcmax", "NWM parameter | saturated soil moisture content"

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

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "id", "toid", "mainstem", "order", "hydroseq", "lengthkm", "areasqkm", "tot_drainage_areasqkm", "has_divide", "divide_id", "poi_id", "vpuid"
   "wb-423670", "nex-423671", "2367049.0", "1.0", "13878", "3.804038126747679", "13.50224937450011", "13.50224937450011", "True", "cat-423670", "19675", "03S"
   "wb-423671", "nex-423663", "2367049.0", "1.0", "13877", "2.3866099099488665", "6.21449990999961", "19.71674928449972", "True", "cat-423671", "30620", "03S"
   "wb-423752", "nex-423748", "2367253.0", "1.0", "13876", "5.861027417139365", "9.15119957699985", "9.15119957699985", "True", "cat-423752", "None", "03S"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - id
     - Identifier.
     - object

   * - toid
     - Identifier of the downstream feature (nexus) to which this catchment drains.
     - object

   * - mainstem
     - mainstem
     - float64

   * - order
     - order
     - float64

   * - hydroseq
     - hydroseq
     - int32

   * - lengthkm
     - Length in kilometers.
     - float64

   * - areasqkm
     - Area in square kilometers.
     - float64

   * - tot_drainage_areasqkm
     - Total drainage area in square kilometers.
     - float64

   * - has_divide
     - has_divide
     - bool

   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - poi_id
     - poi_id
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-divides:

ngen_hydrofabric_file (layer: divides)
--------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "toid", "type", "ds_id", "areasqkm", "vpuid", "id", "lengthkm", "tot_drainage_areasqkm", "has_flowline"
   "cat-410946", "inx-410946", "internal", "412593.0", "78.3864003508807", "03S", "None", "nan", "nan", "False"
   "cat-410945", "inx-410945", "internal", "412491.0", "587.9079171090782", "03S", "None", "nan", "nan", "False"
   "cat-410944", "inx-410944", "internal", "412643.0", "162.52922207240118", "03S", "None", "nan", "nan", "False"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - toid
     - Identifier of the downstream feature (nexus) to which this catchment drains.
     - object

   * - type
     - Type of feature (e.g., divide).
     - object

   * - ds_id
     - Drainage system identifier.
     - float64

   * - areasqkm
     - Area in square kilometers.
     - float64

   * - vpuid
     - VPU identifier.
     - object

   * - id
     - Identifier.
     - object

   * - lengthkm
     - Length in kilometers.
     - float64

   * - tot_drainage_areasqkm
     - Total drainage area in square kilometers.
     - float64

   * - has_flowline
     - Indicates if the catchment has a flowline.
     - bool

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-lakes:

ngen_hydrofabric_file (layer: lakes)
------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "lake_id", "LkArea", "LkMxE", "WeirC", "WeirL", "OrificeC", "OrificeA", "OrificeE", "WeirE", "ifd", "Dam_Length", "domain", "poi_id", "hf_id", "reservoir_index_AnA", "reservoir_index_Extended_AnA", "reservoir_index_GDL_AK", "reservoir_index_Medium_Range", "reservoir_index_Short_Range", "res_id", "vpuid", "lake_x", "lake_y"
   "55470.0", "29.46616114", "8.920000076293945", "0.4", "10.0", "0.1", "1.0", "5.333333492279053", "8.381999969482422", "0.8999999761581421", "10.0", "CONUS", "21", "68240.0", "nan", "nan", "nan", "nan", "nan", "None", "03S", "1578114.466138742", "542981.5336005107"
   "84908.0", "1.20577977", "0.33000001311302185", "0.4", "10.0", "0.1", "1.0", "-0.0833333283662796", "0.2679999768733978", "0.8999999761581421", "10.0", "CONUS", "22", "85362.0", "nan", "nan", "nan", "nan", "nan", "None", "03S", "1502038.5282795832", "403864.604164357"
   "84918.0", "29.73956508", "0.9599999785423279", "0.4", "10.0", "0.1", "1.0", "-0.013333320617675781", "0.8140000104904175", "0.8999999761581421", "10.0", "CONUS", "23", "85476.0", "nan", "nan", "nan", "nan", "nan", "None", "03S", "1506759.286453132", "398638.4477050715"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - lake_id
     - lake_id
     - float64

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

   * - OrificeC
     - OrificeC
     - float64

   * - OrificeA
     - OrificeA
     - float64

   * - OrificeE
     - OrificeE
     - float64

   * - WeirE
     - WeirE
     - float64

   * - ifd
     - ifd
     - float64

   * - Dam_Length
     - Dam_Length
     - float64

   * - domain
     - domain
     - object

   * - poi_id
     - poi_id
     - int32

   * - hf_id
     - hf_id
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

   * - res_id
     - res_id
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - lake_x
     - lake_x
     - float64

   * - lake_y
     - lake_y
     - float64

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-nexus:

ngen_hydrofabric_file (layer: nexus)
------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "id", "toid", "type", "vpuid", "poi_id"
   "nex-410950", "wb-410950", "nexus", "03S", "nan"
   "nex-410951", "wb-410951", "nexus", "03S", "35070.0"
   "nex-410952", "wb-410952", "nexus", "03S", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - id
     - Identifier.
     - object

   * - toid
     - Identifier of the downstream feature (nexus) to which this catchment drains.
     - object

   * - type
     - Type of feature (e.g., divide).
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - poi_id
     - poi_id
     - float64

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-pois:

ngen_hydrofabric_file (layer: pois)
-----------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "poi_id", "id", "nex_id", "vpuid"
   "19675", "wb-423670", "nex-423671", "03S"
   "30620", "wb-423671", "nex-423663", "03S"
   "33526", "wb-423728", "nex-423654", "03S"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - poi_id
     - poi_id
     - int32

   * - id
     - Identifier.
     - object

   * - nex_id
     - nex_id
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-hydrolocations:

ngen_hydrofabric_file (layer: hydrolocations)
---------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "poi_id", "id", "nex_id", "hf_id", "hl_link", "hl_reference", "hl_uri", "hl_source", "hl_x", "hl_y", "vpuid"
   "3746", "wb-424822", "nex-424823", "500802.0", "030801020801", "huc12", "huc12-030801020801", "ref-fab", "1373704.7076079391", "780484.8953634357", "03S"
   "5130", "wb-421607", "nex-421608", "527202.0", "030801030304", "huc12", "huc12-030801030304", "ref-fab", "1394634.9123926074", "823759.1819836448", "03S"
   "4244", "wb-411585", "nex-411586", "562802.0", "030901011304", "huc12", "huc12-030901011304", "ref-fab", "1443372.7137063795", "622233.1012130025", "03S"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - poi_id
     - poi_id
     - int32

   * - id
     - Identifier.
     - object

   * - nex_id
     - nex_id
     - object

   * - hf_id
     - hf_id
     - float64

   * - hl_link
     - hl_link
     - object

   * - hl_reference
     - hl_reference
     - object

   * - hl_uri
     - hl_uri
     - object

   * - hl_source
     - hl_source
     - object

   * - hl_x
     - hl_x
     - float64

   * - hl_y
     - hl_y
     - float64

   * - vpuid
     - VPU identifier.
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-flowpath-attributes:

ngen_hydrofabric_file (layer: flowpath-attributes)
--------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "link", "to", "Length_m", "Y", "n", "nCC", "BtmWdth", "TopWdth", "TopWdthCC", "ChSlp", "alt", "So", "MusX", "MusK", "gage", "gage_nex_id", "WaterbodyID", "waterbody_nex_id", "id", "toid", "vpuid"
   "wb-423670", "nex-423671", "3804.0381267476787", "0.46638980706096966", "0.06", "0.12", "5.91191129054133", "6.865928976757372", "20.597786930272115", "1.0227685851754977", "20.0323429107666", "0.003019662880502428", "0.2", "3600.0", "None", "None", "None", "None", "wb-423670", "nex-423671", "03S"
   "wb-423671", "nex-423663", "2386.6099099488665", "0.5049858162860272", "0.06", "0.12", "6.724094883296428", "7.6995424965830574", "23.098627489749173", "0.9658168426003173", "8.545430183410645", "0.0035805726557105143", "0.2", "3600.0", "02301695", "nex-423663", "None", "None", "wb-423671", "nex-423663", "03S"
   "wb-423752", "nex-423748", "5861.027417139365", "0.4298076586362661", "0.06", "0.12", "5.179553884022866", "6.102819373763817", "18.30845812129145", "1.07404494916444", "38.86513137817383", "0.00356021667742983", "0.2", "3600.0", "None", "None", "None", "None", "wb-423752", "nex-423748", "03S"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - link
     - link
     - object

   * - to
     - to
     - object

   * - Length_m
     - Length_m
     - float64

   * - Y
     - Y
     - float64

   * - n
     - n
     - float64

   * - nCC
     - nCC
     - float64

   * - BtmWdth
     - BtmWdth
     - float64

   * - TopWdth
     - TopWdth
     - float64

   * - TopWdthCC
     - TopWdthCC
     - float64

   * - ChSlp
     - ChSlp
     - float64

   * - alt
     - alt
     - float64

   * - So
     - So
     - float64

   * - MusX
     - MusX
     - float64

   * - MusK
     - MusK
     - float64

   * - gage
     - gage
     - object

   * - gage_nex_id
     - gage_nex_id
     - object

   * - WaterbodyID
     - WaterbodyID
     - object

   * - waterbody_nex_id
     - waterbody_nex_id
     - object

   * - id
     - Identifier.
     - object

   * - toid
     - Identifier of the downstream feature (nexus) to which this catchment drains.
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-network:

ngen_hydrofabric_file (layer: network)
--------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "id", "toid", "divide_id", "ds_id", "mainstem", "hydroseq", "hf_source", "hf_id", "lengthkm", "areasqkm", "tot_drainage_areasqkm", "type", "vpuid", "hf_hydroseq", "hf_lengthkm", "hf_mainstem", "topo", "poi_id", "hl_uri"
   "wb-423666", "tnx-1000002837", "cat-423666", "nan", "2367036.0", "13772.0", "NOAA Reference Fabric", "16918808.0", "4.261507434137776", "7.4394003734988585", "1033.6455015839595", "terminal", "03S", "2367036.0", "7.742660026156029", "2367036.0", "fl-nex", "nan", "None"
   "wb-423787", "tnx-1000002836", "cat-423787", "nan", "2367331.0", "13771.0", "NOAA Reference Fabric", "16927768.0", "0.6257802608509306", "6.075450342000487", "6.075450342000487", "terminal", "03S", "2367331.0", "0.6257802608509306", "2367331.0", "fl-nex", "nan", "None"
   "wb-423786", "tnx-1000002835", "cat-423786", "nan", "2367329.0", "13770.0", "NOAA Reference Fabric", "16924548.0", "1.4300169212241527", "0.6268500720000907", "0.6268500720000907", "terminal", "03S", "2367330.0", "1.0540261556064199", "2367329.0", "fl-nex", "nan", "None"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - id
     - Identifier.
     - object

   * - toid
     - Identifier of the downstream feature (nexus) to which this catchment drains.
     - object

   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - ds_id
     - Drainage system identifier.
     - float64

   * - mainstem
     - mainstem
     - float64

   * - hydroseq
     - hydroseq
     - float64

   * - hf_source
     - hf_source
     - object

   * - hf_id
     - hf_id
     - float64

   * - lengthkm
     - Length in kilometers.
     - float64

   * - areasqkm
     - Area in square kilometers.
     - float64

   * - tot_drainage_areasqkm
     - Total drainage area in square kilometers.
     - float64

   * - type
     - Type of feature (e.g., divide).
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - hf_hydroseq
     - hf_hydroseq
     - float64

   * - hf_lengthkm
     - hf_lengthkm
     - float64

   * - hf_mainstem
     - hf_mainstem
     - float64

   * - topo
     - topo
     - object

   * - poi_id
     - poi_id
     - float64

   * - hl_uri
     - hl_uri
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry



.. _ngen_hydrofabric_file-layer-divide-attributes:

ngen_hydrofabric_file (layer: divide-attributes)
------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/gpkg_vpu/vpu_03S.gpkg``

.. note:: Geometry column omitted from preview table for brevity.

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "mode.bexp_soil_layers_stag=1", "mode.bexp_soil_layers_stag=2", "mode.bexp_soil_layers_stag=3", "mode.bexp_soil_layers_stag=4", "mode.ISLTYP", "mode.IVGTYP", "geom_mean.dksat_soil_layers_stag=1", "geom_mean.dksat_soil_layers_stag=2", "geom_mean.dksat_soil_layers_stag=3", "geom_mean.dksat_soil_layers_stag=4", "geom_mean.psisat_soil_layers_stag=1", "geom_mean.psisat_soil_layers_stag=2", "geom_mean.psisat_soil_layers_stag=3", "geom_mean.psisat_soil_layers_stag=4", "mean.cwpvt", "mean.mfsno", "mean.mp", "mean.refkdt", "mean.slope_1km", "mean.smcmax_soil_layers_stag=1", "mean.smcmax_soil_layers_stag=2", "mean.smcmax_soil_layers_stag=3", "mean.smcmax_soil_layers_stag=4", "mean.smcwlt_soil_layers_stag=1", "mean.smcwlt_soil_layers_stag=2", "mean.smcwlt_soil_layers_stag=3", "mean.smcwlt_soil_layers_stag=4", "mean.vcmx25", "mean.Coeff", "mean.Zmax", "mode.Expon", "centroid_x", "centroid_y", "mean.impervious", "mean.elevation", "mean.slope", "circ_mean.aspect", "dist_4.twi", "vpuid"
   "cat-410946", "5.252414703369141", "5.252414703369141", "5.252414703369141", "5.252414703369141", "1.0", "5.0", "6.713499423963534e-06", "6.713499423963534e-06", "6.713499423963534e-06", "6.713499423963534e-06", "0.03143330993893718", "0.03143330993893718", "0.03143330993893718", "0.03143330993893718", "0.18317580223083496", "2.0", "11.861627578735352", "2.0", "0.008376349695026875", "0.3923191428184509", "0.3923191428184509", "0.3923191428184509", "0.3923191428184509", "0.009999999776482582", "0.009999999776482582", "0.009999999776482582", "0.009999999776482582", "75.72674560546875", "0.005", "33.80711", "4.0", "1271168.7498999485", "812969.9972999999", "1.2767298221588135", "1528.4900147573342", "37.407464278810444", "188.11907603781995", "[{"v":7.057,"frequency":0.2498},{"v":8.667,"frequency":0.2498},{"v":10.31,"frequency":0.2498},{"v":14.02,"frequency":0.2505}]", "03S"
   "cat-410945", "5.300997257232666", "5.300997257232666", "5.300997257232666", "5.300997257232666", "1.0", "5.0", "7.418730759359985e-06", "7.418730759359985e-06", "7.418730759359985e-06", "7.418730759359985e-06", "0.04088344037477461", "0.04088344037477461", "0.04088344037477461", "0.04088344037477461", "0.1488569974899292", "2.0", "10.628262519836426", "2.0", "0.047288767993450165", "0.4021017849445343", "0.4021017849445343", "0.4021017849445343", "0.4021017849445343", "0.010566906072199345", "0.010566906072199345", "0.010566906072199345", "0.010566906072199345", "67.72886657714844", "0.005", "124.8165", "4.0", "1262961.5627226317", "877260.0033", "1.1612335443496704", "3618.5220120426447", "52.55042553740607", "181.15789064647845", "[{"v":6.922,"frequency":0.25},{"v":7.949,"frequency":0.25},{"v":9.4,"frequency":0.25},{"v":14.36,"frequency":0.25}]", "03S"
   "cat-410944", "5.300997257232666", "5.300997257232666", "5.300997257232666", "5.300997257232666", "1.0", "14.0", "4.323843156029169e-06", "4.323843156029169e-06", "4.323843156029169e-06", "4.323843156029169e-06", "0.03824043797599118", "0.03824043797599118", "0.03824043797599118", "0.03824043797599118", "0.09594833105802536", "2.0", "10.341452598571777", "2.0", "0.044040463864803314", "0.41291695833206177", "0.41291695833206177", "0.41291695833206177", "0.41291695833206177", "0.012880989350378513", "0.012880989350378513", "0.012880989350378513", "0.012880989350378513", "67.50013732910156", "0.005", "145.2471", "4.0", "1207820.6248640185", "911324.9988", "0.05170055106282234", "3653.144859219939", "59.09503117725212", "176.54026050148272", "[{"v":7.511,"frequency":0.2502},{"v":8.507,"frequency":0.2498},{"v":9.983,"frequency":0.2498},{"v":15.05,"frequency":0.2502}]", "03S"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - mode.bexp_soil_layers_stag=1
     - mode.bexp_soil_layers_stag=1
     - float64

   * - mode.bexp_soil_layers_stag=2
     - mode.bexp_soil_layers_stag=2
     - float64

   * - mode.bexp_soil_layers_stag=3
     - mode.bexp_soil_layers_stag=3
     - float64

   * - mode.bexp_soil_layers_stag=4
     - mode.bexp_soil_layers_stag=4
     - float64

   * - mode.ISLTYP
     - mode.ISLTYP
     - float64

   * - mode.IVGTYP
     - mode.IVGTYP
     - float64

   * - geom_mean.dksat_soil_layers_stag=1
     - geom_mean.dksat_soil_layers_stag=1
     - float64

   * - geom_mean.dksat_soil_layers_stag=2
     - geom_mean.dksat_soil_layers_stag=2
     - float64

   * - geom_mean.dksat_soil_layers_stag=3
     - geom_mean.dksat_soil_layers_stag=3
     - float64

   * - geom_mean.dksat_soil_layers_stag=4
     - geom_mean.dksat_soil_layers_stag=4
     - float64

   * - geom_mean.psisat_soil_layers_stag=1
     - geom_mean.psisat_soil_layers_stag=1
     - float64

   * - geom_mean.psisat_soil_layers_stag=2
     - geom_mean.psisat_soil_layers_stag=2
     - float64

   * - geom_mean.psisat_soil_layers_stag=3
     - geom_mean.psisat_soil_layers_stag=3
     - float64

   * - geom_mean.psisat_soil_layers_stag=4
     - geom_mean.psisat_soil_layers_stag=4
     - float64

   * - mean.cwpvt
     - mean.cwpvt
     - float64

   * - mean.mfsno
     - mean.mfsno
     - float64

   * - mean.mp
     - mean.mp
     - float64

   * - mean.refkdt
     - mean.refkdt
     - float64

   * - mean.slope_1km
     - mean.slope_1km
     - float64

   * - mean.smcmax_soil_layers_stag=1
     - mean.smcmax_soil_layers_stag=1
     - float64

   * - mean.smcmax_soil_layers_stag=2
     - mean.smcmax_soil_layers_stag=2
     - float64

   * - mean.smcmax_soil_layers_stag=3
     - mean.smcmax_soil_layers_stag=3
     - float64

   * - mean.smcmax_soil_layers_stag=4
     - mean.smcmax_soil_layers_stag=4
     - float64

   * - mean.smcwlt_soil_layers_stag=1
     - mean.smcwlt_soil_layers_stag=1
     - float64

   * - mean.smcwlt_soil_layers_stag=2
     - mean.smcwlt_soil_layers_stag=2
     - float64

   * - mean.smcwlt_soil_layers_stag=3
     - mean.smcwlt_soil_layers_stag=3
     - float64

   * - mean.smcwlt_soil_layers_stag=4
     - mean.smcwlt_soil_layers_stag=4
     - float64

   * - mean.vcmx25
     - mean.vcmx25
     - float64

   * - mean.Coeff
     - mean.Coeff
     - float64

   * - mean.Zmax
     - mean.Zmax
     - float64

   * - mode.Expon
     - mode.Expon
     - float64

   * - centroid_x
     - centroid_x
     - float64

   * - centroid_y
     - centroid_y
     - float64

   * - mean.impervious
     - mean.impervious
     - float64

   * - mean.elevation
     - mean.elevation
     - float64

   * - mean.slope
     - mean.slope
     - float64

   * - circ_mean.aspect
     - circ_mean.aspect
     - float64

   * - dist_4.twi
     - dist_4.twi
     - object

   * - vpuid
     - VPU identifier.
     - object

   * - geometry
     - Catchment geometry in WKT format.
     - geometry




.. _snow_cover_file:

snow_cover_file
---------------

File containing snow cover fraction for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/snow_frac/vpu03S_snow_frac.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "snow_pc_hydroatlas"
   "cat-410946", "0.0"
   "cat-410945", "0.0"
   "cat-410944", "0.0"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - snow_pc_hydroatlas
     - snowcover percentage from HydroATLAS dataset
     - float64




.. _streamcat-attr_data_file:

streamcat.attr_data_file
------------------------

File containing StreamCat attribute data for all catchments in a NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/attr_datasets/streamcat/attr_streamcat_conus.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "BFI", "CanalDens", "DamDens", "DamNIDStor", "DamNrmStor", "Elev", "Perm", "Om", "RckDep", "WtDep", "AgKffact", "Kffact", "PctAlkIntruVol", "PctAlluvCoast", "PctCarbResid", "PctCoastCrs", "PctColluvSed", "PctEolCrs", "PctEolFine", "PctExtruVol", "PctGlacLakeCrs", "PctGlacLakeFine", "PctGlacTilClay", "PctGlacTilCrs", "PctGlacTilLoam", "PctHydric", "PctNonCarbResid", "PctSalLake", "PctSilicic", "PctWater", "Precip", "Tmax", "Tmean", "Tmin", "RdDens", "Runoff", "Clay", "Sand", "Precip_Minus_EVT"
   "cat-1", "50.97614977871673", "0.0", "0.0", "0.0", "0.0", "4.41573220047481", "0.9327959862648094", "0.16721313470521276", "7.124522606720663", "6.410044831293111", "0.0", "0.23598567162637368", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1248.0793687420046", "16.40189576196621", "11.64019762480423", "-5.201682360844988", "0.5468780338934144", "621.0", "0.3689421336222836", "2.8666550631382157", "42.01070572178115"
   "cat-10", "61.0", "0.0", "0.0", "0.0", "0.0", "0.03", "0.0", "0.0", "0.0", "0.0", "0.0", "0.24", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1143.243408205", "15.01485443115", "10.40089797975", "-5.19999980925", "6.3185", "705.0", "0.0", "0.0", "46.0"
   "cat-100", "57.861776267329795", "0.0", "0.12263365999918233", "51110.52451192907", "22255.567108017753", "24.662106685497744", "39.64840113848574", "0.3646600642603927", "148.66528493995057", "164.94400452907053", "0.00958470130740571", "0.15246596463167286", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "99.62427699449351", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1244.2868206418714", "14.698732493942293", "10.213878933060482", "-5.523975540000376", "5.378409398214846", "699.9999999999999", "2.9396928974825243", "78.3037261254769", "50.724319985883874"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - divide_id
     - object

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
   "1", "CanalDens", "Density of NHDPlus line features classified as canal, ditch, or pipeline within the catchment or watershed."
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