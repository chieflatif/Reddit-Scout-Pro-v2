# 🛠️ Reddit Scout Pro Community Edition - Implementation Guide

## Quick Start Implementation

### Step 1: Install New Dependencies

```bash
pip install sqlalchemy alembic bcrypt cryptography psycopg2-binary python-jose email-validator streamlit-authenticator
```

### Step 2: Database Models Implementation

```python
# src/database/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
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

class APIKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reddit_client_id = Column(String(255))
    reddit_client_secret_encrypted = Column(Text)  # Encrypted
    reddit_user_agent = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
```

### Step 3: Authentication Manager

```python
# src/auth/auth_manager.py
import bcrypt
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database.models import User, Session as UserSession
from ..database.database import get_db
import streamlit as st

class AuthManager:
    def __init__(self):
        self.db = get_db()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        """Register a new user."""
        db = next(self.db)
        try:
            # Check if user exists
            existing = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing:
                return {"success": False, "message": "Username or email already exists"}
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=self.hash_password(password)
            )
            db.add(user)
            db.commit()
            
            return {"success": True, "message": "Registration successful", "user_id": user.id}
        except Exception as e:
            db.rollback()
            return {"success": False, "message": str(e)}
        finally:
            db.close()
    
    def login_user(self, username: str, password: str) -> dict:
        """Authenticate user and create session."""
        db = next(self.db)
        try:
            # Find user
            user = db.query(User).filter(User.username == username).first()
            
            if not user or not self.verify_password(password, user.password_hash):
                return {"success": False, "message": "Invalid credentials"}
            
            # Create session
            session_token = secrets.token_urlsafe(32)
            session = UserSession(
                user_id=user.id,
                session_token=session_token,
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            db.add(session)
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            return {
                "success": True,
                "user_id": user.id,
                "username": user.username,
                "session_token": session_token
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "message": str(e)}
        finally:
            db.close()
    
    def validate_session(self, session_token: str) -> dict:
        """Validate session token."""
        db = next(self.db)
        try:
            session = db.query(UserSession).filter(
                UserSession.session_token == session_token,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if session:
                return {
                    "valid": True,
                    "user_id": session.user_id,
                    "username": session.user.username
                }
            return {"valid": False}
        finally:
            db.close()
```

### Step 4: API Key Encryption

```python
# src/core/encryption.py
from cryptography.fernet import Fernet
import os
from typing import Optional

class APIKeyEncryption:
    def __init__(self):
        # Get or generate encryption key
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key().decode()
            print(f"Generated new encryption key: {key}")
            print("Add this to your environment variables as ENCRYPTION_KEY")
        
        self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt API key."""
        if not plaintext:
            return ""
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        """Decrypt API key."""
        if not ciphertext:
            return ""
        try:
            return self.cipher.decrypt(ciphertext.encode()).decode()
        except Exception:
            return None
```

### Step 5: Refactored Reddit Scout

```python
# src/core/reddit_scout_multi.py
import praw
from typing import Optional
from ..database.models import APIKey
from ..database.database import get_db
from .encryption import APIKeyEncryption

class UserRedditScout:
    """Reddit Scout with per-user API key support."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.encryption = APIKeyEncryption()
        self.reddit = self._initialize_reddit()
    
    def _get_user_api_keys(self) -> Optional[APIKey]:
        """Get user's API keys from database."""
        db = next(get_db())
        try:
            return db.query(APIKey).filter(APIKey.user_id == self.user_id).first()
        finally:
            db.close()
    
    def _initialize_reddit(self) -> Optional[praw.Reddit]:
        """Initialize Reddit client with user's API keys."""
        api_keys = self._get_user_api_keys()
        
        if not api_keys:
            return None
        
        # Decrypt the secret
        client_secret = self.encryption.decrypt(api_keys.reddit_client_secret_encrypted)
        
        if not client_secret:
            return None
        
        try:
            reddit = praw.Reddit(
                client_id=api_keys.reddit_client_id,
                client_secret=client_secret,
                user_agent=api_keys.reddit_user_agent or "RedditScoutPro/1.0"
            )
            # Test the connection
            reddit.user.me()
            return reddit
        except Exception:
            return None
    
    def update_api_keys(self, client_id: str, client_secret: str, user_agent: str = None) -> bool:
        """Update user's API keys."""
        db = next(get_db())
        try:
            api_keys = db.query(APIKey).filter(APIKey.user_id == self.user_id).first()
            
            if not api_keys:
                api_keys = APIKey(user_id=self.user_id)
                db.add(api_keys)
            
            api_keys.reddit_client_id = client_id
            api_keys.reddit_client_secret_encrypted = self.encryption.encrypt(client_secret)
            api_keys.reddit_user_agent = user_agent or "RedditScoutPro/1.0"
            
            db.commit()
            
            # Reinitialize Reddit client
            self.reddit = self._initialize_reddit()
            return True
        except Exception:
            db.rollback()
            return False
        finally:
            db.close()
    
    # All existing RedditScout methods remain the same...
```

### Step 6: Streamlit UI Updates

```python
# src/ui/pages/login.py
import streamlit as st
from ...auth.auth_manager import AuthManager

def render_login_page():
    st.title("🔐 Login to Reddit Scout Pro")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            auth = AuthManager()
            result = auth.login_user(username, password)
            
            if result["success"]:
                st.session_state.authenticated = True
                st.session_state.user_id = result["user_id"]
                st.session_state.username = result["username"]
                st.session_state.session_token = result["session_token"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(result["message"])
    
    st.markdown("---")
    st.markdown("Don't have an account? [Register here](#register)")
```

```python
# src/ui/pages/api_keys.py
import streamlit as st
from ...core.reddit_scout_multi import UserRedditScout

def render_api_keys_page():
    st.title("🔑 Reddit API Key Management")
    
    if not st.session_state.get("authenticated"):
        st.error("Please login first")
        return
    
    user_id = st.session_state.user_id
    scout = UserRedditScout(user_id)
    
    st.markdown("""
    ### How to get Reddit API Keys:
    1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
    2. Click "Create App" or "Create Another App"
    3. Fill in the form:
       - Name: Any name for your app
       - App type: Select "script"
       - Redirect URI: http://localhost:8080
    4. Click "Create app"
    5. Your Client ID is the string under "personal use script"
    6. Your Client Secret is the "secret" string
    """)
    
    with st.form("api_keys_form"):
        client_id = st.text_input("Reddit Client ID")
        client_secret = st.text_input("Reddit Client Secret", type="password")
        user_agent = st.text_input("User Agent (optional)", value="RedditScoutPro/1.0")
        
        submit = st.form_submit_button("Save API Keys")
        
        if submit:
            if scout.update_api_keys(client_id, client_secret, user_agent):
                st.success("API keys saved successfully!")
                st.session_state.reddit_configured = True
            else:
                st.error("Failed to save API keys")
    
    # Test connection
    if st.button("Test Reddit Connection"):
        if scout.reddit:
            try:
                scout.reddit.user.me()
                st.success("✅ Reddit API connection successful!")
            except:
                st.error("❌ Failed to connect to Reddit API")
        else:
            st.warning("Please configure your API keys first")
```

### Step 7: Main App Update

```python
# app.py
import streamlit as st
from src.auth.auth_manager import AuthManager
from src.ui.pages import login, register, dashboard, api_keys
from src.database.database import init_db

def main():
    # Initialize database
    init_db()
    
    # Page config
    st.set_page_config(
        page_title="Reddit Scout Pro - Community Edition",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check session validity
    if st.session_state.get('session_token'):
        auth = AuthManager()
        session = auth.validate_session(st.session_state.session_token)
        if not session['valid']:
            st.session_state.authenticated = False
            st.session_state.clear()
    
    # Routing
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login.render_login_page()
        with tab2:
            register.render_register_page()
    else:
        # Sidebar navigation for authenticated users
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
        
        page = st.sidebar.selectbox(
            "Navigate to:",
            ["Dashboard", "API Keys", "Settings", "Logout"]
        )
        
        if page == "Dashboard":
            dashboard.render_dashboard()
        elif page == "API Keys":
            api_keys.render_api_keys_page()
        elif page == "Settings":
            settings.render_settings_page()
        elif page == "Logout":
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
```

### Step 8: Render.com Configuration

```yaml
# render.yaml
services:
  - type: web
    name: reddit-scout-community
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: reddit-scout-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ENCRYPTION_KEY
        generateValue: true
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: STREAMLIT_SERVER_ENABLE_CORS
        value: false

databases:
  - name: reddit-scout-db
    plan: free
    databaseName: reddit_scout
    user: reddit_scout_user
```

### Step 9: Docker Configuration (Optional)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 10: Environment Variables

```bash
# .env.example
# Database
DATABASE_URL=postgresql://user:password@localhost/reddit_scout
# Or for SQLite: sqlite:///reddit_scout.db

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Streamlit
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false

# App Settings
MAX_USERS=100
SESSION_TIMEOUT_DAYS=7
```

## 🚀 Deployment Steps for Render.com

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add multi-user support"
git push origin main
```

2. **Create Render Account:**
- Go to [render.com](https://render.com)
- Sign up with GitHub

3. **Deploy:**
- Click "New +"
- Select "Web Service"
- Connect your GitHub repo
- Use the render.yaml configuration
- Deploy!

4. **Configure Database:**
- Render will automatically create the PostgreSQL database
- Run migrations after first deploy

5. **Test:**
- Register a test user
- Add Reddit API keys
- Test functionality

## 🔒 Security Checklist

- [x] Passwords hashed with bcrypt
- [x] API keys encrypted in database
- [x] Session tokens expire
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] Environment variables for secrets
- [x] HTTPS enforced on Render
- [ ] Rate limiting (implement with Redis)
- [ ] 2FA (future enhancement)

## 📊 Database Migration Commands

```bash
# Initialize Alembic
alembic init alembic

# Create first migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🧪 Testing

```python
# tests/test_auth.py
import pytest
from src.auth.auth_manager import AuthManager

def test_password_hashing():
    auth = AuthManager()
    password = "test123"
    hashed = auth.hash_password(password)
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrong", hashed)

def test_user_registration():
    auth = AuthManager()
    result = auth.register_user("testuser", "test@example.com", "password123")
    assert result["success"]
```

## 📝 Next Steps

1. Implement the database models
2. Create authentication system
3. Update UI components
4. Test locally with SQLite
5. Deploy to Render.com
6. Add monitoring and logging

This implementation provides a solid foundation for your community Reddit Scout Pro with secure multi-user support!
