Schemas
=======

.. _attr_data_final:

attr_data_final
---------------

Final attribute data used for regionalization, based on attribute selection in the configuration. Each attribute is prefixed by its corresponding dataset name.

Sample file path: ``outputs/region/test/attr_data_final/attr_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "is_donor", "ngen_area_sqkm", "ngen_elevation_mean", "ngen_slope250m_mean", "ngen_aspect_circmean", "ngen_glacier_percent", "ngen_bexp_mode", "ngen_dksat_geomean", "ngen_psisat_geomean", "ngen_cwpvt_mean", "ngen_mp_mean", "ngen_mfsno_mean", "ngen_quartz_mean", "ngen_refkdt_mean", "ngen_slope1km_mean", "ngen_smcmax_mean", "ngen_smcwlt_mean", "ngen_vcmx_mean", "ngen_cgw", "ngen_expon", "ngen_max_gw_storage", "ngen_imperv_mean", "streamcat_BFI", "streamcat_DamDens", "streamcat_Elev", "streamcat_Perm", "streamcat_RckDep", "streamcat_WtDep", "streamcat_AgKffact", "streamcat_Kffact", "streamcat_PctCarbResid", "streamcat_PctNonCarbResid", "streamcat_PctWater", "streamcat_Precip", "streamcat_Tmax", "streamcat_Tmean", "streamcat_Tmin", "streamcat_Runoff", "streamcat_Clay", "streamcat_Sand", "streamcat_Precip_Minus_EVT"
   "1074100210157824", "True", "20.24730033750234", "5.020439271508947", "0.050928353325520447", "172.92101692389082", "0.0", "4.4523773193359375", "1.4478479897661595e-05", "0.06899999827146534", "0.14919112988133473", "11.784592853553853", "2.0", "0.9200000166893008", "2.0", "0.010160143808876183", "0.4043118836827545", "0.00999999977648258", "43.64731831779272", "0.00499999988824129", "3.9253879051716494", "0.06470147436680382", "0.16334463421591597", "32.0", "0.0", "4.5478", "25.250000000000004", "149.8", "23.88", "0.0", "0.1", "83.96000000000001", "0.0", "0.0", "1378.2362236479592", "28.84888893791454", "22.977240365975767", "10.56380756533801", "347.0", "7.05", "87.22", "19.4876"
   "1074100266143509", "True", "78.22304914951064", "7.055796156358193", "0.04167822450070077", "192.4173795558176", "0.0", "4.4523773193359375", "1.4478479897661595e-05", "0.06899999827146529", "0.155594989657402", "11.646737281362407", "2.0", "0.9200000166893008", "2.0", "0.010782891968241698", "0.40411582589149475", "0.009999999776482582", "47.60119198625999", "0.004999999888241291", "3.9863010478722907", "0.06679029803763824", "0.08909301754866751", "31.634", "0.0", "7.7015", "25.25", "149.8", "23.88", "0.0083", "0.1", "0.2", "0.0", "0.0", "1366.8317469048638", "28.86652985321995", "22.855665871942897", "10.000218427780162", "347.0", "7.05", "87.22", "19.2913"
   "1074100268056066", "True", "12.953250648004571", "6.241271202318929", "0.038436133457750876", "189.08256717289498", "0.0", "4.4523773193359375", "1.4478479897661595e-05", "0.06899999827146532", "0.15559498965740204", "11.710038185119627", "2.0", "0.9200000166893006", "2.0", "0.010782891968241696", "0.4041158258914948", "0.009999999776482582", "41.95553671434628", "0.00499999988824129", "3.8740487875770593", "0.06568874706210683", "0.10135902554998757", "32.0427", "0.0", "6.6057999999999995", "25.25", "149.8", "23.88", "0.0", "0.1", "82.52", "0.0", "0.0", "1355.4270608590857", "28.87487424670741", "22.99455195325816", "10.272436855642592", "347.0", "7.050000000000001", "87.22", "17.9823"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each catchment.
     - string

   * - is_donor
     - Indicates whether the catchment is a donor (true) or receiver (false).
     - bool

   * - ngen_area_sqkm
     - Area of the catchment in square kilometers
     - float64

   * - ngen_elevation_mean
     - Mean elevation of the catchment
     - float64

   * - ngen_slope250m_mean
     - Mean slope of the catchment at 250m resolution
     - float64

   * - ngen_aspect_circmean
     - Aspect of the catchment in circular mean
     - float64

   * - ngen_glacier_percent
     - Percentage of the catchment covered by glaciers
     - float64

   * - ngen_bexp_mode
     - Mode of the beta exponent on Clapp-Hornberger (1978) soil water relations
     - float64

   * - ngen_dksat_geomean
     - Geometric mean of saturated hydraulic conductivity
     - float64

   * - ngen_psisat_geomean
     - Geometric mean of saturated capillary head
     - float64

   * - ngen_cwpvt_mean
     - Mean canopy wind parameter for canopy wind profile formulation
     - float64

   * - ngen_mp_mean
     - Mean slope of Ball-Berry conductance relationship
     - float64

   * - ngen_mfsno_mean
     - Mean melt factor for snow depletion curve
     - float64

   * - ngen_quartz_mean
     - Mean quartz content of the soil
     - float64

   * - ngen_refkdt_mean
     - Mean soil infiltration parameter
     - float64

   * - ngen_slope1km_mean
     - Mean slope of the catchment at 1km resolution
     - float64

   * - ngen_smcmax_mean
     - Mean saturated soil moisture content
     - float64

   * - ngen_smcwlt_mean
     - Mean wilting point soil moisture content
     - float64

   * - ngen_vcmx_mean
     - Mean maximum carboxylation at 25 degC
     - float64

   * - ngen_cgw
     - Coefficient controlling the drainage out of the soil bottom (0=no-flow)
     - float64

   * - ngen_expon
     - Exponent for nonlinear ground water reservoir (1.0 for linear reservoir)
     - float64

   * - ngen_max_gw_storage
     - Maximum storage in the conceptual ground water reservoir
     - float64

   * - ngen_imperv_mean
     - Mean percentage of impervious area
     - float64

   * - streamcat_BFI
     - Baseflow is the component of streamflow that can be attributed to ground-water discharge into streams. The Baseflow Index (BFI) is the ratio of baseflow to total flow, expressed as a percentage, within catchment.
     - float64

   * - streamcat_DamDens
     - Density of georeferenced dams within catchment (dams/ square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - streamcat_Elev
     - Mean catchment elevation in meters.
     - float64

   * - streamcat_Perm
     - Mean permeability (cm/hour) of soils (STATSGO) within catchment.
     - float64

   * - streamcat_RckDep
     - Mean depth (cm) to bedrock of soils (STATSGO) within catchment.
     - float64

   * - streamcat_WtDep
     - Mean seasonal water table depth (cm) of soils (STATSGO) within catchment.
     - float64

   * - streamcat_AgKffact
     - Mean soil erodibility (Kf) factor (unitless) of soils within catchment on agricultural land. The Kf factor is used in the Universal Soil Loss Equation (USLE) and represents a relative index of susceptibility of bare, cultivated soil to particle detachment and transport by rainfall.
     - float64

   * - streamcat_Kffact
     - Mean soil erodibility (Kf) factor (unitless) of soils within catchment. The Kf factor is used in the Universal Soil Loss Equation (USLE) and represents a relative index of susceptibility of bare, cultivated soil to particle detachment and transport by rainfall.
     - float64

   * - streamcat_PctCarbResid
     - % of catchment area classified as lithology type: carbonate residual material
     - float64

   * - streamcat_PctNonCarbResid
     - % of catchment area classified as lithology type: non-carbonate residual material
     - float64

   * - streamcat_PctWater
     - % of catchment area classified as lithology type: water
     - float64

   * - streamcat_Precip
     - PRISM climate data - 30-year normal mean precipitation (mm): Annual period: 1981-2010 within catchment
     - float64

   * - streamcat_Tmax
     - PRISM climate data - 30-year normal maximum temperature (Â°C): Annual period: 1981-2010 within catchment
     - float64

   * - streamcat_Tmean
     - PRISM climate data - 30-year normal mean temperature (Â°C): Annual period: 1981-2010 within the catchment
     - float64

   * - streamcat_Tmin
     - PRISM climate data - 30-year normal minimum temperature (Â°C): Annual period: 1981-2010 within catchment
     - float64

   * - streamcat_Runoff
     - Mean runoff (mm) within catchment
     - float64

   * - streamcat_Clay
     - Mean % clay content of soils (STATSGO) within catchment.
     - float64

   * - streamcat_Sand
     - Mean % sand content of soils (STATSGO) within catchment.
     - float64

   * - streamcat_Precip_Minus_EVT
     - This dataset represents surplus precipitation (mm): precipitation minus potential evaporation described in DOI: 10.1016/j.scitotenv.2020.137661 within individual,  local NHDPlusV2 catchments and upstream, contributing watersheds.
     - float64




.. _formulations:

formulations
------------

Formulations selected for each catchment from formulation regionalization.

Sample file path: ``outputs/region/test/formulations/form_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "vpu", "div_id", "formulation", "huc_id", "average_score", "summary_score", "cost", "num_gages", "upscale_huc"
   "03S", "1271188450740293", "noah-owp-modular ueb cfe-s smp sft t-route", "03070103", "0.804790125940259", "0.804790125940259", "None", "3", "huc8"
   "03S", "1271188467006295", "noah-owp-modular ueb cfe-s smp sft t-route", "03070103", "0.804790125940259", "0.804790125940259", "None", "3", "huc8"
   "03S", "1271189672895076", "noah-owp-modular ueb cfe-s smp sft t-route", "03070103", "0.804790125940259", "0.804790125940259", "None", "3", "huc8"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - vpu
     - Hydrologic VPU the catchment belongs to.
     - object

   * - div_id
     - Unique identifier for each catchment.
     - string

   * - formulation
     - Formulation assigned to the catchment.
     - object

   * - huc_id
     - HUC ID the catchment belongs to (given the huc level specified in the configuration).
     - object

   * - average_score
     - average_score
     - float64

   * - summary_score
     - Highest summary score for the assigned formulation calibrated basins in the HUC region.
     - float64

   * - cost
     - Computational cost associated with the assigned formulation in the HUC region.
     - object

   * - num_gages
     - Number of calibrated basins using the assigned formulation in the HUC region.
     - int64

   * - upscale_huc
     - HUC level used for upscaling in order to find sufficient number of calibrated basins in the HUC region. If same as the HUC level defined in the configuration, then no upscaling was performed.
     - object




.. _formulations_pars:

formulations_pars
-----------------

Formulations selected for each catchment from formulation regionalization.

Sample file path: ``outputs/region/test/formulations/form_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "calibration_run_id", "validation_run_id", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "02216180", "noah-owp-modular lasam t-route", "96238", "53303", "1.449569578948323", "0.164207594424006", "47.01652132743059", "7.337431193205311", "45.6603354954644", "3.3852757306824355", "0.8620794050971368", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0882979562129701", "0.4285296502213604", "0.162326318541275", "2.992162535953276", "44.40302103261308", "1.0127676448876892", "487.1728361088875", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02314500", "noah-owp-modular ueb cfe-s smp sft t-route", "88591", "80712", "1.1325899771720942", "0.3050381541331196", "44.96433920899859", "6.700948175356739", "43.21754378633932", "5.666193523098661", "0.8836436461002298", "9.841014919134896", "0.0004752459531049", "0.3259986215337735", "0.3287783350496248", "0.2424021325179127", "0.1294704192930534", "0.1903773911813904", "0.000315847996914", "1.0286695847053466", "0.711895430547453", "0.0292708176802384", "3.5165720023979383", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "4.543191925283374", "0.2494196031410354", "0.1200504307212102", "3.710661501583241", "0.5752800932656159", "0.9892993201070314", "2.115022608296266", "0.0063527715210404", "106.99245558555344", "1142.5080069501605", "1.3193811960679946", "0.3430321122963723", "0.9240509177196808", "100339.3662896397", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02321000", "noah-owp-modular lasam t-route", "72245", "22061", "2.588923871809641", "0.3570326160631324", "88.2976789453302", "4.916485113930023", "24.665098758431288", "2.1993202670785763", "0.9209599825667656", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0814888628651469", "0.5683632880298866", "0.1457649445299749", "2.7350358513641218", "76.93400451382719", "2.6014852261146744", "241.39833908885825", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - gage_id
     - object

   * - formulation
     - Formulation assigned to the catchment.
     - object

   * - calibration_run_id
     - calibration_run_id
     - int64

   * - validation_run_id
     - validation_run_id
     - int64

   * - MFSNO
     - MFSNO
     - float64

   * - CWP
     - CWP
     - float64

   * - VCMX25
     - VCMX25
     - float64

   * - MP
     - MP
     - float64

   * - RSURF_SNOW
     - RSURF_SNOW
     - float64

   * - RSURF_EXP
     - RSURF_EXP
     - float64

   * - SCAMAX
     - SCAMAX
     - float64

   * - b
     - b
     - float64

   * - satdk
     - satdk
     - float64

   * - satpsi
     - satpsi
     - float64

   * - slope
     - slope
     - float64

   * - maxsmc
     - maxsmc
     - float64

   * - wltsmc
     - wltsmc
     - float64

   * - max_gw_storage
     - max_gw_storage
     - float64

   * - Cgw
     - Cgw
     - float64

   * - expon
     - expon
     - float64

   * - Kn
     - Kn
     - float64

   * - Klf
     - Klf
     - float64

   * - refkdt
     - refkdt
     - float64

   * - mfmax
     - mfmax
     - float64

   * - uadj
     - uadj
     - float64

   * - si
     - si
     - float64

   * - mfmin
     - mfmin
     - float64

   * - scf
     - scf
     - float64

   * - nmf
     - nmf
     - float64

   * - tipm
     - tipm
     - float64

   * - pxtemp
     - pxtemp
     - float64

   * - plwhc
     - plwhc
     - float64

   * - daygm
     - daygm
     - float64

   * - smcmin
     - smcmin
     - float64

   * - smcmax
     - smcmax
     - float64

   * - van_genuchten_alpha
     - van_genuchten_alpha
     - float64

   * - van_genuchten_n
     - van_genuchten_n
     - float64

   * - hydraulic_conductivity
     - hydraulic_conductivity
     - float64

   * - ponded_depth_max
     - ponded_depth_max
     - float64

   * - field_capacity
     - field_capacity
     - float64

   * - df
     - df
     - float64

   * - cc
     - cc
     - float64

   * - hcan
     - hcan
     - float64

   * - lai
     - lai
     - float64

   * - subalb
     - subalb
     - float64

   * - ems
     - ems
     - float64

   * - cg
     - cg
     - float64

   * - zo
     - zo
     - float64

   * - rho
     - rho
     - float64

   * - rhog
     - rhog
     - float64

   * - Ks
     - Ks
     - float64

   * - de
     - de
     - float64

   * - avo
     - avo
     - float64

   * - apr
     - apr
     - float64

   * - a_Xinanjiang_inflection_point_parameter
     - a_Xinanjiang_inflection_point_parameter
     - float64

   * - b_Xinanjiang_shape_parameter
     - b_Xinanjiang_shape_parameter
     - float64

   * - x_Xinanjiang_shape_parameter
     - x_Xinanjiang_shape_parameter
     - float64

   * - uztwm
     - uztwm
     - float64

   * - uzfwm
     - uzfwm
     - float64

   * - lztwm
     - lztwm
     - float64

   * - lzfsm
     - lzfsm
     - float64

   * - lzfpm
     - lzfpm
     - float64

   * - adimp
     - adimp
     - float64

   * - uzk
     - uzk
     - float64

   * - lzpk
     - lzpk
     - float64

   * - lzsk
     - lzsk
     - float64

   * - zperc
     - zperc
     - float64

   * - rexp
     - rexp
     - float64

   * - pctim
     - pctim
     - float64

   * - pfree
     - pfree
     - float64

   * - riva
     - riva
     - float64

   * - side
     - side
     - float64




.. _pairs_cluster_algorithms:

pairs_cluster_algorithms
------------------------

Receiver-donor pairs generated from parameter regionalization using clustering-based algorithms (currently KMeans, KMedoids, HDBSCAN, and BIRCH). Attribute distances are not calculated for these algorithms.

Sample file path: ``outputs/region/test/pairs/pairs_kmeans_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "tag", "donor", "distSpatial", "donors", "distSpatials"
   "1072639236903480", "main", "1074646019530148", "393", "1074646019530148,1270210323434343,1270210349671160", "393,638,641"
   "1072639243699931", "main", "1074646019530148", "393", "1074646019530148", "393"
   "1072639267016356", "main", "1074646019530148", "391", "1074646019530148", "391"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each receiver catchment.  
     - object

   * - tag
     - Identifier indicating whether the donor is found using all selected attributes during the "main" run or using basic attributes during the "basic" run.
     - object

   * - donor
     - Unique identifier for each donor catchment.
     - object

   * - distSpatial
     - Spatial distance between the receiver and donor catchments (in kilometers).
     - int64

   * - donors
     - The final set of donors considered for the receiver catchment. The number of final donors is determined by the "n_donor_max" parameter specified in the configuration.
     - object

   * - distSpatials
     - Spatial distances corresponding to the final set of donors (in kilometers).
     - object




.. _pairs_distance_algorithms:

pairs_distance_algorithms
-------------------------

Receiver-donor pairs generated from parameter regionalization using distance-based algorithms (currently Gower and URF). 

Sample file path: ``outputs/region/test/pairs/pairs_gower_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "div_id", "tag", "donor", "distSpatial", "donors", "distSpatials", "distAttr", "distAttrs"
   "1072639236903480", "main", "1074646017687319", "391", "1074646017687319,1074646019530148,1074620126761110", "391,393,397", "0.098", "0.098,0.07,0.097"
   "1072639243699931", "main", "1074646017687319", "392", "1074646017687319,1074644787668201,1074644581103738", "392,392,395", "0.076", "0.076,0.077,0.081"
   "1072639267016356", "main", "1074646017687319", "389", "1074646017687319,1074644787668201,1074644581103738", "389,390,393", "0.076", "0.076,0.076,0.08"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - div_id
     - Unique identifier for each receiver catchment.  
     - object

   * - tag
     - Identifier indicating whether the donor is found using all selected attributes during the "main" run or using basic attributes during the "basic" run.
     - object

   * - donor
     - Unique identifier for each donor catchment.
     - object

   * - distSpatial
     - Spatial distance between the receiver and donor catchments (in kilometers).
     - int64

   * - donors
     - The final set of donors considered for the receiver catchment. The number of final donors is determined by the "n_donor_max" parameter specified in the configuration.
     - object

   * - distSpatials
     - Spatial distances corresponding to the final set of donors (in kilometers).
     - object

   * - distAttr
     - Attribute distance between the receiver and donor catchments (unitless).
     - float64

   * - distAttrs
     - Attribute distances corresponding to the final set of donors (unitless).
     - object




.. _pairs_mswm:

pairs_mswm
----------

Receiver-donor pairs generated from parameter regionalization to be used by MSWM.

Sample file path: ``outputs/region/test/pairs/pairs_kmeans_conus_vpu03S_mswm.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "div_id"
   "02204130", "1270722761765509"
   "02204130", "1270720284062617"
   "02204130", "1270720286076263"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each donor basin.
     - object

   * - div_id
     - Unique identifier for each receiver catchment in the VPU.
     - int64




.. _params:

params
------

Formulation and calibrated parameters for each donor basin.

Sample file path: ``outputs/region/test/params/formulation_params_kmeans_conus_vpu03S.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "calibration_run_id", "validation_run_id", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "02418760", "noah-owp-modular lasam t-route", "87047", "64087", "3.3259953587437594", "0.267237405479078", "25.095078744337528", "9.924152873914972", "11.844002617531284", "3.703894840320293", "0.7092745859760993", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.1164208248787974", "0.3875411718430442", "0.0052213416668847", "1.255381126414214", "57.08059904345664", "0.5933512594541368", "271.74458091143015", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02361000", "noah-owp-modular lasam t-route", "88399", "62797", "1.185222985859238", "0.2998390535466202", "68.58398198517835", "11.325266784087388", "4.963195549310472", "1.2136957290869923", "0.7183911792975753", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.1374381401049788", "0.3444166119202376", "0.2877229013589725", "2.13134034735349", "76.65264731971207", "2.1584872945634057", "133.8472366173122", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02327100", "noah-owp-modular lasam t-route", "91176", "11929", "3.79004333980786", "0.254276697190028", "40.15436097151438", "4.49508109249586", "41.740596648531735", "1.086010058809768", "0.8559430344165491", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0287898726148542", "0.3807174973809346", "0.2040935272201232", "2.882401314333724", "83.82046866015068", "1.3033211409669754", "300.5137976264068", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - gage_id
     - object

   * - formulation
     - Formulation assigned to the calibration basin. Modules within the formulation are separated by commas.
     - object

   * - calibration_run_id
     - calibration_run_id
     - int64

   * - validation_run_id
     - validation_run_id
     - int64

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




.. _spatial_distance:

spatial_distance
----------------

Spatial distances between donor and receiver catchments within the VPU. Columns represent donor catchments, and rows represent receiver catchments.

Sample file path: ``outputs/region/test/spatial_distance/donor_receiver_dist_conus_vpu03S.parquet``

.. warning:: Schema table omitted for spatial_distance files due to large number of columns.



.. _summary_score:

summary_score
-------------

Summary scores for each calibrated formulation and basin.

Sample file path: ``outputs/region/test/summary_score/score_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "summary_score"
   "02204130", "noah-owp-modular lasam t-route", "0.7157593162362361"
   "02204130", "noah-owp-modular snow-17 cfe-x smp sft t-route", "0.7767337722121507"
   "02204130", "noah-owp-modular ueb cfe-s smp sft t-route", "0.6668881187748419"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each calibration basin.
     - object

   * - formulation
     - Formulation calibrated for each calibration basin.
     - object

   * - summary_score
     - Summary score for the calibrated formulation and basin.
     - float64




.. toctree::
   :maxdepth: 2