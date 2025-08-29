"""Multi-user Reddit Scout client with per-user API key support."""

import praw
from typing import Optional, Dict, List, Any
from ..database.models import APIKey, UserPreferences
from ..database.database import get_db_session
from .encryption import decrypt_api_key
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class UserRedditScout:
    """Reddit Scout with per-user API key support."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.reddit = None
        self.preferences = None
        self._initialize_client()
        self._load_preferences()
    
    def _get_user_api_keys(self) -> Optional[APIKey]:
        """Get user's API keys from database."""
        db = get_db_session()
        try:
            return db.query(APIKey).filter(APIKey.user_id == self.user_id).first()
        except Exception as e:
            logger.error(f"Failed to get API keys for user {self.user_id}: {e}")
            return None
        finally:
            db.close()
    
    def _load_preferences(self):
        """Load user preferences."""
        db = get_db_session()
        try:
            self.preferences = db.query(UserPreferences).filter(
                UserPreferences.user_id == self.user_id
            ).first()
            
            if not self.preferences:
                # Create default preferences
                self.preferences = UserPreferences(
                    user_id=self.user_id,
                    default_subreddits='["python", "programming", "technology", "datascience"]'
                )
                db.add(self.preferences)
                db.commit()
        except Exception as e:
            logger.error(f"Failed to load preferences for user {self.user_id}: {e}")
            db.rollback()
        finally:
            db.close()
    
    def _initialize_client(self) -> bool:
        """Initialize Reddit client with user's API keys."""
        api_keys = self._get_user_api_keys()
        
        if not api_keys or not api_keys.reddit_client_id or not api_keys.reddit_client_secret_encrypted:
            logger.warning(f"No API keys found for user {self.user_id}")
            return False
        
        # Decrypt the client secret
        client_secret = decrypt_api_key(api_keys.reddit_client_secret_encrypted)
        
        if not client_secret:
            logger.error(f"Failed to decrypt API key for user {self.user_id}")
            return False
        
        try:
            self.reddit = praw.Reddit(
                client_id=api_keys.reddit_client_id,
                client_secret=client_secret,
                user_agent=api_keys.reddit_user_agent or "RedditScoutPro/2.0"
            )
            
            # Test the connection
            self.reddit.user.me()
            logger.info(f"Reddit client initialized successfully for user {self.user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client for user {self.user_id}: {e}")
            self.reddit = None
            return False
    
    def is_configured(self) -> bool:
        """Check if Reddit client is properly configured."""
        return self.reddit is not None
    
    def update_api_keys(self, client_id: str, client_secret: str, user_agent: str = None) -> Dict[str, any]:
        """Update user's API keys."""
        from .encryption import encrypt_api_key
        
        db = get_db_session()
        try:
            # Test the API keys first
            test_reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent or "RedditScoutPro/2.0"
            )
            
            # Try to make a simple API call to validate
            test_reddit.user.me()
            
            # Keys are valid, save them
            api_keys = db.query(APIKey).filter(APIKey.user_id == self.user_id).first()
            
            if not api_keys:
                api_keys = APIKey(user_id=self.user_id)
                db.add(api_keys)
            
            api_keys.reddit_client_id = client_id
            api_keys.reddit_client_secret_encrypted = encrypt_api_key(client_secret)
            api_keys.reddit_user_agent = user_agent or "RedditScoutPro/2.0"
            api_keys.updated_at = datetime.utcnow()
            
            db.commit()
            
            # Reinitialize Reddit client
            self._initialize_client()
            
            logger.info(f"API keys updated successfully for user {self.user_id}")
            return {"success": True, "message": "API keys saved and validated successfully"}
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update API keys for user {self.user_id}: {e}")
            return {"success": False, "message": f"Invalid API keys: {str(e)}"}
        finally:
            db.close()
    
    def get_default_subreddits(self) -> List[str]:
        """Get user's default subreddits."""
        if self.preferences and self.preferences.default_subreddits:
            try:
                return json.loads(self.preferences.default_subreddits)
            except:
                pass
        return ["python", "programming", "technology", "datascience"]
    
    def update_preferences(self, **kwargs) -> bool:
        """Update user preferences."""
        db = get_db_session()
        try:
            if not self.preferences:
                self.preferences = UserPreferences(user_id=self.user_id)
                db.add(self.preferences)
            
            # Update preferences
            for key, value in kwargs.items():
                if hasattr(self.preferences, key):
                    setattr(self.preferences, key, value)
            
            self.preferences.updated_at = datetime.utcnow()
            db.commit()
            
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update preferences for user {self.user_id}: {e}")
            return False
        finally:
            db.close()
    
    def search_subreddits(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Search for subreddits by query."""
        if not self.is_configured():
            return []
        
        try:
            subreddits = []
            for subreddit in self.reddit.subreddits.search(query, limit=limit):
                subreddits.append({
                    "name": subreddit.display_name,
                    "title": subreddit.title,
                    "description": subreddit.public_description,
                    "subscribers": subreddit.subscribers,
                    "created_utc": subreddit.created_utc,
                    "over18": subreddit.over18
                })
            return subreddits
        except Exception as e:
            logger.error(f"Failed to search subreddits: {e}")
            return []
    
    def get_subreddit_posts(self, subreddit_name: str, sort_type: str = "hot", 
                           time_filter: str = "week", limit: int = 25) -> List[Dict[str, Any]]:
        """Get posts from a subreddit."""
        if not self.is_configured():
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            # Get posts based on sort type
            if sort_type == "hot":
                submissions = subreddit.hot(limit=limit)
            elif sort_type == "new":
                submissions = subreddit.new(limit=limit)
            elif sort_type == "top":
                submissions = subreddit.top(time_filter=time_filter, limit=limit)
            elif sort_type == "rising":
                submissions = subreddit.rising(limit=limit)
            else:
                submissions = subreddit.hot(limit=limit)
            
            for post in submissions:
                # Apply user's content filters
                if self.preferences:
                    if post.score < self.preferences.min_score_threshold:
                        continue
                    if post.num_comments < self.preferences.min_comments_threshold:
                        continue
                    if self.preferences.exclude_nsfw and post.over_18:
                        continue
                    if self.preferences.exclude_spoilers and post.spoiler:
                        continue
                
                posts.append({
                    "id": post.id,
                    "title": post.title,
                    "author": str(post.author) if post.author else "[deleted]",
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "num_comments": post.num_comments,
                    "created_utc": post.created_utc,
                    "url": post.url,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "selftext": post.selftext,
                    "is_self": post.is_self,
                    "over_18": post.over_18,
                    "spoiler": post.spoiler,
                    "subreddit": post.subreddit.display_name
                })
            
            return posts
        except Exception as e:
            logger.error(f"Failed to get posts from r/{subreddit_name}: {e}")
            return []
    
    def search_posts(self, query: str, subreddits: List[str] = None, 
                    sort: str = "relevance", time_filter: str = "all", 
                    limit: int = 25) -> List[Dict[str, Any]]:
        """Search for posts across subreddits."""
        if not self.is_configured():
            return []
        
        try:
            posts = []
            
            if subreddits:
                # Search in specific subreddits
                subreddit_string = "+".join(subreddits)
                subreddit = self.reddit.subreddit(subreddit_string)
            else:
                # Search across all of Reddit
                subreddit = self.reddit.subreddit("all")
            
            submissions = subreddit.search(
                query, 
                sort=sort, 
                time_filter=time_filter, 
                limit=limit
            )
            
            for post in submissions:
                # Apply user's content filters
                if self.preferences:
                    if post.score < self.preferences.min_score_threshold:
                        continue
                    if post.num_comments < self.preferences.min_comments_threshold:
                        continue
                    if self.preferences.exclude_nsfw and post.over_18:
                        continue
                    if self.preferences.exclude_spoilers and post.spoiler:
                        continue
                
                posts.append({
                    "id": post.id,
                    "title": post.title,
                    "author": str(post.author) if post.author else "[deleted]",
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "num_comments": post.num_comments,
                    "created_utc": post.created_utc,
                    "url": post.url,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "selftext": post.selftext,
                    "is_self": post.is_self,
                    "over_18": post.over_18,
                    "spoiler": post.spoiler,
                    "subreddit": post.subreddit.display_name
                })
            
            return posts
        except Exception as e:
            logger.error(f"Failed to search posts: {e}")
            return []
    
    def get_subreddit_info(self, subreddit_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a subreddit."""
        if not self.is_configured():
            return None
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return {
                "name": subreddit.display_name,
                "title": subreddit.title,
                "description": subreddit.description,
                "public_description": subreddit.public_description,
                "subscribers": subreddit.subscribers,
                "active_user_count": subreddit.active_user_count,
                "created_utc": subreddit.created_utc,
                "over18": subreddit.over18,
                "lang": subreddit.lang,
                "subreddit_type": subreddit.subreddit_type,
                "url": f"https://reddit.com/r/{subreddit_name}"
            }
        except Exception as e:
            logger.error(f"Failed to get info for r/{subreddit_name}: {e}")
            return None
