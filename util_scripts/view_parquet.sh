#!/bin/bash
#
# =========================================================
# Parquet Viewer Script using DuckDB
# Supports default preview, custom queries, and full export
# Works with shell redirection
# Usage:
#   ./view_parquet.sh <parquet_file> [NUM_ROWS] [--all] [--no-csv] [-q "<SQL_QUERY>"]
# Examples:
#   # Preview first 50 rows (default)
#   ./view_parquet.sh data.parquet
#
#  # Define file first and then run queries
#  export file='outputs/region/test/pairs/pairs_kmeans_conus_vpu03S.parquet'
#  # Preview first 50 rows (default) and export to preview.csv
#  ./view_parquet.sh $file
#  # Preview first 100 rows with no CSV export
#   ./view_parquet.sh $file 100 --no-csv
#  # Export all rows to CSV
#   ./view_parquet.sh $file --all
#  # Export all rows to a custom CSV file
#   ./view_parquet.sh $file --all -o all_data.csv
#  # Run a custom SQL query (e.g., count rows)
#   ./view_parquet.sh $file -q "SELECT COUNT(*) FROM __FILE__"
#  # Run a custom SQL query with a WHERE clause
#   ./view_parquet.sh $file -q "SELECT * FROM __FILE__ WHERE distSpatial > 500"
#   # Run a custom SQL query with a WHERE clause and no CSV export
#   ./view_parquet.sh $file -q "SELECT * FROM __FILE__ WHERE distSpatial > 200" --no-csv
# =========================================================

FILE=""
NUM_ROWS=50
CUSTOM_QUERY=""
EXPORT_ALL=false
EXPORT_CSV=true   # By default, writes preview.csv
OUTPUT_CSV="preview.csv"

# -----------------------------
# Parse arguments
# -----------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -q|--query)
            CUSTOM_QUERY="$2"
            shift 2
            ;;
        --all)
            EXPORT_ALL=true
            shift
            ;;
        --no-csv)  # optional flag to suppress CSV
            EXPORT_CSV=false
            shift
            ;;
        -o|--output)
            OUTPUT_CSV="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            if [ -z "$FILE" ]; then
                FILE="$1"
            else
                NUM_ROWS="$1"
            fi
            shift
            ;;
    esac
done

# Validate file
if [ -z "$FILE" ]; then
    echo "Usage: $0 <parquet_file> [NUM_ROWS] [--all] [--no-csv] [-q \"<SQL_QUERY>\"]"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' does not exist."
    exit 1
fi

# Prepare query
if [ -n "$CUSTOM_QUERY" ]; then
    # Replace __FILE__ placeholder with quoted file path
    QUERY="${CUSTOM_QUERY//__FILE__/\"$FILE\"}"
else
    if [ "$EXPORT_ALL" = true ]; then
        QUERY="SELECT * FROM \"$FILE\""
    else
        QUERY="SELECT * FROM \"$FILE\" LIMIT $NUM_ROWS"
    fi
fi

# Run query and print to stdout
duckdb -c "$QUERY"


# Optional CSV export
if [ "$EXPORT_CSV" = true ]; then
    echo "Exporting results to $OUTPUT_CSV ..."
    duckdb -c "COPY ($QUERY) TO '$OUTPUT_CSV' WITH (HEADER, DELIMITER ',');"
fi

echo "Done."