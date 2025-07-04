#!/bin/bash

# Check for venv directory and activate if present
if [ -d "venv" ]; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ./venv
else
    echo "No venv directory found. Exiting."
    exit 1
fi

urls=()

while true; do
    read -p "Enter Threads profile URL (press Enter to finish): " url
    if [ -z "$url" ]; then
        break
    fi
    urls+=("$url")
done

threads-downloader --profile "${urls[@]}"

echo "Download completed. Press Enter to exit."
read