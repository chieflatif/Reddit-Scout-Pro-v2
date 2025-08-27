#!/usr/bin/env python3
"""
Reddit Explorer - Main Entry Point

Run this script to start the Reddit Explorer dashboard.

Usage:
    python app.py
    or
    streamlit run app.py
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the dashboard
from src.dashboard import main

if __name__ == "__main__":
    main() 