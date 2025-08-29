#!/usr/bin/env python3
"""
Bulletproof startup script for Reddit Scout Pro Community Edition.
Handles all potential deployment issues and provides clear error messages.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Ensure Python version is compatible."""
    if sys.version_info < (3, 8):
        logger.error(f"Python {sys.version} is too old. Requires Python 3.8+")
        sys.exit(1)
    logger.info(f"✅ Python {sys.version} is compatible")

def check_environment_variables():
    """Check critical environment variables."""
    required_vars = {
        'DATABASE_URL': 'PostgreSQL database connection string',
        'SECRET_KEY': 'Application secret key for sessions',
        'ENCRYPTION_KEY': 'Encryption key for API keys (optional - will generate)'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            if var == 'ENCRYPTION_KEY':
                logger.warning(f"⚠️ {var} not set - will auto-generate")
            else:
                logger.error(f"❌ {var} not set - {description}")
                missing_vars.append(var)
        else:
            # Don't log actual values for security
            logger.info(f"✅ {var} is set")
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Set these in your deployment platform's environment variables section")
        sys.exit(1)

def check_dependencies():
    """Check that all required packages are installed."""
    required_packages = [
        'streamlit',
        'sqlalchemy', 
        'bcrypt',
        'cryptography',
        'praw',
        'psycopg2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} installed")
        except ImportError:
            logger.error(f"❌ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            logger.info("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

def check_file_structure():
    """Verify all required files and directories exist."""
    required_paths = [
        'app_multi_user.py',
        'src/',
        'src/database/',
        'src/auth/',
        'src/core/',
        'src/ui/',
        'requirements.txt'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            logger.error(f"❌ Missing: {path}")
            missing_paths.append(path)
        else:
            logger.info(f"✅ Found: {path}")
    
    if missing_paths:
        logger.error(f"Missing required files/directories: {', '.join(missing_paths)}")
        logger.error("Ensure the complete project structure is deployed")
        sys.exit(1)

def test_database_connection():
    """Test database connectivity before starting the app."""
    try:
        # Add src to path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from database.database import check_db_health, init_db
        
        logger.info("Testing database connection...")
        if not init_db():
            logger.error("❌ Database initialization failed")
            sys.exit(1)
        
        if not check_db_health():
            logger.error("❌ Database health check failed")
            sys.exit(1)
        
        logger.info("✅ Database connection successful")
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        logger.error("Check your DATABASE_URL and ensure PostgreSQL is running")
        sys.exit(1)

def start_streamlit():
    """Start the Streamlit application with proper configuration."""
    port = os.getenv('PORT', '8501')
    
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app_multi_user.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    logger.info(f"Starting Streamlit on port {port}...")
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Use exec to replace this process with Streamlit
        os.execvp(sys.executable, cmd)
    except Exception as e:
        logger.error(f"❌ Failed to start Streamlit: {e}")
        sys.exit(1)

def main():
    """Main startup sequence."""
    logger.info("🚀 Starting Reddit Scout Pro Community Edition...")
    
    # Run all checks
    check_python_version()
    check_file_structure()
    check_environment_variables()
    check_dependencies()
    test_database_connection()
    
    logger.info("✅ All checks passed! Starting application...")
    
    # Start the application
    start_streamlit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)
