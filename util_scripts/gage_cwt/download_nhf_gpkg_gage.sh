# Download NHF GPKG files for specified gages
# If arguments are provided: use them as gage IDs.
# If no arguments are provided: fall back to reading gages_nwm4_calib_all.csv.

#!/bin/bash
set -euo pipefail

id_type="gage_id"
version_api="v1"
version_nhf="1.2.0"

domains=("CONUS" "Puerto_Rico" "Hawaii" "Alaska")
gages_file="$HOME/repos/nwm-region-mgr/data/inputs/region/gages_nwm4_calib_all.csv"

# Optional gage IDs passed on command line
cli_gages=("$@")

for domain in "${domains[@]}"; do
    echo "Processing domain: $domain"

    domain1="${domain// /_}" # replace spaces with underscores for file paths
    dest_dir="$HOME/data/hydrofabric/gpkg_nhf_${version_nhf}/${domain1}/"
    mkdir -p "$dest_dir"


    # If gages supplied on command line, use them.
    if [[ ${#cli_gages[@]} -gt 0 ]]; then
        gages=("${cli_gages[@]}")
    else
        # Read gages from CSV for this domain
        mapfile -t gages < <(
            python - <<EOF
import csv

with open("${gages_file}", newline="") as fp:
    reader = csv.DictReader(fp)

    for row in reader:
        domain = row.get("domain", "").replace(" ", "_")
        if domain == "${domain1}":
            print(row["gage_id"])
EOF
    )
    fi

    for gage in "${gages[@]}"; do
        dest_file="${dest_dir}/${gage}.gpkg"

        if [[ -f "$dest_file" ]]; then
            echo "File for Gage $gage already exists, skipping."
            continue
        fi

        url="http://edfs.test.nextgenwaterprediction.com/api/${version_api}/hydrofabric/${gage}/gpkg?id_type=${id_type}&source=nhf&domain=${domain1}"

        echo "Downloading GPKG for Gage $gage ... from URL: $url"
        curl -L -o "$dest_file" "$url"
    done

done
