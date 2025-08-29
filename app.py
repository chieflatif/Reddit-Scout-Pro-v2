#!/usr/bin/env python3
"""
Reddit Explorer - Multi-User Auth Gate with per-user Reddit keys
"""

import sys
import os
import streamlit as st

# Ensure src is on path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import init_db
from src.auth.decorators import init_auth_state, logout_user
from src.ui.pages.login import render_auth_page
from src.database.database import get_user_api_keys


def load_user_keys_into_env(user_id: int) -> None:
    """Load the logged-in user's Reddit API keys into environment variables.

    This ensures `src.reddit_scout.RedditScout` reads per-user credentials via
    `src.config.settings` on first import.
    """
    try:
        keys = get_user_api_keys(user_id)
        # Clear prior env to avoid cross-user leakage
        for k in [
            'REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT',
            'REDDIT_USERNAME', 'REDDIT_PASSWORD'
        ]:
            if k in os.environ:
                del os.environ[k]

        if keys:
            if keys.get('client_id'):
                os.environ['REDDIT_CLIENT_ID'] = keys['client_id']
            if keys.get('client_secret'):
                os.environ['REDDIT_CLIENT_SECRET'] = keys['client_secret']
            os.environ['REDDIT_USER_AGENT'] = keys.get('user_agent') or 'RedditScoutPro/1.0'
            if keys.get('reddit_username'):
                os.environ['REDDIT_USERNAME'] = keys['reddit_username']
            if keys.get('reddit_password'):
                os.environ['REDDIT_PASSWORD'] = keys['reddit_password']
    except Exception:
        # Fail-safe: leave env unchanged
        pass


def main():
    # Initialize DB and auth state
    init_db()
    init_auth_state()

    # Not authenticated → show login/register
    if not st.session_state.get('authenticated'):
        render_auth_page()
        return

    # Sidebar: logout
    with st.sidebar:
        st.markdown(f"User: **{st.session_state.get('username','')}**")
        if st.button("Logout"):
            logout_user()
            st.rerun()
        st.markdown("---")

    # Load per-user keys into env before importing dashboard/config
    user_id = st.session_state.get('user_id')
    if user_id:
        load_user_keys_into_env(user_id)

    # Ensure dashboard constructs its own RedditScout
    st.session_state.reddit_scout = None

    # Defer import so `src.config.settings` reads updated env
    from src.dashboard import main as dashboard_main
    dashboard_main()


if __name__ == "__main__":
    main()