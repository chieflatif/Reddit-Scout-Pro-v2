"""Database connection and session management for Reddit Scout Pro."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .models import Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()
    
    def _get_database_url(self) -> str:
        """Get database URL from environment variables."""
        # Try standard DATABASE_URL first (Render, Heroku, etc.)
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Fix postgres:// to postgresql:// if needed (Heroku compatibility)
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
                logger.info("Fixed postgres:// to postgresql:// in DATABASE_URL")
            
            logger.info("Using DATABASE_URL from environment")
            return database_url
        
        # Fallback to Replit's individual database environment variables
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'reddit_scout')
        db_user = os.getenv('DB_USER', 'postgres')
        db_pass = os.getenv('DB_PASS', '')
        
        if all([db_host, db_port, db_name, db_user]):
            database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            logger.info("Using individual database environment variables")
            return database_url
        
        # Development fallback to SQLite
        logger.warning("No PostgreSQL configuration found, using SQLite for development")
        return "sqlite:///reddit_scout.db"
    
    def _initialize_database(self):
        """Initialize database connection and create tables."""
        database_url = self._get_database_url()
        
        # Configure engine based on database type
        if database_url.startswith('sqlite'):
            # SQLite configuration for development
            self.engine = create_engine(
                database_url,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 20
                },
                echo=False  # Set to True for SQL debugging
            )
        else:
            # PostgreSQL configuration for production
            try:
                self.engine = create_engine(
                    database_url,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    echo=False  # Set to True for SQL debugging
                )
            except Exception as e:
                if "psycopg2" in str(e).lower():
                    logger.error("PostgreSQL driver (psycopg2) not available. Using SQLite fallback for testing.")
                    # Fallback to SQLite for testing
                    self.engine = create_engine(
                        "sqlite:///reddit_scout_fallback.db",
                        poolclass=StaticPool,
                        connect_args={"check_same_thread": False},
                        echo=False
                    )
                else:
                    raise
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info(f"Database initialized with URL: {database_url.split('@')[0]}@***")
    
    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def close_connection(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

# Global database manager instance
db_manager = DatabaseManager()

def get_db():
    """Dependency to get database session."""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database and create tables."""
    try:
        db_manager.create_tables()
        logger.info("Database initialization completed")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def get_db_session():
    """Get a database session (for direct use)."""
    return db_manager.get_session()

# Health check function
def check_db_health():
    """Check database connectivity."""
    try:
        from sqlalchemy import text
        db = get_db_session()
        # Simple query to test connection
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
