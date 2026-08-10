.. _output-data:
Schemas
=======

.. _attr_data_final:

attr_data_final
---------------

Final attribute data used for regionalization, based on attribute selection in the configuration. Each attribute is prefixed by its corresponding dataset name.

Sample file path: ``outputs/region/attr_data_final/attr_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "is_donor", "hlr_AQPERMNEW", "hlr_TAVE", "hlr_PPT", "hlr_PET", "hlr_PMPE", "hlr_SAND", "streamcat_BFI", "streamcat_CanalDens", "streamcat_DamDens", "streamcat_DamNIDStor", "streamcat_DamNrmStor", "streamcat_Elev", "streamcat_Perm", "streamcat_Om", "streamcat_RckDep", "streamcat_WtDep", "streamcat_AgKffact", "streamcat_Kffact", "streamcat_PctAlkIntruVol", "streamcat_PctAlluvCoast", "streamcat_PctCarbResid", "streamcat_PctCoastCrs", "streamcat_PctColluvSed", "streamcat_PctEolCrs", "streamcat_PctEolFine", "streamcat_PctExtruVol", "streamcat_PctGlacLakeCrs", "streamcat_PctGlacLakeFine", "streamcat_PctGlacTilClay", "streamcat_PctGlacTilCrs", "streamcat_PctGlacTilLoam", "streamcat_PctHydric", "streamcat_PctNonCarbResid", "streamcat_PctSalLake", "streamcat_PctSilicic", "streamcat_PctWater", "streamcat_Precip", "streamcat_Tmax", "streamcat_Tmean", "streamcat_Tmin", "streamcat_RdDens", "streamcat_Runoff", "streamcat_Clay", "streamcat_Sand", "streamcat_Precip_Minus_EVT"
   "cat-1016462", "True", "1.0", "54.47579956055", "57.95169830322", "27.85939979553", "30.09230041504", "47.9600982666", "61.234730315169315", "0.0", "0.0", "0.0", "0.0", "1587.7367709765883", "9.519517947816217", "2.2046839454643035", "145.31146402586657", "182.88000000000002", "0.0", "0.2424741767948702", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "2034.477416335128", "14.656024201640122", "9.26436413052888", "-4.28366317915664", "0.7612452736729998", "688.7553864291", "12.12719725702732", "50.900356584218635", "117.86036881754052"
   "cat-1016463", "True", "1.0", "54.47579956055", "57.95169830322", "27.85939979553", "30.09230041504", "47.9600982666", "59.99961175401633", "0.0", "0.0", "0.0", "0.0", "1293.2124562083463", "7.514833336969149", "0.8859361491105748", "138.82250870764383", "182.88", "0.0", "0.24920367159082205", "0.0", "0.0", "0.0", "0.0", "100.00000000000001", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1625.3267947426727", "15.977565978138605", "10.13201872256988", "-4.04376468154375", "0.49560771571458906", "682.0000000000001", "16.57660636336356", "45.65598623463524", "87.9793030931872"
   "cat-1016464", "True", "1.0", "54.47579956055", "57.95169830321999", "27.859399795529995", "30.092300415040004", "47.9600982666", "59.5115", "0.0", "0.0", "0.0", "0.0", "1094.4615", "7.27", "0.72", "138.03", "182.88", "0.0", "0.25", "0.0", "0.0", "0.0", "0.0", "100.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "1364.8580513892748", "17.358519982078356", "10.695478851653236", "-4.337621540316755", "0.7705", "681.9999999999999", "17.12", "44.9009", "67.2034"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - is_donor
     - Indicates whether the catchment is a donor (true) or receiver (false).
     - bool

   * - hlr_AQPERMNEW
     - Aquifer permeability
     - float64

   * - hlr_TAVE
     - Mean annual temperature
     - float64

   * - hlr_PPT
     - Mean annual precipitation
     - float64

   * - hlr_PET
     - Mean annual potential evaporatranspiration
     - float64

   * - hlr_PMPE
     - Mean annual precipitation minus PET
     - float64

   * - hlr_SAND
     - Percentage of sand in the soil
     - float64

   * - streamcat_BFI
     - Baseflow is the component of streamflow that can be attributed to ground-water discharge into streams. The Baseflow Index (BFI) is the ratio of baseflow to total flow, expressed as a percentage, within catchment.
     - float64

   * - streamcat_CanalDens
     - Density of NHDPlus line features classified as canal, ditch, or pipeline within the catchment or watershed.
     - float64

   * - streamcat_DamDens
     - Density of georeferenced dams within catchment (dams/ square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - streamcat_DamNIDStor
     - Total possible volume of all reservoirs (NID_STORA in NID) per unit area of catchment (cubic meters/square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - streamcat_DamNrmStor
     - Normal (most common) volume of all reservoirs (NORM_STORA in NID) per unit area of catchment (cubic meters/square km) based on the National Inventory of Dams (https://catalog.data.gov/dataset/national-inventory-of-dams)
     - float64

   * - streamcat_Elev
     - Mean catchment elevation in meters.
     - float64

   * - streamcat_Perm
     - Mean permeability (cm/hour) of soils (STATSGO) within catchment.
     - float64

   * - streamcat_Om
     - Mean organic matter content (% by weight) of soils (STATSGO) within catchment.
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

   * - streamcat_PctAlkIntruVol
     - % of catchment area classified as lithology type: alkaline intrusive volcanic rock
     - float64

   * - streamcat_PctAlluvCoast
     - % of catchment area classified as lithology type: alluvium and fine-textured coastal zone sediment
     - float64

   * - streamcat_PctCarbResid
     - % of catchment area classified as lithology type: carbonate residual material
     - float64

   * - streamcat_PctCoastCrs
     - % of catchment area classified as lithology type: coastal zone sediment, coarse-textured
     - float64

   * - streamcat_PctColluvSed
     - % of catchment area classified as lithology type: colluvial sediment
     - float64

   * - streamcat_PctEolCrs
     - % of catchment area classified as lithology type: eolian sediment, coarse-textured (sand dunes)
     - float64

   * - streamcat_PctEolFine
     - % of catchment area classified as lithology type: eolian sediment, fine-textured (glacial loess)
     - float64

   * - streamcat_PctExtruVol
     - % of catchment area classified as lithology type: extrusive volcanic rock
     - float64

   * - streamcat_PctGlacLakeCrs
     - % of catchment area classified as lithology type: glacial outwash and glacial lake sediment, coarse-textured
     - float64

   * - streamcat_PctGlacLakeFine
     - % of catchment area classified as lithology type: glacial lake sediment, fine-textured
     - float64

   * - streamcat_PctGlacTilClay
     - % of catchment area classified as lithology type: glacial till, clayey
     - float64

   * - streamcat_PctGlacTilCrs
     - % of catchment area classified as lithology type: glacial till, coarse-textured
     - float64

   * - streamcat_PctGlacTilLoam
     - % of catchment area classified as lithology type: glacial till, loamy
     - float64

   * - streamcat_PctHydric
     - % of catchment area classified as lithology type: hydric, peat and muck
     - float64

   * - streamcat_PctNonCarbResid
     - % of catchment area classified as lithology type: non-carbonate residual material
     - float64

   * - streamcat_PctSalLake
     - % of catchment area classified as lithology type: saline like sediment
     - float64

   * - streamcat_PctSilicic
     - % of catchment area classified as lithology type: silicic residual material
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

   * - streamcat_RdDens
     - Density of roads (2010 Census Tiger Lines) within catchment (km/square km)
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

Sample file path: ``outputs/region/formulations/form_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "vpu", "divide_id", "formulation", "huc_id", "total_score", "summary_score", "cost", "num_gages", "upscale_huc"
   "03S", "cat-415628", "noah-owp-modular snow-17 cfe-x t-route", "03070103", "1.82", "0.9305114474915951", "15", "3", "huc8"
   "03S", "cat-415629", "noah-owp-modular snow-17 cfe-x t-route", "03070103", "1.82", "0.9305114474915951", "15", "3", "huc8"
   "03S", "cat-415630", "noah-owp-modular snow-17 cfe-x t-route", "03070103", "1.82", "0.9305114474915951", "15", "3", "huc8"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - vpu
     - Hydrologic VPU the catchment belongs to.
     - object

   * - divide_id
     - Unique identifier for each catchment.
     - object

   * - formulation
     - Formulation assigned to the catchment.
     - object

   * - huc_id
     - HUC ID the catchment belongs to (given the huc level specified in the configuration).
     - object

   * - total_score
     - Total formulation summary score across all calibrated catchments in the HUC region. If "average_score" is chosen in the configuration, this column would be the average score instead.
     - float64

   * - summary_score
     - Highest summary score for the assigned formulation calibrated basins in the HUC region.
     - float64

   * - cost
     - Computational cost associated with the assigned formulation in the HUC region.
     - int64

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

Sample file path: ``outputs/region/formulations/form_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "02314500", "noah-owp-modular lasam t-route", "3.5101328525866955", "0.3404262876739411", "103.32723999542704", "8.541847860650119", "84.86645310088417", "4.685753699776528", "0.804539911248697", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.1212547772261575", "0.5441297948626399", "0.1363046350741823", "1.6388107273647554", "10.308690609074098", "2.0768951334525343", "144.37434845659223", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02208150", "noah-owp-modular snow-17 cfe-x t-route", "3.302211730841977", "0.1530701120368238", "64.50241741064907", "10.35361122481772", "5.207204189742202", "1.5516800131487098", "0.8216748155447595", "9.648070687838704", "0.0006609990923245", "0.1775838251849715", "0.8769159858698881", "0.2349686060115616", "0.2356840976954763", "0.0447582966361027", "0.0017528344687233", "3.70769307361701", "0.5042854276011531", "0.3944502804739151", "2.9132022303304272", "1.519958841718836", "0.0175067702690927", "5754.503459824122", "0.510868734302519", "0.948809627707221", "0.0957871146374974", "0.299815928365687", "0.5438230929426437", "0.0486967003610763", "0.4290860867104877", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0021747040843594", "4.354979613185452", "4.094942483452014", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02228500", "noah-owp-modular lasam t-route", "3.367167254916128", "0.3242573597008308", "39.62515991147947", "4.76285615881014", "13.113738231745913", "1.9876986913464847", "0.8281455190482556", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0273517867947678", "0.6395935886966257", "0.1943972719062101", "1.7708281781042006", "76.11714597774704", "1.5183546697462902", "307.3492392241725", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

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

Sample file path: ``outputs/region/pairs/pairs_kmeans_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "tag", "donor", "distSpatial", "donors", "distSpatials"
   "cat-410687", "main", "cat-412161", "18", "cat-412161,cat-412160,cat-412159", "18,28,28"
   "cat-410688", "main", "cat-412161", "18", "cat-412161,cat-412159,cat-412160", "18,27,28"
   "cat-410689", "main", "cat-412319", "48", "cat-412319,cat-412276,cat-412275", "48,52,54"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
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

Sample file path: ``outputs/region/pairs/pairs_gower_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "divide_id", "tag", "donor", "distSpatial", "donors", "distSpatials", "distAttr", "distAttrs"
   "cat-410687", "proximity", "cat-412161", "18", "cat-412161,cat-503325,cat-412159", "18,25,28", "nan", "None"
   "cat-410688", "proximity", "cat-412161", "18", "cat-412161,cat-412159,cat-412160", "18,27,28", "nan", "None"
   "cat-410689", "main", "cat-412318", "49", "cat-412318,cat-412317,cat-412289", "49,55,55", "0.018", "0.018,0.018,0.029"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - divide_id
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

Sample file path: ``outputs/region/pairs/pairs_kmeans_conus_vpu03S_mswm.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "divide_id"
   "02204130", "cat-417756"
   "02204130", "cat-419726"
   "02204130", "cat-417633"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each donor basin.
     - object

   * - divide_id
     - Unique identifier for each receiver catchment in the VPU.
     - object




.. _params:

params
------

Formulation and calibrated parameters for each donor basin.

Sample file path: ``outputs/region/params/formulation_params_gower_conus_vpu03S.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "02314500", "noah-owp-modular lasam t-route", "3.5101328525866955", "0.3404262876739411", "103.32723999542704", "8.541847860650119", "84.86645310088417", "4.685753699776528", "0.804539911248697", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.1212547772261575", "0.5441297948626399", "0.1363046350741823", "1.6388107273647554", "10.308690609074098", "2.0768951334525343", "144.37434845659223", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02208150", "noah-owp-modular snow-17 cfe-x t-route", "3.302211730841977", "0.1530701120368238", "64.50241741064907", "10.35361122481772", "5.207204189742202", "1.5516800131487098", "0.8216748155447595", "9.648070687838704", "0.0006609990923245", "0.1775838251849715", "0.8769159858698881", "0.2349686060115616", "0.2356840976954763", "0.0447582966361027", "0.0017528344687233", "3.70769307361701", "0.5042854276011531", "0.3944502804739151", "2.9132022303304272", "1.519958841718836", "0.0175067702690927", "5754.503459824122", "0.510868734302519", "0.948809627707221", "0.0957871146374974", "0.299815928365687", "0.5438230929426437", "0.0486967003610763", "0.4290860867104877", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0021747040843594", "4.354979613185452", "4.094942483452014", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "02228500", "noah-owp-modular lasam t-route", "3.367167254916128", "0.3242573597008308", "39.62515991147947", "4.76285615881014", "13.113738231745913", "1.9876986913464847", "0.8281455190482556", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.0273517867947678", "0.6395935886966257", "0.1943972719062101", "1.7708281781042006", "76.11714597774704", "1.5183546697462902", "307.3492392241725", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

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




.. _spatial_distance:

spatial_distance
----------------

Spatial distances between donor and receiver catchments within the VPU. Columns represent donor catchments, and rows represent receiver catchments.

Sample file path: ``outputs/region/spatial_distance/donor_receiver_dist_conus_vpu03S.parquet``

.. warning:: Schema table omitted for spatial_distance files due to large number of columns.



.. _summary_score:

summary_score
-------------

Summary scores for each calibrated formulation and basin.

Sample file path: ``outputs/region/summary_score/score_conus_vpu03S.parquet``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "summary_score"
   "02204130", "noah-owp-modular lasam t-route", "0.8172787119659016"
   "02204130", "noah-owp-modular snow-17 cfe-x t-route", "0.9305114474915951"
   "02204130", "noah-owp-modular ueb cfe-s t-route", "0.5628047288522315"

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