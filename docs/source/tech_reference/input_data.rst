Schemas
=======

.. _general-ngen_hydrofabric_file-layer-flowpaths:

general.ngen_hydrofabric_file (layer: flowpaths)
------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-divides:

general.ngen_hydrofabric_file (layer: divides)
----------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-lakes:

general.ngen_hydrofabric_file (layer: lakes)
--------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-nexus:

general.ngen_hydrofabric_file (layer: nexus)
--------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-pois:

general.ngen_hydrofabric_file (layer: pois)
-------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-hydrolocations:

general.ngen_hydrofabric_file (layer: hydrolocations)
-----------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-flowpath-attributes:

general.ngen_hydrofabric_file (layer: flowpath-attributes)
----------------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-network:

general.ngen_hydrofabric_file (layer: network)
----------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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



.. _general-ngen_hydrofabric_file-layer-divide-attributes:

general.ngen_hydrofabric_file (layer: divide-attributes)
--------------------------------------------------------

NGEN Hydrofabric Catchment Divides for a VPU. Only the divides layer is used during regionalization.

Sample file path: ``inputs/region/hydrofabric/vpu_divides/vpu_03S.gpkg``

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




.. _general-gage_divide_cwt_file:

general.gage_divide_cwt_file
----------------------------

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




.. _general-donor_gage_file:

general.donor_gage_file
-----------------------

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




.. _general-calval_stats_file:

general.calval_stats_file
-------------------------

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




.. _general-calib_param_file:

general.calib_param_file
------------------------

Calibrated parameters for various modules for all gages in an NWM domain (e.g., CONUS).

Sample file path: ``inputs/region/pseudo_calib_params/sampled_params_conus.csv``

**Example rows:**

.. csv-table::
   :header-rows: 1

   "gage_id", "formulation", "MFSNO", "CWP", "VCMX25", "MP", "RSURF_SNOW", "RSURF_EXP", "SCAMAX", "b", "satdk", "satpsi", "slope", "maxsmc", "wltsmc", "max_gw_storage", "Cgw", "expon", "Kn", "Klf", "refkdt", "mfmax", "uadj", "si", "mfmin", "scf", "nmf", "tipm", "pxtemp", "plwhc", "daygm", "smcmin", "smcmax", "van_genuchten_alpha", "van_genuchten_n", "hydraulic_conductivity", "ponded_depth_max", "field_capacity", "df", "cc", "hcan", "lai", "subalb", "ems", "cg", "zo", "rho", "rhog", "Ks", "de", "avo", "apr", "a_Xinanjiang_inflection_point_parameter", "b_Xinanjiang_shape_parameter", "x_Xinanjiang_shape_parameter", "uztwm", "uzfwm", "lztwm", "lzfsm", "lzfpm", "adimp", "uzk", "lzpk", "lzsk", "zperc", "rexp", "pctim", "pfree", "riva", "side"
   "1010000", "noah-owp-modular cfe-s t-route", "2.5681848800643285", "0.3286171733536613", "98.26779571658672", "12.345915915145532", "34.57680991125569", "4.064091503042371", "0.9712745199335464", "3.7414847994010367", "0.0009141315202519", "0.2682757844834037", "0.7532535832349109", "0.4130823012978584", "0.2589183149092599", "0.1352373803701926", "0.0004228761310245", "1.1540687515916113", "0.3326644885346328", "0.8494590266511353", "3.7047342427645367", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "1010000", "noah-owp-modular snow-17 lasam t-route", "1.7202166366984653", "0.2830454483663369", "55.7216447075499", "7.395125941680879", "64.91094869284314", "4.532964185028021", "0.839432321093368", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "0.2549536985740628", "0.1149808945005032", "3395.942668181262", "0.0402573508525195", "1.3993208237988155", "0.1860697866529445", "0.4344457454145048", "2.8034892811290693", "0.1682210213074931", "0.0212834071116516", "0.1391684172778563", "0.7052654753641924", "0.1892796609353877", "1.8393994158286835", "0.8245934418227354", "2.6163411478418066", "85.65653278592669", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"
   "1010000", "noah-owp-modular ueb cfe-x t-route", "1.6984225027876014", "0.1138073585146865", "44.18211099270653", "10.7458769168222", "41.55877300879165", "2.6584257451986466", "0.9894877010479544", "6.451208746356487", "0.0009931305806678", "0.4331962074757012", "0.2281443013468404", "0.2915759136119435", "0.1545028069618073", "0.1101811687158985", "0.00173408132033", "4.603211031471964", "0.9632723151253538", "0.1889839116526389", "0.1175267001634975", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "1.451971818772199", "0.2253714587504531", "2.6267503130197287", "1.0381689683179314", "0.2723324489894099", "0.9878101435547773", "2.104278810378881", "0.0096068438949711", "346.4354100199481", "1291.644609708449", "6.939487504771504", "0.3945507373583731", "0.8990968927991766", "83059.92094090296", "-0.4349516338584633", "2.974069284705172", "4.643406523991181", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan"

**Schema:**

.. list-table::
   :header-rows: 1

   * - Column
     - Description
     - Type
   * - gage_id
     - Unique identifier for each calibration gage.
     - int64

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




.. _general-divide_huc12_cwt_file:

general.divide_huc12_cwt_file
-----------------------------

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




.. _attr_datasets-ngen-attr_select_file:

attr_datasets.ngen.attr_select_file
-----------------------------------

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
     - select
     - int64

   * - attr_name
     - attr_name
     - object

   * - description
     - description
     - object




.. _attr_datasets-ngen-attr_data_file:

attr_datasets.ngen.attr_data_file
---------------------------------

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




.. _attr_datasets-hlr-attr_select_file:

attr_datasets.hlr.attr_select_file
----------------------------------

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
     - select
     - int64

   * - attr_name
     - attr_name
     - object

   * - description
     - description
     - object




.. _attr_datasets-hlr-attr_data_file:

attr_datasets.hlr.attr_data_file
--------------------------------

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
     - AQPERMNEW
     - float64

   * - SLOPE
     - SLOPE
     - float64

   * - TAVE
     - TAVE
     - float64

   * - PPT
     - PPT
     - float64

   * - PET
     - PET
     - float64

   * - SAND
     - SAND
     - float64

   * - PMPE
     - PMPE
     - float64

   * - MINELE
     - MINELE
     - float64

   * - RELIEF
     - RELIEF
     - float64

   * - PFLATTOT
     - PFLATTOT
     - float64

   * - PFLATLOW
     - PFLATLOW
     - float64

   * - PFLATUP
     - PFLATUP
     - float64




.. _attr_datasets-streamcat-attr_select_file:

attr_datasets.streamcat.attr_select_file
----------------------------------------

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
     - select
     - int64

   * - attr_name
     - attr_name
     - object

   * - description
     - description
     - object




.. _attr_datasets-streamcat-attr_data_file:

attr_datasets.streamcat.attr_data_file
--------------------------------------

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
     - BFI
     - float64

   * - CanalDens
     - CanalDens
     - float64

   * - DamDens
     - DamDens
     - float64

   * - DamNIDStor
     - DamNIDStor
     - float64

   * - DamNrmStor
     - DamNrmStor
     - float64

   * - Elev
     - Elev
     - float64

   * - Perm
     - Perm
     - float64

   * - Om
     - Om
     - float64

   * - RckDep
     - RckDep
     - float64

   * - WtDep
     - WtDep
     - float64

   * - AgKffact
     - AgKffact
     - float64

   * - Kffact
     - Kffact
     - float64

   * - PctAlkIntruVol
     - PctAlkIntruVol
     - float64

   * - PctAlluvCoast
     - PctAlluvCoast
     - float64

   * - PctCarbResid
     - PctCarbResid
     - float64

   * - PctCoastCrs
     - PctCoastCrs
     - float64

   * - PctColluvSed
     - PctColluvSed
     - float64

   * - PctEolCrs
     - PctEolCrs
     - float64

   * - PctEolFine
     - PctEolFine
     - float64

   * - PctExtruVol
     - PctExtruVol
     - float64

   * - PctGlacLakeCrs
     - PctGlacLakeCrs
     - float64

   * - PctGlacLakeFine
     - PctGlacLakeFine
     - float64

   * - PctGlacTilClay
     - PctGlacTilClay
     - float64

   * - PctGlacTilCrs
     - PctGlacTilCrs
     - float64

   * - PctGlacTilLoam
     - PctGlacTilLoam
     - float64

   * - PctHydric
     - PctHydric
     - float64

   * - PctNonCarbResid
     - PctNonCarbResid
     - float64

   * - PctSalLake
     - PctSalLake
     - float64

   * - PctSilicic
     - PctSilicic
     - float64

   * - PctWater
     - PctWater
     - float64

   * - Precip
     - Precip
     - float64

   * - Tmax
     - Tmax
     - float64

   * - Tmean
     - Tmean
     - float64

   * - Tmin
     - Tmin
     - float64

   * - RdDens
     - RdDens
     - float64

   * - Runoff
     - Runoff
     - float64

   * - Clay
     - Clay
     - float64

   * - Sand
     - Sand
     - float64

   * - Precip_Minus_EVT
     - Precip_Minus_EVT
     - float64




.. _snow_cover-snow_cover_file:

snow_cover.snow_cover_file
--------------------------

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




.. _formulation_cost-file:

formulation_cost.file
---------------------

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
     - formulation
     - object

   * -  cost
     -  cost
     - int64




.. toctree::
   :maxdepth: 2