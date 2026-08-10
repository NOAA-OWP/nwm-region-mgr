#!/bin/bash
set -euo pipefail

id_type="gage_id"
version="v1"
domains=("CONUS" "Puerto_Rico" "Hawaii" "Alaska")
gages_file="$HOME/repos/nwm-region-mgr/data/inputs/region/gages_nwm4_calib_all.csv"

for domain in "${domains[@]}"; do
    echo "Processing domain: $domain"

    domain1="${domain// /_}" # replace spaces with underscores for file paths
    dest_dir="$HOME/data/hydrofabric/gpkg_nhf/${domain1}/"
    mkdir -p "$dest_dir"


    # iterate through gages for the current domain
    while read -r gage; do
        dest_file="${dest_dir}/${gage}.gpkg"

        if [[ -f "$dest_file" ]]; then
            echo "File for Gage $gage already exists, skipping."
            continue
        fi
        
        url="http://edfs.test.nextgenwaterprediction.com/api/${version}/hydrofabric/${gage}/gpkg?id_type=${id_type}&source=nhf&domain=${domain1}"

        echo "Downloading GPKG for Gage $gage ... from URL: $url"
        curl -L -o "$dest_file" "$url"
    done < <(
    python - <<EOF

import csv

with open("$gages_file", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["domain"] == "$domain":
            print(row["gage_id"])
EOF
    )

done
