"""Reddit Scout - Comprehensive Reddit exploration and analysis."""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

import pandas as pd
import praw
from praw.models import Comment, Submission
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

from .config import settings


class RedditScout:
    """Reddit Scout for comprehensive Reddit exploration and analysis."""
    
    def __init__(self):
        """Initialize Reddit Scout with PRAW client."""
        self.reddit = None
        self._setup_reddit_client()
        
    def _setup_reddit_client(self):
        """Setup Reddit client with credentials."""
        try:
            self.reddit = praw.Reddit(
                client_id=settings.reddit_client_id,
                client_secret=settings.reddit_client_secret,
                user_agent=settings.reddit_user_agent,
                username=settings.reddit_username if settings.reddit_username else None,
                password=settings.reddit_password if settings.reddit_password else None,
            )
            # Test connection
            self.reddit.user.me()
            print("✅ Reddit API connection established")
        except Exception as e:
            print(f"⚠️ Reddit API setup failed: {e}")
            # Use read-only mode
            self.reddit = praw.Reddit(
                client_id=settings.reddit_client_id or "dummy",
                client_secret=settings.reddit_client_secret or "dummy",
                user_agent=settings.reddit_user_agent,
            )
    
    def search_subreddits(self, query: str, limit: int = 25) -> List[Dict]:
        """Search for subreddits by name or description."""
        results = []
        
        try:
            for subreddit in self.reddit.subreddits.search(query, limit=limit):
                try:
                    results.append({
                        'name': subreddit.display_name,
                        'title': subreddit.title,
                        'description': subreddit.public_description,
                        'subscribers': subreddit.subscribers or 0,
                        'created_utc': datetime.fromtimestamp(subreddit.created_utc),
                        'nsfw': subreddit.over18,
                        'url': f"https://reddit.com{subreddit.url}",
                        'active_users': getattr(subreddit, 'active_user_count', 0),
                    })
                except Exception as e:
                    print(f"Error processing subreddit {subreddit.display_name}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error searching subreddits: {e}")
            
        return sorted(results, key=lambda x: x['subscribers'] or 0, reverse=True)
    
    def get_subreddit_info(self, subreddit_name: str) -> Dict:
        """Get detailed information about a specific subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.description,
                'public_description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'active_users': getattr(subreddit, 'active_user_count', 0),
                'created_utc': datetime.fromtimestamp(subreddit.created_utc),
                'nsfw': subreddit.over18,
                'url': f"https://reddit.com{subreddit.url}",
                'submission_type': subreddit.submission_type,
                'lang': getattr(subreddit, 'lang', 'en'),
            }
        except Exception as e:
            print(f"Error getting subreddit info: {e}")
            return {}
    
    def get_active_discussions(self, subreddit_name: str, limit: int = 50, time_filter: str = 'day') -> List[Dict]:
        """Get active discussions from a subreddit."""
        discussions = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get hot posts (most active)
            for submission in subreddit.hot(limit=limit):
                if self._should_include_post(submission):
                    discussion_data = self._extract_submission_data(submission)
                    discussions.append(discussion_data)
                    
        except Exception as e:
            print(f"Error getting active discussions: {e}")
            
        return sorted(discussions, key=lambda x: x['activity_score'], reverse=True)
    
    def get_trending_discussions(self, subreddit_name: str, limit: int = 50, time_filter: str = 'day') -> List[Dict]:
        """Get trending discussions from a subreddit."""
        discussions = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get top posts by time filter
            for submission in subreddit.top(time_filter=time_filter, limit=limit):
                if self._should_include_post(submission):
                    discussion_data = self._extract_submission_data(submission)
                    discussions.append(discussion_data)
                    
        except Exception as e:
            print(f"Error getting trending discussions: {e}")
            
        return sorted(discussions, key=lambda x: x['score'], reverse=True)
    
    def get_new_discussions(self, subreddit_name: str, limit: int = 50) -> List[Dict]:
        """Get newest discussions from a subreddit."""
        discussions = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for submission in subreddit.new(limit=limit):
                if self._should_include_post(submission):
                    discussion_data = self._extract_submission_data(submission)
                    discussions.append(discussion_data)
                    
        except Exception as e:
            print(f"Error getting new discussions: {e}")
            
        return discussions
    
    def analyze_subreddit_sentiment(self, subreddit_name: str, limit: int = 100) -> Dict:
        """Analyze sentiment of posts and comments in a subreddit."""
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
        analyzed_texts = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for submission in subreddit.hot(limit=limit):
                # Analyze submission title and text
                texts_to_analyze = [submission.title]
                if hasattr(submission, 'selftext') and submission.selftext:
                    texts_to_analyze.append(submission.selftext)
                
                for text in texts_to_analyze:
                    sentiment = self._analyze_text_sentiment(text)
                    if sentiment:
                        sentiments[sentiment] += 1
                        analyzed_texts.append({
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            'sentiment': sentiment,
                            'post_id': submission.id,
                            'score': submission.score
                        })
                        
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            
        total = sum(sentiments.values())
        if total > 0:
            sentiment_percentages = {k: (v / total) * 100 for k, v in sentiments.items()}
        else:
            sentiment_percentages = sentiments
            
        return {
            'counts': sentiments,
            'percentages': sentiment_percentages,
            'total_analyzed': total,
            'sample_texts': analyzed_texts[:20]  # Return sample
        }
    
    def get_keyword_discussions(self, keywords: List[str], subreddit_names: List[str], limit: int = 50) -> List[Dict]:
        """Search for discussions containing specific keywords across multiple subreddits."""
        all_discussions = []
        
        for subreddit_name in subreddit_names:
            for keyword in keywords:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    
                    for submission in subreddit.search(keyword, limit=limit//len(keywords)):
                        if self._should_include_post(submission):
                            discussion_data = self._extract_submission_data(submission)
                            discussion_data['matched_keyword'] = keyword
                            discussion_data['subreddit'] = subreddit_name
                            all_discussions.append(discussion_data)
                            
                except Exception as e:
                    print(f"Error searching keyword '{keyword}' in r/{subreddit_name}: {e}")
                    continue
                    
        return sorted(all_discussions, key=lambda x: x['score'], reverse=True)
    
    def search_global_keywords(self, keywords: List[str], limit: int = None, time_filter: str = 'all', search_comments: bool = False, country_filter: str = None) -> List[Dict]:
        """FAST search for discussions containing keywords across Reddit."""
        all_discussions = []
        seen_ids = set()  # To avoid duplicates
        
        # Set reasonable limits for speed
        max_results_per_keyword = min(limit or 50, 50)  # Cap at 50 results per keyword
        
        for keyword in keywords:
            try:
                print(f"🔍 FAST SEARCH for '{keyword}' across Reddit...")
                
                # FAST GLOBAL SEARCH - Limited but quick
                print(f"  Searching Reddit with limit: {max_results_per_keyword}")
                
                for submission in self.reddit.subreddit('all').search(
                    keyword, 
                    limit=max_results_per_keyword, 
                    time_filter=time_filter,
                    sort='relevance'
                ):
                    if submission.id in seen_ids:
                        continue
                        
                    seen_ids.add(submission.id)
                    
                    if self._should_include_post(submission):
                        discussion_data = self._extract_submission_data(submission)
                        discussion_data['matched_keyword'] = keyword
                        discussion_data['subreddit'] = submission.subreddit.display_name
                        discussion_data['match_location'] = 'post'
                        discussion_data['search_phase'] = 'global'
                        
                        # Add additional metadata
                        discussion_data['subreddit_subscribers'] = getattr(submission.subreddit, 'subscribers', 0) or 0
                        discussion_data['is_video'] = submission.is_video
                        discussion_data['preview_text'] = submission.selftext[:200] + '...' if submission.selftext and len(submission.selftext) > 200 else submission.selftext
                        
                        all_discussions.append(discussion_data)
                
                print(f"  Found {len([d for d in all_discussions if d.get('search_phase') == 'global' and d.get('matched_keyword') == keyword])} posts for '{keyword}'")
                
                # Optional: Quick search in a few popular subreddits (if enabled)
                if search_comments and country_filter:
                    print(f"  Optional: Quick search in {country_filter} subreddits...")
                    
                    # Define focused subreddit lists by country
                    country_subreddits = {
                        'Spain': ['SpainFIRE', 'spain', 'es', 'eupersonalfinance'],
                        'USA': ['personalfinance', 'investing', 'financialindependence', 'Fire'],
                        'UK': ['UKPersonalFinance', 'FIREUK', 'unitedkingdom'],
                        'Germany': ['Finanzen', 'germany', 'de'],
                        'France': ['vosfinances', 'france'],
                        'Canada': ['PersonalFinanceCanada', 'canada'],
                    }
                    
                    target_subs = country_subreddits.get(country_filter, [])[:3]  # Limit to 3 subreddits max
                    
                    for sub_name in target_subs:
                        try:
                            subreddit = self.reddit.subreddit(sub_name)
                            print(f"    🔍 Quick search in r/{sub_name}...")
                            
                            # Simple search - much faster
                            for submission in subreddit.search(keyword, limit=10, time_filter=time_filter):
                                if submission.id in seen_ids:
                                    continue
                                    
                                seen_ids.add(submission.id)
                                
                                if self._should_include_post(submission):
                                    discussion_data = self._extract_submission_data(submission)
                                    discussion_data['matched_keyword'] = keyword
                                    discussion_data['subreddit'] = submission.subreddit.display_name
                                    discussion_data['match_location'] = 'post'
                                    discussion_data['search_phase'] = 'country_focused'
                                    
                                    # Add additional metadata
                                    discussion_data['subreddit_subscribers'] = getattr(submission.subreddit, 'subscribers', 0) or 0
                                    discussion_data['is_video'] = submission.is_video
                                    discussion_data['preview_text'] = submission.selftext[:200] + '...' if submission.selftext and len(submission.selftext) > 200 else submission.selftext
                                    
                                    all_discussions.append(discussion_data)
                                    
                        except Exception as sub_error:
                            print(f"      ❌ r/{sub_name}: {sub_error}")
                            continue
                        
            except Exception as e:
                print(f"Error searching keyword '{keyword}': {e}")
                continue
                
        print(f"\n🎯 FAST SEARCH COMPLETE: {len(all_discussions)} total results found")
        
        # Sort by relevance: score and recency
        return sorted(all_discussions, key=lambda x: (x['score'], x['created_utc']), reverse=True)
    
    def get_subreddit_analytics(self, subreddit_name: str, limit: int = 100) -> Dict:
        """Get comprehensive analytics for a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for submission in subreddit.hot(limit=limit):
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'upvote_ratio': submission.upvote_ratio,
                    'created_utc': datetime.fromtimestamp(submission.created_utc),
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'is_self': submission.is_self,
                    'domain': submission.domain,
                })
            
            df = pd.DataFrame(posts)
            
            if df.empty:
                return {'error': 'No data available'}
            
            analytics = {
                'total_posts': len(df),
                'avg_score': df['score'].mean(),
                'avg_comments': df['num_comments'].mean(),
                'avg_upvote_ratio': df['upvote_ratio'].mean(),
                'top_authors': df['author'].value_counts().head(10).to_dict(),
                'post_types': {
                    'self_posts': (df['is_self'] == True).sum(),
                    'link_posts': (df['is_self'] == False).sum(),
                },
                'top_domains': df[df['is_self'] == False]['domain'].value_counts().head(10).to_dict(),
                'activity_by_hour': self._analyze_posting_times(df),
                'engagement_distribution': {
                    'high_engagement': (df['score'] > df['score'].quantile(0.8)).sum(),
                    'medium_engagement': ((df['score'] > df['score'].quantile(0.2)) & 
                                        (df['score'] <= df['score'].quantile(0.8))).sum(),
                    'low_engagement': (df['score'] <= df['score'].quantile(0.2)).sum(),
                }
            }
            
            return analytics
            
        except Exception as e:
            print(f"Error getting subreddit analytics: {e}")
            return {'error': str(e)}
    
    def generate_wordcloud_data(self, subreddit_name: str, limit: int = 100) -> Dict:
        """Generate word cloud data from subreddit posts without TextBlob dependency."""
        try:
            import re
            from collections import Counter
            
            # Extended stopwords in multiple languages
            stopwords = {
                # English
                'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
                'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
                'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
                'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
                'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
                'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
                'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
                'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
                'give', 'day', 'most', 'us', 'is', 'are', 'was', 'been', 'has', 'had',
                'were', 'am', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
                'can', 'much', 'many', 'lot', 'more', 'less', 'very', 'too', 'still',
                'being', 'going', 'why', 'before', 'here', 'there', 'where', 'does', 'did',
                'thing', 'things', 'something', 'someone', 'really', 'actually', 'probably',
                'maybe', 'seems', 'definitely', 'literally', 'basically', 'honestly',
                'obviously', 'clearly', 'certainly', 'exactly', 'absolutely', 'completely',
                # Spanish
                'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo',
                'le', 'da', 'su', 'por', 'son', 'con', 'no', 'me', 'todo', 'pero', 'más',
                'hay', 'ya', 'está', 'mi', 'si', 'porque', 'qué', 'solo', 'has', 'le',
                'ya', 'puede', 'ahora', 'cada', 'muy', 'sin', 'sobre', 'también', 'hasta',
                'donde', 'who', 'desde', 'todos', 'durante', 'tanto', 'menos', 'mucho',
                'ante', 'ellos', 'ella', 'uno', 'ser', 'tener', 'hacer', 'poder', 'decir',
                'ir', 'ver', 'dar', 'saber', 'querer', 'estar', 'poner', 'parecer', 'seguir',
                'para', 'como', 'con', 'del', 'una', 'este', 'esta', 'esto', 'ese', 'esa',
                'eso', 'aquel', 'aquella', 'aquello', 'los', 'las', 'nos', 'vos', 'les',
                'algo', 'alguien', 'nada', 'nadie', 'alguno', 'ninguno', 'mucho', 'poco',
                'tanto', 'demasiado', 'bastante', 'más', 'menos', 'muy', 'bien', 'mal',
                'mejor', 'peor', 'mayor', 'menor', 'primero', 'último', 'mismo', 'otro',
                # Reddit specific
                'reddit', 'comments', 'comment', 'post', 'posts', 'subreddit', 'edit', 
                'deleted', 'removed', 'http', 'https', 'com', 'www', 'amp', 'bot',
                'deleted', 'removed', 'moderator', 'automod', 'thanks', 'please',
                'thanks', 'thank', 'edit', 'update', 'tldr', 'tl;dr'
            }
            
            print(f"Fetching data from r/{subreddit_name}...")
            subreddit = self.reddit.subreddit(subreddit_name)
            all_text = []
            post_count = 0
            
            for submission in subreddit.hot(limit=limit):
                # Add title
                if submission.title:
                    all_text.append(submission.title)
                
                # Add selftext if it exists and is substantial
                if (hasattr(submission, 'selftext') and 
                    submission.selftext and 
                    submission.selftext not in ['[removed]', '[deleted]', ''] and 
                    len(submission.selftext) > 10):  # Only add substantial text
                    all_text.append(submission.selftext)
                
                # SKIP COMMENTS FOR SPEED - they're too slow to load
                # Comments can add 15+ seconds to processing time
                    
                post_count += 1
                if post_count >= limit:
                    break
            
            if not all_text:
                return {
                    'error': f'No text data found for r/{subreddit_name}. The subreddit might be private or have no content.',
                    'error_type': 'NoDataError',
                    'subreddit': subreddit_name
                }
            
            # Combine and clean text
            combined_text = ' '.join(all_text)
            print(f"Combined text length: {len(combined_text)} characters")
            
            # Clean and normalize text
            text_lower = combined_text.lower()
            
            # Extract words using regex (letters and numbers, including accented characters)
            words = re.findall(r'\b[a-záéíóúñüç0-9]+\b', text_lower)
            print(f"Extracted {len(words)} total words")
            
            # Filter words
            filtered_words = []
            for word in words:
                if (len(word) >= 4 and  # Minimum length
                    len(word) <= 20 and  # Maximum length  
                    word not in stopwords and  # Not a stopword
                    not word.isdigit() and  # Not just numbers
                    not word.startswith(('http', 'www', '.com', '.es', '.org'))):  # Not URLs
                    filtered_words.append(word)
            
            print(f"Filtered to {len(filtered_words)} meaningful words")
            
            if not filtered_words:
                return {
                    'error': f'No meaningful words found after filtering for r/{subreddit_name}. Try a subreddit with more text content.',
                    'error_type': 'NoWordsAfterFiltering',
                    'subreddit': subreddit_name,
                    'debug_info': {
                        'total_words': len(words),
                        'text_length': len(combined_text),
                        'posts_processed': post_count
                    }
                }
            
            # Count frequencies
            word_freq = Counter(filtered_words)
            
            # Get top words
            top_words = word_freq.most_common(100)
            
            return {
                'word_frequencies': dict(top_words),
                'total_words': len(words),
                'unique_words': len(set(filtered_words)),
                'filtered_words': len(filtered_words),
                'posts_processed': post_count,
                'text_sample': combined_text[:500] + '...' if len(combined_text) > 500 else combined_text
            }
            
        except Exception as e:
            import traceback
            error_msg = f"Error generating word cloud data for r/{subreddit_name}: {str(e)}"
            print(error_msg)
            print(f"Full traceback: {traceback.format_exc()}")
            return {
                'error': error_msg,
                'error_type': type(e).__name__,
                'subreddit': subreddit_name
            }
    
    def _should_include_post(self, submission) -> bool:
        """Check if a post should be included based on filters."""
        if settings.exclude_nsfw and submission.over_18:
            return False
        if settings.exclude_spoilers and submission.spoiler:
            return False
        if submission.score < settings.min_score_threshold:
            return False
        if submission.num_comments < settings.min_comments_threshold:
            return False
        return True
    
    def _extract_submission_data(self, submission) -> Dict:
        """Extract comprehensive data from a Reddit submission."""
        return {
            'id': submission.id,
            'title': submission.title,
            'author': str(submission.author) if submission.author else '[deleted]',
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio,
            'num_comments': submission.num_comments,
            'created_utc': datetime.fromtimestamp(submission.created_utc),
            'url': f"https://reddit.com{submission.permalink}",
            'permalink': f"https://reddit.com{submission.permalink}",  # Added for compatibility
            'domain': submission.domain,
            'is_self': submission.is_self,
            'selftext': submission.selftext if hasattr(submission, 'selftext') else '',
            'nsfw': submission.over_18,
            'spoiler': submission.spoiler,
            'stickied': submission.stickied,
            'activity_score': submission.score + (submission.num_comments * 2),  # Weighted activity score
            'engagement_rate': (submission.num_comments / max(submission.score, 1)) * 100,
        }
    
    def _analyze_text_sentiment(self, text: str) -> Optional[str]:
        """Analyze sentiment of text using TextBlob."""
        if not settings.sentiment_analysis_enabled:
            return None
            
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return None
    
    def _analyze_posting_times(self, df: pd.DataFrame) -> Dict:
        """Analyze posting patterns by hour."""
        try:
            df['hour'] = df['created_utc'].dt.hour
            hourly_counts = df['hour'].value_counts().sort_index()
            return hourly_counts.to_dict()
        except Exception as e:
            print(f"Error analyzing posting times: {e}")
            return {}
    
    def _detect_language(self, text: str) -> Optional[str]:
        """Detect language of text."""
        try:
            if len(text.strip()) < 20:  # Too short for reliable detection
                return None
            return detect(text)
        except (LangDetectException, Exception):
            return None 