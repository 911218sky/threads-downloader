#!/bin/bash

# Check for venv directory and activate if present
if [ -d "venv" ]; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ./venv
elif ! command -v threads-downloader >/dev/null 2>&1; then
    echo "Neither 'venv' directory nor 'threads-downloader' command found. Exiting."
    read -p "Press Enter to exit."
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