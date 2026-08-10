#!/bin/bash

vpus=("01" "02" "03W" "03S" "03N" "04" "05" "06" "07" "08" "09" "10L" "10U" "11" "12" "13" "14" "15" "16" "17" "18")
echo "Subsetting CONUS geopackage by VPU..."
echo "Requires mounting hydrofabric-data S3 bucket to ~/s3/hydrofabric-data: s3fs hydrofabric-data ~/s3/hydrofabric-data"

# loop through vpus and create subset geopackages
for vpu in "${vpus[@]}"; do
    python subset_conus_gpkg_by_vpu.py --vpu $vpu
done


