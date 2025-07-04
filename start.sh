#!/bin/bash

# Initialize conda for shell usage
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ./venv

urls=()

while true; do
    read -p "Enter Threads profile URL (press Enter to finish): " url
    if [ -z "$url" ]; then
        break
    fi
    urls+=("$url")
done

# Run the threads-downloader command with all collected URLs
threads-downloader --profile "${urls[@]}"

echo "Download completed. Press Enter to exit."
read