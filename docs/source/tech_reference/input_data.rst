Schemas
=======

general.ngen_hydrofabric_file (layer: divides)
----------------------------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - divide_id
     - object
     - False

   * - toid
     - object
     - False

   * - type
     - object
     - False

   * - ds_id
     - float64
     - True

   * - areasqkm
     - float64
     - False

   * - vpuid
     - object
     - False

   * - id
     - object
     - True

   * - lengthkm
     - float64
     - True

   * - tot_drainage_areasqkm
     - float64
     - True

   * - has_flowline
     - bool
     - False

   * - geometry
     - geometry
     - False




general.gage_divide_cwt_file
----------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - gage_id
     - object
     - False

   * - divide_id
     - object
     - False

   * - toid
     - object
     - False

   * - areasqkm
     - float64
     - False

   * - vpuid
     - object
     - True

   * - type
     - object
     - False




general.donor_gage_file
-----------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - gage_id
     - object
     - False

   * - nws_id
     - object
     - True

   * - agency
     - object
     - False

   * - station_name
     - object
     - True

   * - domain
     - object
     - False

   * - domain_id
     - int64
     - False

   * - nwm_v3_calibration
     - bool
     - False

   * - headwater_calibration
     - bool
     - False

   * - latitude
     - float64
     - True

   * - longitude
     - float64
     - True




general.calval_stats_file
-------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - gage_id
     - object
     - False

   * - formulation
     - object
     - False

   * - evalPeriod
     - object
     - False

   * - bias
     - float64
     - False

   * - rmse
     - float64
     - False

   * - cor
     - float64
     - False

   * - nse
     - float64
     - False

   * - nselog
     - float64
     - False

   * - nseWt
     - float64
     - False

   * - kge
     - float64
     - False

   * - msof
     - float64
     - False

   * - hyperResMultiObj
     - float64
     - False

   * - nnsesq
     - float64
     - False

   * - eventmultiobj
     - float64
     - False

   * - lbem
     - float64
     - False

   * - lbemprime
     - float64
     - False

   * - corr1
     - float64
     - False

   * - pod
     - float64
     - False

   * - far
     - float64
     - False

   * - csi
     - float64
     - False

   * - nnse
     - float64
     - False

   * - peak_bias
     - float64
     - False

   * - peak_tm_err_hr
     - float64
     - False

   * - event_volume_bias
     - float64
     - False




formulation_cost.file
---------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - formulation
     - object
     - False

   * -  cost
     - int64
     - False




attr_datasets.ngen.attr_select_file
-----------------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - select
     - int64
     - False

   * - attr_name
     - object
     - False

   * - description
     - object
     - False




attr_datasets.ngen.attr_data_file
---------------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - divide_id
     - object
     - False

   * - dksat
     - float64
     - True

   * - psisat
     - float64
     - True

   * - smcmax
     - float64
     - False

   * - smcwlt
     - float64
     - False

   * - bexp
     - float64
     - False

   * - ISLTYP
     - float64
     - False

   * - IVGTYP
     - float64
     - False

   * - cwpvt
     - float64
     - False

   * - mfsno
     - float64
     - False

   * - mp
     - float64
     - False

   * - refkdt
     - float64
     - False

   * - slope_1km
     - float64
     - False

   * - vcmx25
     - float64
     - False

   * - Coeff
     - float64
     - True

   * - Zmax
     - float64
     - True

   * - Expon
     - float64
     - True

   * - centroid_x
     - float64
     - False

   * - centroid_y
     - float64
     - False

   * - impervious
     - float64
     - False

   * - elevation
     - float64
     - False

   * - slope
     - float64
     - False

   * - aspect
     - float64
     - False

   * - dist_4.twi
     - object
     - False

   * - vpuid
     - object
     - False




attr_datasets.hlr.attr_select_file
----------------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - select
     - int64
     - False

   * - attr_name
     - object
     - False

   * - description
     - object
     - False




attr_datasets.hlr.attr_data_file
--------------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - divide_id
     - object
     - False

   * - AQPERMNEW
     - float64
     - False

   * - SLOPE
     - float64
     - False

   * - TAVE
     - float64
     - False

   * - PPT
     - float64
     - False

   * - PET
     - float64
     - False

   * - SAND
     - float64
     - False

   * - PMPE
     - float64
     - False

   * - MINELE
     - float64
     - False

   * - RELIEF
     - float64
     - False

   * - PFLATTOT
     - float64
     - False

   * - PFLATLOW
     - float64
     - False

   * - PFLATUP
     - float64
     - False




snow_cover.snow_cover_file
--------------------------

.. list-table::
   :header-rows: 1

   * - Column
     - Type
     - Nullable
   * - divide_id
     - object
     - False

   * - snow_pc_hydroatlas
     - float64
     - True




.. toctree::
   :maxdepth: 2