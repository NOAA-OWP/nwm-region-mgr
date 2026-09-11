# Download NHF GPKG files for VPUs

#!/bin/bash
set -euo pipefail

id_type="vpu_id"
version_api="v1"
version_nhf="1.2.2"

domains=("CONUS" "Puerto_Rico" "Hawaii" "Alaska")

for domain in "${domains[@]}"; do
    echo "Processing domain: $domain"

    domain1="${domain// /_}" # replace spaces with underscores for file paths
    dest_dir="$HOME/data/hydrofabric/gpkg_nhf_${version_nhf}"
    mkdir -p "$dest_dir"


    if [[ "$domain" == "CONUS" ]]; then
        vpus=("01" "02" "03N" "03S" "03W" "04" "05" "06" "07" "08" "09" "10L" "10U" "11" "12" "13" "14" "15" "16" "17" "18")
    elif [[ "$domain" == "Puerto_Rico" ]]; then
        vpus=("21")
    elif [[ "$domain" == "Hawaii" ]]; then
        vpus=("20")
    elif [[ "$domain" == "Alaska" ]]; then
        vpus=("19")
    else
        echo "Unknown domain: $domain"
        exit 1
    fi  

    for vpu in "${vpus[@]}"; do
        dest_file="${dest_dir}/vpu_${vpu}.gpkg"

        if [[ -f "$dest_file" ]]; then
            echo "File for VPU $vpu already exists, skipping."
            continue
        fi

        url="http://edfs.test.nextgenwaterprediction.com/api/${version_api}/hydrofabric/${vpu}/gpkg?id_type=${id_type}&source=nhf&domain=${domain1}"

        echo "Downloading GPKG for VPU $vpu ... from URL: $url"
        curl -L -o "$dest_file" "$url"
    done

done
