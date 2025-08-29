"""API Keys management page for Reddit Scout Pro."""

import streamlit as st
from ...auth.decorators import require_auth, get_current_user
from ...core.reddit_scout_multi import UserRedditScout

@require_auth
def render_api_keys_page():
    """Render the API keys management page."""
    st.title("🔑 Reddit API Keys")
    st.markdown("Configure your Reddit API credentials to start exploring Reddit data.")
    
    user = get_current_user()
    if not user:
        st.error("Authentication error. Please log in again.")
        return
    
    # Get current Reddit Scout instance
    reddit_scout = st.session_state.get('reddit_scout')
    if not reddit_scout:
        reddit_scout = UserRedditScout(user['user_id'])
        st.session_state.reddit_scout = reddit_scout
    
    # Check current configuration status
    is_configured = reddit_scout.is_configured()
    
    if is_configured:
        st.success("✅ Reddit API keys are configured and working!")
    else:
        st.warning("⚠️ Reddit API keys are not configured. Please add them below.")
    
    # Instructions section
    with st.expander("📖 How to get Reddit API Keys", expanded=not is_configured):
        st.markdown("""
        ### Step-by-Step Guide:
        
        1. **Go to Reddit Apps**: Visit [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
        
        2. **Create a New App**:
           - Click "Create App" or "Create Another App"
           - Choose a name for your app (e.g., "My Reddit Scout")
           - Select **"script"** as the app type
           - Add a description (optional)
           - Set redirect URI to: `http://localhost:8080`
        
        3. **Get Your Credentials**:
           - **Client ID**: The string under "personal use script" (shorter string)
           - **Client Secret**: The "secret" string (longer string)
        
        4. **Important Notes**:
           - Keep your credentials secure and never share them
           - These keys are encrypted and stored safely in our database
           - You can update them anytime if needed
        """)
        
        st.image("https://i.imgur.com/yNlEkWP.png", caption="Example of Reddit app creation", width=600)
    
    # API Keys form
    st.markdown("### Configure Your API Keys")
    
    with st.form("api_keys_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input(
                "Reddit Client ID",
                placeholder="Enter your Reddit Client ID",
                help="The shorter string under 'personal use script'",
                type="password"
            )
        
        with col2:
            user_agent = st.text_input(
                "User Agent (Optional)",
                value="RedditScoutPro/2.0",
                help="Identifies your app to Reddit's API"
            )
        
        client_secret = st.text_input(
            "Reddit Client Secret",
            placeholder="Enter your Reddit Client Secret",
            help="The longer 'secret' string from your Reddit app",
            type="password"
        )
        
        submit_button = st.form_submit_button(
            "Save & Test API Keys",
            use_container_width=True,
            type="primary"
        )
        
        if submit_button:
            if not client_id or not client_secret:
                st.error("Please provide both Client ID and Client Secret.")
            else:
                with st.spinner("Testing and saving your API keys..."):
                    result = reddit_scout.update_api_keys(
                        client_id=client_id.strip(),
                        client_secret=client_secret.strip(),
                        user_agent=user_agent.strip() if user_agent else None
                    )
                    
                    if result["success"]:
                        st.success("🎉 API keys saved and validated successfully!")
                        st.balloons()
                        
                        # Update session state
                        st.session_state.reddit_scout = reddit_scout
                        
                        # Show next steps
                        st.info("🚀 You're all set! You can now explore Reddit data using the navigation menu.")
                        
                        # Auto-redirect to dashboard after a delay
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
                        st.markdown("""
                        **Common Issues:**
                        - Double-check your Client ID and Secret
                        - Make sure you selected "script" as app type
                        - Verify the app is active in your Reddit preferences
                        """)
    
    # Test connection section
    if is_configured:
        st.markdown("### Test Connection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test Reddit Connection", use_container_width=True):
                with st.spinner("Testing connection..."):
                    try:
                        # Test with a simple API call
                        test_subreddit = reddit_scout.get_subreddit_info("python")
                        if test_subreddit:
                            st.success("✅ Connection test successful!")
                            st.json({
                                "subreddit": test_subreddit["name"],
                                "subscribers": test_subreddit["subscribers"],
                                "title": test_subreddit["title"]
                            })
                        else:
                            st.error("❌ Connection test failed")
                    except Exception as e:
                        st.error(f"❌ Connection test failed: {str(e)}")
        
        with col2:
            if st.button("🗑️ Remove API Keys", use_container_width=True):
                st.session_state.confirm_delete = True
        
        # Confirmation dialog for deletion
        if st.session_state.get('confirm_delete', False):
            st.warning("⚠️ Are you sure you want to remove your API keys?")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Yes, Remove", type="primary"):
                    # Clear API keys
                    result = reddit_scout.update_api_keys("", "", "")
                    st.session_state.reddit_scout = UserRedditScout(user['user_id'])
                    st.session_state.confirm_delete = False
                    st.success("API keys removed successfully.")
                    st.rerun()
            
            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False
                    st.rerun()
    
    # Security information
    st.markdown("---")
    with st.expander("🔒 Security & Privacy Information"):
        st.markdown("""
        ### How We Protect Your API Keys:
        
        - **Encryption**: Your Client Secret is encrypted using industry-standard AES encryption
        - **Secure Storage**: Keys are stored in an encrypted database
        - **No Logging**: We never log or display your actual API keys
        - **Local Processing**: All Reddit data analysis happens in real-time, nothing is permanently stored
        
        ### What We Don't Store:
        - Your Reddit posts or comments
        - Your browsing history
        - Personal Reddit data
        - API responses (except for temporary caching)
        
        ### Your Rights:
        - You can update or remove your API keys anytime
        - You can delete your account and all associated data
        - You maintain full control over your Reddit API access
        """)
    
    # Quick start section
    if is_configured:
        st.markdown("---")
        st.markdown("### 🚀 Quick Start")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Explore Subreddits", use_container_width=True):
                st.session_state.page_redirect = "Subreddit Finder"
                st.rerun()
        
        with col2:
            if st.button("🔥 Active Discussions", use_container_width=True):
                st.session_state.page_redirect = "Active Discussions"
                st.rerun()
        
        with col3:
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.page_redirect = "Subreddit Analytics"
                st.rerun()
