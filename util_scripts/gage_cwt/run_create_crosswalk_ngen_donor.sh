# NHF 1.2.0
python create_crosswalk_ngen_donor.py \
  --domains ak \
  --input-dir ~/data/hydrofabric/gpkg_nhf_1.2.0 \
  --outdir ~/data/region_input/nhf_1.2.0/cwt_divide_gage \
  --gages-file ~/repos/nwm-region-mgr/data/inputs/region/gages_nwm4_calib_all.csv \
  --nested-gages inner \
  --hf-version nhf
