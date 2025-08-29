"""Main entry point for Reddit Scout Pro Community Edition on Replit."""

import subprocess
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_requirements():
    """Install required packages on Replit startup."""
    try:
        logger.info("Installing requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_multi_user.txt"
        ])
        logger.info("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        raise

def setup_environment():
    """Set up environment variables and configuration."""
    # Set default environment variables if not present
    if not os.getenv('DATABASE_URL'):
        logger.warning("DATABASE_URL not set - will use SQLite for development")
    
    if not os.getenv('SECRET_KEY'):
        logger.warning("SECRET_KEY not set - generating temporary key")
        os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    if not os.getenv('ENCRYPTION_KEY'):
        logger.warning("ENCRYPTION_KEY not set - will generate on first use")

def main():
    """Main entry point."""
    try:
        # Install requirements (Replit needs this on startup)
        install_requirements()
        
        # Setup environment
        setup_environment()
        
        # Import and run the app (after requirements are installed)
        from app_multi_user import main as app_main
        app_main()
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        print(f"❌ Error starting Reddit Scout Pro: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check that all environment variables are set in Replit Secrets")
        print("2. Ensure PostgreSQL database is enabled in Replit")
        print("3. Check the logs for more details")
        sys.exit(1)

if __name__ == "__main__":
    main()
