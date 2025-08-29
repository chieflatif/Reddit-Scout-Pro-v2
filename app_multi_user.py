"""Multi-user Reddit Scout Pro application."""

import streamlit as st
import logging
import os
from src.database.database import init_db, check_db_health
from src.auth.decorators import init_auth_state, check_session_validity, clear_auth_state, logout_user
from src.ui.pages.login import render_auth_page
from src.ui.pages.api_keys import render_api_keys_page
from src.core.encryption import test_encryption_system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Reddit Scout Pro - Community Edition",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/reddit-scout-pro/issues',
            'Report a bug': 'https://github.com/yourusername/reddit-scout-pro/issues',
            'About': """
            # Reddit Scout Pro - Community Edition
            
            A powerful multi-user Reddit analytics platform.
            
            **Features:**
            - Multi-user authentication
            - Personal Reddit API key management
            - Comprehensive Reddit analytics
            - Sentiment analysis and trending topics
            
            Built with ❤️ for the community.
            """
        }
    )

def initialize_app():
    """Initialize the application."""
    # Initialize database
    if not init_db():
        st.error("❌ Database initialization failed. Please check your configuration.")
        st.stop()
    
    # Test encryption system
    if not test_encryption_system():
        st.error("❌ Encryption system test failed. Please check your ENCRYPTION_KEY.")
        st.stop()
    
    # Initialize authentication state
    init_auth_state()
    
    logger.info("Application initialized successfully")

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("🔍 Reddit Scout Pro")
        st.markdown("*Community Edition*")
        
        if st.session_state.get('authenticated'):
            # Authenticated user sidebar
            user = st.session_state.get('username', 'User')
            st.markdown(f"👋 Welcome, **{user}**!")
            
            # Check if Reddit is configured
            reddit_scout = st.session_state.get('reddit_scout')
            if reddit_scout and reddit_scout.is_configured():
                st.success("✅ Reddit API Ready")
            else:
                st.warning("⚠️ Configure Reddit API")
            
            st.markdown("---")
            
            # Navigation menu
            pages = [
                "🏠 Dashboard",
                "🔑 API Keys",
                "🔍 Subreddit Finder", 
                "🔥 Active Discussions",
                "📈 Trending Analysis",
                "🆕 Latest Posts",
                "📊 Analytics",
                "💭 Sentiment Analysis",
                "🔎 Search",
                "☁️ Word Cloud",
                "⚙️ Settings"
            ]
            
            selected_page = st.selectbox(
                "Navigate to:",
                pages,
                key="navigation"
            )
            
            st.markdown("---")
            
            # Account management
            st.markdown("### Account")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Settings", use_container_width=True):
                    st.session_state.page_redirect = "Settings"
                    st.rerun()
            
            with col2:
                if st.button("🚪 Logout", use_container_width=True):
                    logout_user()
                    st.rerun()
            
            return selected_page
        else:
            # Unauthenticated user sidebar
            st.markdown("### Welcome!")
            st.info("Please sign in to access Reddit Scout Pro features.")
            
            # App information
            with st.expander("ℹ️ About", expanded=True):
                st.markdown("""
                **Reddit Scout Pro** helps you:
                - 🔍 Discover subreddits
                - 📊 Analyze engagement
                - 💭 Track sentiment
                - 🔥 Find trending topics
                
                Sign up to get started!
                """)
            
            return None

def render_main_content(page):
    """Render main content based on selected page."""
    if not st.session_state.get('authenticated'):
        render_auth_page()
        return
    
    # Handle page redirects
    if st.session_state.get('page_redirect'):
        page = st.session_state.page_redirect
        del st.session_state.page_redirect
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "🔑 API Keys":
        render_api_keys_page()
    elif page == "🔍 Subreddit Finder":
        render_subreddit_finder()
    elif page == "🔥 Active Discussions":
        render_active_discussions()
    elif page == "📈 Trending Analysis":
        render_trending_analysis()
    elif page == "🆕 Latest Posts":
        render_latest_posts()
    elif page == "📊 Analytics":
        render_analytics()
    elif page == "💭 Sentiment Analysis":
        render_sentiment_analysis()
    elif page == "🔎 Search":
        render_search()
    elif page == "☁️ Word Cloud":
        render_word_cloud()
    elif page == "⚙️ Settings":
        render_settings()
    else:
        render_dashboard()

def render_dashboard():
    """Render the main dashboard."""
    st.title("🏠 Dashboard")
    st.markdown("Welcome to your Reddit Scout Pro dashboard!")
    
    # Check if Reddit API is configured
    reddit_scout = st.session_state.get('reddit_scout')
    if not reddit_scout or not reddit_scout.is_configured():
        st.warning("⚠️ Please configure your Reddit API keys to start exploring.")
        if st.button("Configure API Keys", type="primary"):
            st.session_state.page_redirect = "🔑 API Keys"
            st.rerun()
        return
    
    # Dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 User", st.session_state.get('username'))
    
    with col2:
        st.metric("🔑 API Status", "✅ Configured")
    
    with col3:
        st.metric("🚀 Ready to Explore", "Yes!")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Find Subreddits", use_container_width=True):
            st.session_state.page_redirect = "🔍 Subreddit Finder"
            st.rerun()
    
    with col2:
        if st.button("🔥 Active Discussions", use_container_width=True):
            st.session_state.page_redirect = "🔥 Active Discussions"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page_redirect = "📊 Analytics"
            st.rerun()
    
    # Recent activity placeholder
    st.markdown("### 📈 Recent Activity")
    st.info("🚧 Coming soon: Your recent searches and favorite subreddits will appear here.")

# Placeholder functions for other pages (to be implemented)
def render_subreddit_finder():
    st.title("🔍 Subreddit Finder")
    st.info("🚧 Coming soon: Advanced subreddit discovery features.")

def render_active_discussions():
    st.title("🔥 Active Discussions")
    st.info("🚧 Coming soon: Real-time discussion tracking.")

def render_trending_analysis():
    st.title("📈 Trending Analysis")
    st.info("🚧 Coming soon: Trending topic analysis.")

def render_latest_posts():
    st.title("🆕 Latest Posts")
    st.info("🚧 Coming soon: Latest posts from your favorite subreddits.")

def render_analytics():
    st.title("📊 Analytics")
    st.info("🚧 Coming soon: Comprehensive subreddit analytics.")

def render_sentiment_analysis():
    st.title("💭 Sentiment Analysis")
    st.info("🚧 Coming soon: Community sentiment tracking.")

def render_search():
    st.title("🔎 Search")
    st.info("🚧 Coming soon: Multi-subreddit search capabilities.")

def render_word_cloud():
    st.title("☁️ Word Cloud")
    st.info("🚧 Coming soon: Visual word cloud generation.")

def render_settings():
    st.title("⚙️ Settings")
    st.info("🚧 Coming soon: User preferences and account settings.")

def main():
    """Main application entry point."""
    try:
        # Setup page configuration
        setup_page_config()
        
        # Initialize application
        initialize_app()
        
        # Check session validity for authenticated users
        if st.session_state.get('authenticated'):
            if not check_session_validity():
                st.warning("Your session has expired. Please log in again.")
                clear_auth_state()
                st.rerun()
        
        # Render sidebar and get selected page
        selected_page = render_sidebar()
        
        # Render main content
        render_main_content(selected_page)
        
        # Health check in footer (for development)
        debug_mode = os.getenv("DEBUG", "false").lower() == "true"
        if debug_mode:
            with st.expander("🔧 System Status", expanded=False):
                db_healthy = check_db_health()
                st.write(f"Database: {'✅ Healthy' if db_healthy else '❌ Error'}")
                st.write(f"Encryption: {'✅ Working' if test_encryption_system() else '❌ Error'}")
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("❌ An unexpected error occurred. Please refresh the page.")
        if debug_mode:
            st.exception(e)

if __name__ == "__main__":
    main()
