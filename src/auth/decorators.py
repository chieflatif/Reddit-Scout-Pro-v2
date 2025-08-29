"""Authentication decorators and utilities for Streamlit."""

import streamlit as st
from functools import wraps
from typing import Callable, Any
from .auth_manager import AuthManager

def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication for Streamlit functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("🔒 Please log in to access this feature.")
            st.stop()
        
        # Validate session if token exists
        if st.session_state.get('session_token'):
            auth = AuthManager()
            session = auth.validate_session(st.session_state.session_token)
            
            if not session['valid']:
                # Session expired, clear state
                clear_auth_state()
                st.error("🕐 Your session has expired. Please log in again.")
                st.rerun()
        
        return func(*args, **kwargs)
    return wrapper

def init_auth_state():
    """Initialize authentication state in Streamlit session."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'email' not in st.session_state:
        st.session_state.email = None
    
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    
    if 'reddit_scout' not in st.session_state:
        st.session_state.reddit_scout = None

def set_auth_state(user_data: dict):
    """Set authentication state from login response."""
    st.session_state.authenticated = True
    st.session_state.user_id = user_data.get('user_id')
    st.session_state.username = user_data.get('username')
    st.session_state.email = user_data.get('email')
    st.session_state.session_token = user_data.get('session_token')
    
    # Initialize Reddit Scout for this user
    from ..core.reddit_scout_multi import UserRedditScout
    st.session_state.reddit_scout = UserRedditScout(user_data.get('user_id'))

def clear_auth_state():
    """Clear authentication state."""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.session_token = None
    st.session_state.reddit_scout = None
    
    # Clear any other user-specific session data
    keys_to_clear = [key for key in st.session_state.keys() 
                    if key.startswith('user_') or key.startswith('reddit_')]
    for key in keys_to_clear:
        del st.session_state[key]

def check_session_validity():
    """Check if current session is still valid."""
    if not st.session_state.get('session_token'):
        return False
    
    auth = AuthManager()
    session = auth.validate_session(st.session_state.session_token)
    
    if not session['valid']:
        clear_auth_state()
        return False
    
    return True

def logout_user():
    """Logout current user."""
    if st.session_state.get('session_token'):
        auth = AuthManager()
        auth.logout_user(st.session_state.session_token)
    
    clear_auth_state()

def get_current_user():
    """Get current authenticated user info."""
    if not st.session_state.get('authenticated'):
        return None
    
    return {
        'user_id': st.session_state.get('user_id'),
        'username': st.session_state.get('username'),
        'email': st.session_state.get('email')
    }

def require_reddit_config(func: Callable) -> Callable:
    """Decorator to require Reddit API configuration."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated'):
            st.error("🔒 Please log in first.")
            st.stop()
        
        reddit_scout = st.session_state.get('reddit_scout')
        if not reddit_scout or not reddit_scout.is_configured():
            st.warning("⚙️ Please configure your Reddit API keys first.")
            if st.button("Go to API Keys Setup"):
                st.session_state.page_redirect = "API Keys"
                st.rerun()
            st.stop()
        
        return func(*args, **kwargs)
    return wrapper
