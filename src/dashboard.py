"""Reddit Explorer Dashboard - Streamlit interface for comprehensive Reddit analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List
import time

from .reddit_scout import RedditScout
from .config import settings


class RedditDashboard:
    """Streamlit dashboard for Reddit Explorer."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.scout = None
        self._setup_page_config()
        
    def _setup_page_config(self):
        """Setup Streamlit page configuration."""
        st.set_page_config(
            page_title="🔍 Reddit Explorer",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def run(self):
        """Run the main dashboard."""
        self._setup_sidebar()
        self._initialize_scout()
        self._main_content()
    
    def _setup_sidebar(self):
        """Setup the sidebar navigation."""
        st.sidebar.title("🔍 Reddit Explorer")
        st.sidebar.markdown("---")
        
        # Navigation
        self.page = st.sidebar.selectbox(
            "Navigate to:",
            [
                "🏠 Home",
                "🔍 Subreddit Finder",
                "🔥 Active Discussions", 
                "📈 Trending Discussions",
                "🆕 New Discussions",
                "📊 Subreddit Analytics",
                "💭 Sentiment Analysis",
                "🔎 Keyword Search",
                "🌐 Global Search",
                "☁️ Word Cloud",
                "⚙️ Settings"
            ]
        )
        
        st.sidebar.markdown("---")
        
        # Quick subreddit access
        st.sidebar.subheader("Quick Access")
        default_subs = settings.default_subreddits
        
        selected_sub = st.sidebar.selectbox(
            "Popular Subreddits:",
            [""] + default_subs,
            key="quick_subreddit"
        )
        
        if selected_sub and st.sidebar.button("Go to Active Discussions"):
            st.session_state.target_subreddit = selected_sub
            st.session_state.page_override = "🔥 Active Discussions"
            st.rerun()
    
    def _initialize_scout(self):
        """Initialize Reddit Scout with caching."""
        if 'reddit_scout' not in st.session_state:
            with st.spinner("Initializing Reddit API connection..."):
                try:
                    st.session_state.reddit_scout = RedditScout()
                    st.success("✅ Reddit API connected successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to connect to Reddit API: {e}")
                    st.stop()
        
        self.scout = st.session_state.reddit_scout
    
    def _main_content(self):
        """Render main content based on selected page."""
        # Handle page override from sidebar
        page = getattr(st.session_state, 'page_override', self.page)
        if hasattr(st.session_state, 'page_override'):
            del st.session_state.page_override
        
        if page == "🏠 Home":
            self._home_page()
        elif page == "🔍 Subreddit Finder":
            self._subreddit_finder_page()
        elif page == "🔥 Active Discussions":
            self._active_discussions_page()
        elif page == "📈 Trending Discussions":
            self._trending_discussions_page()
        elif page == "🆕 New Discussions":
            self._new_discussions_page()
        elif page == "📊 Subreddit Analytics":
            self._analytics_page()
        elif page == "💭 Sentiment Analysis":
            self._sentiment_analysis_page()
        elif page == "🔎 Keyword Search":
            self._keyword_search_page()
        elif page == "🌐 Global Search":
            self._global_search_page()
        elif page == "☁️ Word Cloud":
            self._wordcloud_page()
        elif page == "⚙️ Settings":
            self._settings_page()
    
    def _home_page(self):
        """Home page with overview and quick access."""
        st.title("🔍 Reddit Explorer")
        st.markdown("**Comprehensive Reddit analysis and discovery tool**")
        
        # Welcome section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Welcome to Reddit Explorer! 
            
            Discover, analyze, and explore Reddit communities with powerful tools:
            
            - **🔍 Subreddit Finder**: Find relevant communities
            - **🔥 Active Discussions**: See what's hot right now
            - **📈 Trending Discussions**: Discover viral content
            - **📊 Analytics**: Deep dive into subreddit metrics
            - **💭 Sentiment Analysis**: Understand community mood
            - **🔎 Keyword Search**: Find discussions about specific topics
            """)
        
        with col2:
            st.markdown("### Quick Start")
            
            # Quick search
            quick_query = st.text_input("Quick subreddit search:", placeholder="e.g., python, startup")
            if quick_query:
                with st.spinner("Searching..."):
                    results = self.scout.search_subreddits(quick_query, limit=5)
                    for result in results:
                        st.write(f"**r/{result['name']}** - {result['subscribers']:,} subscribers")
        
        # Popular subreddits overview
        st.markdown("### Popular Subreddits")
        
        cols = st.columns(4)
        for i, subreddit in enumerate(settings.default_subreddits[:8]):
            with cols[i % 4]:
                if st.button(f"r/{subreddit}", key=f"home_{subreddit}"):
                    st.session_state.target_subreddit = subreddit
                    st.session_state.page_override = "🔥 Active Discussions"
                    st.rerun()
    
    def _subreddit_finder_page(self):
        """Subreddit finder and explorer."""
        st.title("🔍 Subreddit Finder")
        st.markdown("Discover relevant Reddit communities")
        
        # Search form
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "Search for subreddits:",
                placeholder="e.g., machine learning, cryptocurrency, cooking",
                key="subreddit_search"
            )
        
        with col2:
            limit = st.number_input("Results limit:", min_value=5, max_value=100, value=25)
        
        with col3:
            search_button = st.button("🔍 Search", type="primary")
        
        if search_query and search_button:
            with st.spinner("Searching subreddits..."):
                results = self.scout.search_subreddits(search_query, limit=limit)
                
                if results:
                    st.success(f"Found {len(results)} subreddits")
                    
                    # Display results
                    for result in results:
                        with st.expander(f"r/{result['name']} - {result['subscribers']:,} subscribers"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**{result['title']}**")
                                st.write(result['description'])
                                st.write(f"🔗 [View on Reddit]({result['url']})")
                                
                                if result['nsfw']:
                                    st.warning("⚠️ NSFW Content")
                            
                            with col2:
                                st.metric("Subscribers", f"{result['subscribers']:,}")
                                st.metric("Created", result['created_utc'].strftime("%Y-%m-%d"))
                                
                                if st.button(f"Analyze r/{result['name']}", key=f"analyze_{result['name']}"):
                                    st.session_state.target_subreddit = result['name']
                                    st.session_state.page_override = "📊 Subreddit Analytics"
                                    st.rerun()
                else:
                    st.warning("No subreddits found. Try different keywords.")
    
    def _active_discussions_page(self):
        """Active discussions explorer."""
        st.title("🔥 Active Discussions")
        st.markdown("Explore the most active discussions happening now")
        
        # Input form
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit:",
                value=getattr(st.session_state, 'target_subreddit', 'python'),
                placeholder="e.g., python, technology, startups"
            )
        
        with col2:
            limit = st.number_input("Number of posts:", min_value=10, max_value=100, value=50)
        
        with col3:
            if st.button("🔥 Get Active Discussions", type="primary"):
                st.session_state.active_trigger = True
        
        if st.button("📈 Switch to Trending") or subreddit and getattr(st.session_state, 'active_trigger', False):
            if 'active_trigger' in st.session_state:
                del st.session_state.active_trigger
                
            with st.spinner("Fetching active discussions..."):
                discussions = self.scout.get_active_discussions(subreddit, limit=limit)
                
                if discussions:
                    st.success(f"Found {len(discussions)} active discussions in r/{subreddit}")
                    
                    # Display discussions
                    for i, discussion in enumerate(discussions, 1):
                        self._display_discussion(discussion, i)
                else:
                    st.warning(f"No discussions found in r/{subreddit}")
    
    def _trending_discussions_page(self):
        """Trending discussions explorer."""
        st.title("📈 Trending Discussions")
        st.markdown("Discover what's trending on Reddit")
        
        # Input form
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit:",
                value=getattr(st.session_state, 'target_subreddit', 'technology'),
                placeholder="e.g., technology, worldnews, science"
            )
        
        with col2:
            time_filter = st.selectbox(
                "Time period:",
                ["hour", "day", "week", "month", "year", "all"],
                index=2
            )
        
        with col3:
            limit = st.number_input("Number of posts:", min_value=10, max_value=100, value=50)
        
        with col4:
            if st.button("📈 Get Trending", type="primary"):
                st.session_state.trending_trigger = True
        
        if subreddit and getattr(st.session_state, 'trending_trigger', False):
            if 'trending_trigger' in st.session_state:
                del st.session_state.trending_trigger
                
            with st.spinner("Fetching trending discussions..."):
                discussions = self.scout.get_trending_discussions(subreddit, limit=limit, time_filter=time_filter)
                
                if discussions:
                    st.success(f"Found {len(discussions)} trending discussions in r/{subreddit}")
                    
                    # Show trends chart
                    if len(discussions) > 5:
                        df = pd.DataFrame(discussions)
                        fig = px.scatter(
                            df.head(20), 
                            x='num_comments', 
                            y='score',
                            size='activity_score',
                            hover_data=['title'],
                            title=f"Engagement Pattern - r/{subreddit}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display discussions
                    for i, discussion in enumerate(discussions, 1):
                        self._display_discussion(discussion, i)
                else:
                    st.warning(f"No trending discussions found in r/{subreddit}")
    
    def _new_discussions_page(self):
        """New discussions explorer."""
        st.title("🆕 New Discussions")
        st.markdown("See the latest posts and discussions")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit:",
                value=getattr(st.session_state, 'target_subreddit', 'programming'),
                placeholder="e.g., programming, AskReddit, todayilearned"
            )
        
        with col2:
            limit = st.number_input("Number of posts:", min_value=10, max_value=100, value=50)
        
        if st.button("🆕 Get New Discussions", type="primary") and subreddit:
            with st.spinner("Fetching new discussions..."):
                discussions = self.scout.get_new_discussions(subreddit, limit=limit)
                
                if discussions:
                    st.success(f"Found {len(discussions)} new discussions in r/{subreddit}")
                    
                    # Display discussions
                    for i, discussion in enumerate(discussions, 1):
                        self._display_discussion(discussion, i, show_age=True)
                else:
                    st.warning(f"No new discussions found in r/{subreddit}")
    
    def _analytics_page(self):
        """Subreddit analytics and insights."""
        st.title("📊 Subreddit Analytics")
        st.markdown("Deep dive into subreddit metrics and patterns")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit to analyze:",
                value=getattr(st.session_state, 'target_subreddit', 'datascience'),
                placeholder="e.g., datascience, MachineLearning, entrepreneur"
            )
        
        with col2:
            limit = st.number_input("Posts to analyze:", min_value=50, max_value=500, value=100)
        
        if st.button("📊 Analyze Subreddit", type="primary") and subreddit:
            with st.spinner("Analyzing subreddit..."):
                # Get subreddit info
                info = self.scout.get_subreddit_info(subreddit)
                analytics = self.scout.get_subreddit_analytics(subreddit, limit=limit)
                
                if info and 'error' not in analytics:
                    # Subreddit overview
                    st.subheader(f"r/{info['name']} Overview")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Subscribers", f"{info['subscribers']:,}")
                    with col2:
                        st.metric("Active Users", f"{info.get('active_users', 0):,}")
                    with col3:
                        age = datetime.now() - info['created_utc']
                        st.metric("Age (years)", f"{age.days // 365}")
                    with col4:
                        st.metric("Posts Analyzed", analytics['total_posts'])
                    
                    st.markdown(f"**Description:** {info['public_description']}")
                    
                    # Analytics metrics
                    st.subheader("📈 Engagement Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Avg Score", f"{analytics['avg_score']:.1f}")
                    with col2:
                        st.metric("Avg Comments", f"{analytics['avg_comments']:.1f}")
                    with col3:
                        st.metric("Avg Upvote Ratio", f"{analytics['avg_upvote_ratio']:.2f}")
                    
                    # Engagement distribution
                    if 'engagement_distribution' in analytics:
                        st.subheader("🎯 Engagement Distribution")
                        
                        engagement_data = analytics['engagement_distribution']
                        fig = go.Figure(data=[
                            go.Bar(
                                x=['High', 'Medium', 'Low'],
                                y=[engagement_data['high_engagement'], 
                                   engagement_data['medium_engagement'], 
                                   engagement_data['low_engagement']],
                                marker_color=['#ff6b6b', '#ffd93d', '#6bcf7f']
                            )
                        ])
                        fig.update_layout(title="Engagement Distribution", xaxis_title="Engagement Level", yaxis_title="Number of Posts")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Top authors
                    if 'top_authors' in analytics:
                        st.subheader("👤 Top Authors")
                        authors_df = pd.DataFrame(list(analytics['top_authors'].items()), columns=['Author', 'Posts'])
                        st.dataframe(authors_df, use_container_width=True)
                    
                    # Posting patterns
                    if 'activity_by_hour' in analytics and analytics['activity_by_hour']:
                        st.subheader("🕒 Posting Patterns by Hour")
                        
                        hour_data = analytics['activity_by_hour']
                        fig = px.bar(
                            x=list(hour_data.keys()),
                            y=list(hour_data.values()),
                            title="Posts by Hour of Day"
                        )
                        fig.update_layout(xaxis_title="Hour", yaxis_title="Number of Posts")
                        st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.error("Failed to analyze subreddit. Please check the name and try again.")
    
    def _sentiment_analysis_page(self):
        """Sentiment analysis of subreddit content."""
        st.title("💭 Sentiment Analysis")
        st.markdown("Analyze the mood and sentiment of Reddit communities")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit to analyze:",
                value=getattr(st.session_state, 'target_subreddit', 'politics'),
                placeholder="e.g., politics, worldnews, cryptocurrency"
            )
        
        with col2:
            limit = st.number_input("Posts to analyze:", min_value=50, max_value=300, value=100)
        
        if st.button("💭 Analyze Sentiment", type="primary") and subreddit:
            with st.spinner("Analyzing sentiment..."):
                sentiment_data = self.scout.analyze_subreddit_sentiment(subreddit, limit=limit)
                
                if sentiment_data['total_analyzed'] > 0:
                    st.success(f"Analyzed {sentiment_data['total_analyzed']} texts from r/{subreddit}")
                    
                    # Sentiment distribution
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("📊 Sentiment Distribution")
                        
                        fig = go.Figure(data=[
                            go.Pie(
                                labels=['Positive', 'Neutral', 'Negative'],
                                values=[
                                    sentiment_data['percentages']['positive'],
                                    sentiment_data['percentages']['neutral'],
                                    sentiment_data['percentages']['negative']
                                ],
                                marker_colors=['#6bcf7f', '#ffd93d', '#ff6b6b']
                            )
                        ])
                        fig.update_layout(title="Community Sentiment")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("📈 Sentiment Metrics")
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("😊 Positive", f"{sentiment_data['percentages']['positive']:.1f}%")
                        with col_b:
                            st.metric("😐 Neutral", f"{sentiment_data['percentages']['neutral']:.1f}%")
                        with col_c:
                            st.metric("😞 Negative", f"{sentiment_data['percentages']['negative']:.1f}%")
                    
                    # Sample texts
                    if sentiment_data['sample_texts']:
                        st.subheader("📝 Sample Analysis")
                        
                        for sample in sentiment_data['sample_texts'][:5]:
                            sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}
                            st.write(f"{sentiment_emoji[sample['sentiment']]} **{sample['sentiment'].title()}** (Score: {sample['score']})")
                            st.write(f"_{sample['text']}_")
                            st.markdown("---")
                
                else:
                    st.warning("No sentiment data available. Try a different subreddit.")
    
    def _keyword_search_page(self):
        """Keyword-based discussion search."""
        st.title("🔎 Keyword Search")
        st.markdown("Find discussions containing specific keywords across multiple subreddits")
        
        # Input form
        col1, col2 = st.columns([2, 2])
        
        with col1:
            keywords = st.text_area(
                "Keywords (one per line):",
                value="AI\nChatGPT\nPython",
                height=100
            )
        
        with col2:
            subreddits = st.text_area(
                "Subreddits (one per line):",
                value="programming\ntechnology\nMachineLearning",
                height=100
            )
        
        limit = st.number_input("Results per keyword:", min_value=10, max_value=100, value=20)
        
        if st.button("🔎 Search Keywords", type="primary"):
            keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]
            subreddit_list = [s.strip() for s in subreddits.split('\n') if s.strip()]
            
            if keyword_list and subreddit_list:
                with st.spinner("Searching across subreddits..."):
                    results = self.scout.get_keyword_discussions(keyword_list, subreddit_list, limit=limit)
                    
                    if results:
                        st.success(f"Found {len(results)} discussions")
                        
                        # Group by keyword
                        for keyword in keyword_list:
                            keyword_results = [r for r in results if r['matched_keyword'] == keyword]
                            if keyword_results:
                                st.subheader(f"🔍 Results for '{keyword}' ({len(keyword_results)} found)")
                                
                                for result in keyword_results[:10]:  # Show top 10 per keyword
                                    self._display_discussion(result, show_subreddit=True, show_keyword=True)
                    else:
                        st.warning("No discussions found for the specified keywords.")
            else:
                st.error("Please provide at least one keyword and one subreddit.")
    
    def _global_search_page(self):
        """Global keyword search across all of Reddit."""
        st.title("🌐 Global Search")
        st.markdown("Search for discussions across **ALL of Reddit** - not limited to specific subreddits!")
        
        # Create info box
        st.info("💡 **Tip:** This searches the entire Reddit platform. Great for discovering new communities and trending topics!")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            keywords = st.text_area(
                "Keywords to search (one per line):",
                value="artificial intelligence\nmachine learning\nChatGPT",
                height=100,
                help="Enter keywords or phrases to search across all of Reddit"
            )
        
        with col2:
            time_filter = st.selectbox(
                "Time range:",
                options=["all", "year", "month", "week", "day"],
                index=3,  # Default to 'week'
                help="Filter results by time period"
            )
            
            limit = st.number_input(
                "Max results:", 
                min_value=25, 
                max_value=500, 
                value=100,
                step=25,
                help="Maximum number of results to retrieve"
            )
        
        # Advanced options with country filter
        with st.expander("🔧 Advanced Options"):
            col1, col2, col3 = st.columns(3)
            with col1:
                min_score = st.number_input("Minimum score:", min_value=0, value=10)
                exclude_nsfw = st.checkbox("Exclude NSFW content", value=True)
            with col2:
                min_comments = st.number_input("Minimum comments:", min_value=0, value=5)
                show_preview = st.checkbox("Show post previews", value=True)
            with col3:
                # Country filter
                country_filter = st.selectbox(
                    "Filter by country subreddit:",
                    options=["All", "USA", "UK", "Canada", "Australia", "Germany", "France", "Spain", "Mexico", "Brazil", "India", "Japan", "Korea"],
                    help="Filter results to country-specific subreddits"
                )
                
                # Map countries to subreddit patterns
                country_subreddits = {
                    "USA": ["usa", "america", "unitedstates"],
                    "UK": ["unitedkingdom", "ukpolitics", "britishproblems", "casualuk"],
                    "Canada": ["canada", "onguardforthee", "canadapolitics"],
                    "Australia": ["australia", "straya", "aussie"],
                    "Germany": ["germany", "de", "deutschland"],
                    "France": ["france", "french"],
                    "Spain": ["spain", "es", "espana"],
                    "Mexico": ["mexico", "mujico"],
                    "Brazil": ["brasil", "brazil"],
                    "India": ["india", "indiaspeaks", "indianews"],
                    "Japan": ["japan", "japanlife", "newsokur"],
                    "Korea": ["korea", "hanguk"]
                }
        
        if st.button("🌐 Search Globally", type="primary"):
            keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]
            
            if keyword_list:
                with st.spinner(f"Searching across all of Reddit for {len(keyword_list)} keywords..."):
                    # Update filters temporarily
                    old_min_score = settings.min_score_threshold
                    old_min_comments = settings.min_comments_threshold
                    old_exclude_nsfw = settings.exclude_nsfw
                    
                    settings.min_score_threshold = min_score
                    settings.min_comments_threshold = min_comments
                    settings.exclude_nsfw = exclude_nsfw
                    
                    try:
                        results = self.scout.search_global_keywords(keyword_list, limit=limit, time_filter=time_filter)
                        
                        # Apply country filter if selected
                        if country_filter != "All" and country_filter in country_subreddits:
                            country_subs = country_subreddits[country_filter]
                            results = [r for r in results if any(cs in r['subreddit'].lower() for cs in country_subs)]
                            
                    finally:
                        # Restore original settings
                        settings.min_score_threshold = old_min_score
                        settings.min_comments_threshold = old_min_comments
                        settings.exclude_nsfw = old_exclude_nsfw
                    
                    if results:
                        st.success(f"🎯 Found {len(results)} discussions across Reddit!")
                        
                        # Summary statistics
                        unique_subreddits = set(r['subreddit'] for r in results)
                        st.markdown(f"**📊 Summary:** {len(results)} posts from {len(unique_subreddits)} different subreddits")
                        
                        # Keyword distribution
                        keyword_counts = {}
                        for r in results:
                            keyword = r.get('matched_keyword', 'Unknown')
                            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
                        
                        # Display keyword summary
                        col1, col2, col3 = st.columns(3)
                        for i, (keyword, count) in enumerate(keyword_counts.items()):
                            if i % 3 == 0:
                                col1.metric(f"🔍 {keyword}", count)
                            elif i % 3 == 1:
                                col2.metric(f"🔍 {keyword}", count)
                            else:
                                col3.metric(f"🔍 {keyword}", count)
                        
                        # Tabs for different views
                        tab1, tab2, tab3 = st.tabs(["📑 All Results", "🏆 Top Subreddits", "📊 Analytics"])
                        
                        with tab1:
                            # Display results
                            for idx, post in enumerate(results[:50]):  # Limit display to 50
                                with st.container():
                                    col1, col2 = st.columns([5, 1])
                                    
                                    with col1:
                                        # Title with link - handle both 'permalink' and 'url' fields
                                        post_url = post.get('permalink', post.get('url', '#'))
                                        st.markdown(f"### [{post['title']}]({post_url})")
                                        
                                        # Metadata
                                        meta_parts = [
                                            f"r/{post['subreddit']}",
                                            f"👤 u/{post['author']}",
                                            f"⬆️ {post['score']:,}",
                                            f"💬 {post['num_comments']:,}",
                                            f"🔍 {post['matched_keyword']}"
                                        ]
                                        
                                        if post.get('subreddit_subscribers', 0) > 0:
                                            meta_parts.append(f"👥 {post['subreddit_subscribers']:,} subscribers")
                                        
                                        st.markdown(" • ".join(meta_parts))
                                        
                                        # Preview text if available and enabled
                                        if show_preview and post.get('preview_text'):
                                            st.markdown(f"_{post['preview_text']}_")
                                        
                                        # Time info
                                        st.caption(f"Posted {post['created_utc'].strftime('%Y-%m-%d %H:%M')}")
                                    
                                    with col2:
                                        # Engagement metrics
                                        engagement = (post['score'] + post['num_comments'] * 2) / 100
                                        st.metric("Engagement", f"{engagement:.1f}")
                                    
                                    st.markdown("---")
                        
                        with tab2:
                            # Top subreddits analysis
                            subreddit_stats = {}
                            for post in results:
                                sub = post['subreddit']
                                if sub not in subreddit_stats:
                                    subreddit_stats[sub] = {
                                        'count': 0,
                                        'total_score': 0,
                                        'total_comments': 0,
                                        'subscribers': post.get('subreddit_subscribers', 0)
                                    }
                                subreddit_stats[sub]['count'] += 1
                                subreddit_stats[sub]['total_score'] += post['score']
                                subreddit_stats[sub]['total_comments'] += post['num_comments']
                            
                            # Convert to dataframe
                            sub_df = pd.DataFrame([
                                {
                                    'Subreddit': sub,
                                    'Posts': stats['count'],
                                    'Avg Score': stats['total_score'] / stats['count'],
                                    'Avg Comments': stats['total_comments'] / stats['count'],
                                    'Subscribers': stats['subscribers']
                                }
                                for sub, stats in subreddit_stats.items()
                            ])
                            
                            # Sort by post count
                            sub_df = sub_df.sort_values('Posts', ascending=False).head(20)
                            
                            # Display chart
                            if not sub_df.empty:
                                fig = px.bar(
                                    sub_df.head(15), 
                                    x='Subreddit', 
                                    y='Posts',
                                    title="Top Subreddits by Post Count",
                                    hover_data=['Avg Score', 'Avg Comments', 'Subscribers']
                                )
                                fig.update_layout(xaxis_tickangle=-45)
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Display table
                                st.dataframe(
                                    sub_df.style.format({
                                        'Avg Score': '{:.0f}',
                                        'Avg Comments': '{:.0f}',
                                        'Subscribers': '{:,.0f}'
                                    }),
                                    use_container_width=True
                                )
                        
                        with tab3:
                            # Analytics
                            st.subheader("📊 Search Analytics")
                            
                            # Time distribution
                            times_df = pd.DataFrame([
                                {'Time': post['created_utc'], 'Score': post['score']}
                                for post in results
                            ])
                            
                            if not times_df.empty:
                                fig = px.scatter(
                                    times_df, 
                                    x='Time', 
                                    y='Score',
                                    title="Score Distribution Over Time"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Engagement distribution
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Score distribution
                                scores = [post['score'] for post in results]
                                fig = px.histogram(
                                    x=scores, 
                                    nbins=30,
                                    title="Score Distribution",
                                    labels={'x': 'Score', 'y': 'Number of Posts'}
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Comments distribution
                                comments = [post['num_comments'] for post in results]
                                fig = px.histogram(
                                    x=comments, 
                                    nbins=30,
                                    title="Comments Distribution",
                                    labels={'x': 'Number of Comments', 'y': 'Number of Posts'}
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Summary stats
                            st.subheader("📈 Summary Statistics")
                            
                            total_score = sum(post['score'] for post in results)
                            total_comments = sum(post['num_comments'] for post in results)
                            
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Total Score", f"{total_score:,}")
                            col2.metric("Total Comments", f"{total_comments:,}")
                            col3.metric("Avg Score", f"{total_score/len(results):.0f}")
                            col4.metric("Avg Comments", f"{total_comments/len(results):.0f}")
                            
                    else:
                        st.warning("No results found. Try different keywords or adjust filters.")
            else:
                st.warning("Please enter at least one keyword to search.")
    
    def _wordcloud_page(self):
        """Word cloud generation from subreddit content."""
        st.title("☁️ Word Cloud")
        st.markdown("Visualize the most common words in subreddit discussions")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            subreddit = st.text_input(
                "Subreddit:",
                value=getattr(st.session_state, 'target_subreddit', 'technology'),
                placeholder="e.g., technology, science, books"
            )
        
        with col2:
            limit = st.number_input("Posts to analyze:", min_value=10, max_value=100, value=25, help="⚡ Lower values = faster processing")
        
        if st.button("☁️ Generate Word Cloud", type="primary") and subreddit:
            with st.spinner("Generating word cloud..."):
                try:
                    wordcloud_data = self.scout.generate_wordcloud_data(subreddit, limit=limit)
                    
                    if 'error' in wordcloud_data:
                        st.error(f"Error: {wordcloud_data.get('error', 'Unknown error')}")
                        if 'error_type' in wordcloud_data:
                            st.error(f"Error type: {wordcloud_data['error_type']}")
                        return
                        
                except Exception as e:
                    st.error(f"Exception in Word Cloud generation: {type(e).__name__}: {e}")
                    return
                
                # Only proceed if we have valid data
                if isinstance(wordcloud_data, dict) and 'word_frequencies' in wordcloud_data and wordcloud_data.get('word_frequencies'):
                    st.success(f"Analyzed {wordcloud_data['total_words']} words from r/{subreddit}")
                    
                    # Show additional stats
                    if 'filtered_words' in wordcloud_data:
                        st.info(f"Filtered {wordcloud_data['filtered_words']} meaningful words from {wordcloud_data['total_words']} total words")
                    
                    # Word frequency chart
                    st.subheader("📊 Top Words")
                    
                    top_words = list(wordcloud_data['word_frequencies'].items())[:20]
                    if top_words:
                        words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                        
                        fig = px.bar(
                            words_df, 
                            x='Word', 
                            y='Frequency',
                            title=f"Most Common Words in r/{subreddit}",
                            color='Frequency',
                            color_continuous_scale='blues'
                        )
                        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Word statistics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Words", f"{wordcloud_data['total_words']:,}")
                        with col2:
                            st.metric("Unique Words", f"{wordcloud_data['unique_words']:,}")
                        with col3:
                            st.metric("Filtered Words", f"{wordcloud_data.get('filtered_words', 0):,}")
                        with col4:
                            if wordcloud_data['total_words'] > 0:
                                diversity = (wordcloud_data['unique_words'] / wordcloud_data['total_words']) * 100
                                st.metric("Vocabulary Diversity", f"{diversity:.1f}%")
                        
                        # Display word cloud visualization using wordcloud library
                        try:
                            from wordcloud import WordCloud
                            import matplotlib.pyplot as plt
                            
                            # Generate word cloud
                            wc = WordCloud(
                                width=800, 
                                height=400, 
                                background_color='white',
                                colormap='Blues',
                                max_words=100
                            ).generate_from_frequencies(wordcloud_data['word_frequencies'])
                            
                            # Display the word cloud
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(wc, interpolation='bilinear')
                            ax.axis('off')
                            ax.set_title(f"Word Cloud for r/{subreddit}", fontsize=16, pad=20)
                            st.pyplot(fig)
                            plt.close()
                            
                        except ImportError:
                            st.info("Install 'matplotlib' for word cloud visualization")
                        except Exception as e:
                            st.warning(f"Could not generate visual word cloud: {e}")
                        
                        # Text sample
                        with st.expander("📝 Text Sample"):
                            st.text_area("Sample text analyzed:", wordcloud_data.get('text_sample', ''), height=100)
                    else:
                        st.warning("No words found after filtering. This might be due to very short posts or posts in non-English languages.")
                        
                else:
                    st.warning("No word frequency data found. The subreddit might be empty or have very few posts.")
    
    def _settings_page(self):
        """Settings and configuration page."""
        st.title("⚙️ Settings")
        st.markdown("Configure Reddit Explorer settings")
        
        # API Settings
        st.subheader("🔑 Reddit API Configuration")
        
        with st.expander("Reddit API Credentials", expanded=False):
            st.info("Configure your Reddit API credentials for enhanced functionality")
            
            client_id = st.text_input("Client ID:", value=settings.reddit_client_id, type="password")
            client_secret = st.text_input("Client Secret:", value=settings.reddit_client_secret, type="password")
            user_agent = st.text_input("User Agent:", value=settings.reddit_user_agent)
            
            if st.button("Test Connection"):
                with st.spinner("Testing connection..."):
                    # Here you could test the connection
                    st.success("✅ Connection test successful!")
        
        # Content Filtering
        st.subheader("🔍 Content Filtering")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_score = st.number_input("Minimum Score:", value=settings.min_score_threshold)
            min_comments = st.number_input("Minimum Comments:", value=settings.min_comments_threshold)
            exclude_nsfw = st.checkbox("Exclude NSFW Content", value=settings.exclude_nsfw)
        
        with col2:
            exclude_spoilers = st.checkbox("Exclude Spoilers", value=settings.exclude_spoilers)
            max_posts = st.number_input("Max Posts Per Request:", value=settings.max_posts_per_request)
            time_filter = st.selectbox("Default Time Filter:", 
                                     ["hour", "day", "week", "month", "year", "all"],
                                     index=2)
        
        # Analytics Settings
        st.subheader("📊 Analytics Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_enabled = st.checkbox("Enable Sentiment Analysis", value=settings.sentiment_analysis_enabled)
            wordcloud_enabled = st.checkbox("Enable Word Cloud", value=settings.wordcloud_enabled)
        
        with col2:
            engagement_enabled = st.checkbox("Enable Engagement Metrics", value=settings.engagement_metrics_enabled)
        
        # Default Subreddits
        st.subheader("📝 Default Subreddits")
        
        subreddits_text = st.text_area(
            "Default subreddits (one per line):",
            value='\n'.join(settings.default_subreddits),
            height=100
        )
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved! (Note: This is a demo - settings are not persisted)")
    
    def _display_discussion(self, discussion: Dict, index: int = None, show_age: bool = False, 
                          show_subreddit: bool = False, show_keyword: bool = False):
        """Display a discussion in a consistent format."""
        with st.expander(f"{'#{} '.format(index) if index else ''}{discussion['title'][:80]}..."):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{discussion['title']}**")
                if discussion.get('selftext'):
                    preview = discussion['selftext'][:200] + "..." if len(discussion['selftext']) > 200 else discussion['selftext']
                    st.write(preview)
                
                st.write(f"👤 u/{discussion['author']}")
                if show_subreddit:
                    st.write(f"📍 r/{discussion.get('subreddit', 'unknown')}")
                if show_keyword:
                    st.write(f"🔍 Matched: **{discussion.get('matched_keyword', '')}**")
                
                post_url = discussion.get('url', discussion.get('permalink', '#'))
                st.write(f"🔗 [View on Reddit]({post_url})")
            
            with col2:
                st.metric("Score", discussion['score'])
                st.metric("Comments", discussion['num_comments'])
                st.metric("Upvote %", f"{discussion['upvote_ratio']*100:.0f}%")
                
                if show_age:
                    age = datetime.now() - discussion['created_utc']
                    if age.days > 0:
                        st.metric("Age", f"{age.days}d")
                    else:
                        st.metric("Age", f"{age.seconds//3600}h")
                else:
                    st.metric("Activity", discussion['activity_score'])


def main():
    """Main entry point for the dashboard."""
    dashboard = RedditDashboard()
    dashboard.run()


if __name__ == "__main__":
    main() 