"""Database models for Reddit Scout Pro Community Edition."""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class APIKey(Base):
    """API key storage for Reddit authentication per user."""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reddit_client_id = Column(String(255))
    reddit_client_secret_encrypted = Column(Text)  # Encrypted using Fernet
    reddit_user_agent = Column(String(100), default="RedditScoutPro/2.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey(user_id={self.user_id}, client_id='{self.reddit_client_id[:10]}...')>"

class Session(Base):
    """User session management for authentication."""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String(255))  # Optional: track user agent
    ip_address = Column(String(45))   # Optional: track IP address
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<Session(user_id={self.user_id}, expires_at='{self.expires_at}')>"

class UserPreferences(Base):
    """User preferences and settings."""
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Reddit preferences
    default_subreddits = Column(Text)  # JSON string of default subreddits
    max_posts_per_request = Column(Integer, default=100)
    default_time_filter = Column(String(20), default="week")
    
    # Content filtering preferences
    min_score_threshold = Column(Integer, default=5)
    min_comments_threshold = Column(Integer, default=3)
    exclude_nsfw = Column(Boolean, default=True)
    exclude_spoilers = Column(Boolean, default=True)
    
    # UI preferences
    theme = Column(String(20), default="light")
    items_per_page = Column(Integer, default=25)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id})>"
