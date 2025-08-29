"""Login page for Reddit Scout Pro."""

import streamlit as st
from ...auth.auth_manager import AuthManager
from ...auth.decorators import set_auth_state

def render_login_page():
    """Render the login page."""
    st.title("🔐 Login to Reddit Scout Pro")
    st.markdown("Welcome back! Please sign in to access your personalized Reddit analytics.")
    
    # Create two columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### Sign In")
            
            username = st.text_input(
                "Username or Email",
                placeholder="Enter your username or email",
                help="You can use either your username or email address"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            
            # Remember me option (future enhancement)
            # remember_me = st.checkbox("Remember me for 30 days")
            
            submit_button = st.form_submit_button(
                "Sign In",
                use_container_width=True,
                type="primary"
            )
            
            if submit_button:
                if not username or not password:
                    st.error("Please enter both username/email and password.")
                else:
                    with st.spinner("Signing you in..."):
                        auth = AuthManager()
                        result = auth.login_user(
                            username=username.strip(),
                            password=password,
                            user_agent=st.context.headers.get("User-Agent"),
                            ip_address=st.context.headers.get("X-Forwarded-For")
                        )
                        
                        if result["success"]:
                            # Set authentication state
                            set_auth_state(result)
                            st.success(f"Welcome back, {result['username']}! 🎉")
                            st.balloons()
                            
                            # Small delay to show success message
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
        
        st.markdown("---")
        
        # Additional options
        st.markdown("### Don't have an account?")
        if st.button("Create Account", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()
        
        # Future enhancements
        # st.markdown("### Forgot your password?")
        # if st.button("Reset Password", use_container_width=True):
        #     st.session_state.show_reset = True
        #     st.rerun()

def render_registration_page():
    """Render the registration page."""
    st.title("📝 Create Your Account")
    st.markdown("Join the Reddit Scout Pro community and start exploring Reddit like never before!")
    
    # Create two columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form", clear_on_submit=False):
            st.markdown("### Create Account")
            
            username = st.text_input(
                "Username",
                placeholder="Choose a unique username",
                help="3-50 characters, letters, numbers, and underscores only",
                max_chars=50
            )
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="We'll use this for account recovery and important updates"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                help="At least 8 characters with uppercase, lowercase, and numbers"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )
            
            # Terms acceptance
            accept_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy",
                help="By creating an account, you agree to our community guidelines"
            )
            
            submit_button = st.form_submit_button(
                "Create Account",
                use_container_width=True,
                type="primary"
            )
            
            if submit_button:
                # Validation
                if not all([username, email, password, confirm_password]):
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif not accept_terms:
                    st.error("Please accept the Terms of Service to continue.")
                else:
                    with st.spinner("Creating your account..."):
                        auth = AuthManager()
                        result = auth.register_user(
                            username=username.strip(),
                            email=email.strip(),
                            password=password
                        )
                        
                        if result["success"]:
                            st.success("🎉 Account created successfully!")
                            st.info("You can now sign in with your new account.")
                            
                            # Auto-login the user
                            login_result = auth.login_user(username, password)
                            if login_result["success"]:
                                set_auth_state(login_result)
                                st.balloons()
                                import time
                                time.sleep(2)
                                st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
        
        st.markdown("---")
        
        # Back to login
        st.markdown("### Already have an account?")
        if st.button("Sign In", use_container_width=True):
            st.session_state.show_register = False
            st.rerun()

def render_auth_page():
    """Render the main authentication page (login/register)."""
    # Check if user wants to register
    if st.session_state.get('show_register', False):
        render_registration_page()
    else:
        render_login_page()
    
    # Add some information about the app
    st.markdown("---")
    
    with st.expander("ℹ️ About Reddit Scout Pro", expanded=False):
        st.markdown("""
        **Reddit Scout Pro** is a powerful Reddit analytics and discovery tool that helps you:
        
        - 🔍 **Discover** relevant subreddits for your interests
        - 🔥 **Track** active discussions and trending topics
        - 📊 **Analyze** subreddit metrics and engagement patterns
        - 💭 **Monitor** sentiment across communities
        - 🔎 **Search** across multiple subreddits simultaneously
        - ☁️ **Visualize** popular topics with word clouds
        
        **Your Privacy**: We store only your login credentials and Reddit API keys (encrypted). 
        We never store or analyze your personal Reddit data.
        
        **Getting Started**: After signing in, you'll need to add your Reddit API keys to start exploring.
        Don't worry - we'll guide you through the process!
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Reddit Scout Pro Community Edition</p>", 
        unsafe_allow_html=True
    )
