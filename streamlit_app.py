#!/usr/bin/env python3
"""
Render-optimized entry point for Reddit Scout Pro MULTI-USER
"""
import os
import sys
from pathlib import Path

# Set environment variables for Render
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'

# Import and run the MULTI-USER app version
from app_multi_user import main

if __name__ == "__main__":
    main()
