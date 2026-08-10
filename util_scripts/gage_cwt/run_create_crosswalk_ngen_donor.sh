# NHF v1
python create_crosswalk_ngen_donor.py \
  --input-dir ~/data/hydrofabric/gpkg_nhf \
  --outdir ~/run_region/region_input/nhf/cwt_divide_gage \
  --gages-file ~/repos/nwm-region-mgr/data/inputs/region/gages_nwm4_calib_all.csv \
  --nested-gages inner \
  --hf-version nhf

#HF v2.2
# python create_crosswalk_ngen_donor.py \
#   --input-dir ~/repos/nwm-region-mgr/data/inputs/hydrofabric/gpkg_v2.2 \
#   --outdir ~/repos/nwm-region-mgr/data/inputs/cwt_divide_gage \
#   --gages-file ~/repos/nwm-region-mgr/data/inputs/gages_nwm4_calib_all.csv \
#   --nested-gages inner