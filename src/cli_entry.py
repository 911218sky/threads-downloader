#!/usr/bin/env python
"""Entry point for CLI executable."""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threads_downloader.cli import main

if __name__ == "__main__":
    main()
