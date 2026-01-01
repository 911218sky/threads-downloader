#!/bin/bash

echo "========================================"
echo "  Threads Downloader - Setup Script"
echo "========================================"
echo

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "[!] Conda is not installed."
    echo
    read -p "Would you like to install Miniconda? (y/n): " INSTALL_CONDA
    
    if [[ "$INSTALL_CONDA" =~ ^[Yy]$ ]]; then
        echo
        echo "Downloading Miniconda installer..."
        
        # Detect OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if [[ $(uname -m) == "arm64" ]]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
            else
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
            fi
        else
            # Linux
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        fi
        
        curl -fsSL "$MINICONDA_URL" -o miniconda_installer.sh
        
        if [ -f "miniconda_installer.sh" ]; then
            echo "Installing Miniconda..."
            bash miniconda_installer.sh -b -p "$HOME/miniconda3"
            rm miniconda_installer.sh
            
            # Initialize conda
            eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
            conda init bash
            
            echo
            echo "[OK] Miniconda installed successfully!"
            echo "[!] Please restart your terminal and run this script again."
            exit 0
        else
            echo "[ERROR] Failed to download Miniconda installer."
            exit 1
        fi
    else
        echo
        echo "Setup cancelled. Please install Conda manually:"
        echo "  https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
fi

echo "[OK] Conda found: $(conda --version)"
echo

# Initialize conda for this script
eval "$(conda shell.bash hook)"

# Check if venv exists
if [ -d "venv" ]; then
    echo "[OK] Virtual environment found."
    read -p "Recreate virtual environment? (y/n): " RECREATE
    if [[ "$RECREATE" =~ ^[Yy]$ ]]; then
        echo "Removing existing venv..."
        rm -rf venv
    else
        echo
        echo "Activating virtual environment..."
        conda activate ./venv
        
        echo "Updating dependencies..."
        pip install -r requirements.txt
        pip install -e .
        
        echo
        echo "========================================"
        echo "  Setup completed successfully!"
        echo "========================================"
        exit 0
    fi
fi

# Create virtual environment
echo
echo "Creating virtual environment with Python 3.12..."
conda create -p venv python=3.12 -y
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
conda activate ./venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi

# Install package in editable mode
echo
echo "Installing package in editable mode..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install package."
    exit 1
fi

echo
echo "========================================"
echo "  Setup completed successfully!"
echo "========================================"
echo
echo "To start using Threads Downloader:"
echo "  1. Run: conda activate ./venv"
echo "  2. Run: threads-downloader --help"
echo
echo "Or simply run: ./start.sh"
