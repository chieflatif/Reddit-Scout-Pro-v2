"""Configuration management for Reddit Explorer."""

from __future__ import annotations

from typing import List

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application Configuration
    app_title: str = Field(default="🔍 Reddit Explorer", description="Application title")
    environment: str = Field(default="development", description="Environment: development, production")
    debug: bool = Field(default=True, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Reddit API Configuration
    reddit_client_id: str = Field(default="", description="Reddit API client ID")
    reddit_client_secret: str = Field(default="", description="Reddit API client secret")
    reddit_user_agent: str = Field(default="RedditExplorer/1.0", description="Reddit API user agent")
    reddit_username: str = Field(default="", description="Reddit username (optional for read-only access)")
    reddit_password: str = Field(default="", description="Reddit password (optional for read-only access)")
    
    # Reddit Explorer Configuration
    default_subreddits: str = Field(
        default="python,programming,datascience,MachineLearning,technology,entrepreneur,startups",
        description="Default subreddits to explore (comma-separated)"
    )
    max_posts_per_request: int = Field(default=100, description="Maximum posts to fetch per request")
    max_comments_per_post: int = Field(default=50, description="Maximum comments to fetch per post")
    default_time_filter: str = Field(default="week", description="Default time filter: hour, day, week, month, year, all")
    
    # Content Filtering
    min_score_threshold: int = Field(default=5, description="Minimum score threshold for posts")
    min_comments_threshold: int = Field(default=3, description="Minimum comments threshold for posts")
    exclude_nsfw: bool = Field(default=True, description="Exclude NSFW content")
    exclude_spoilers: bool = Field(default=True, description="Exclude spoiler content")
    
    # Language and Geographic Filtering
    default_languages: str = Field(
        default="en,es", 
        description="Default languages to monitor (comma-separated ISO codes)"
    )
    
    # Search Configuration
    trending_keywords: str = Field(
        default="AI,ChatGPT,Python,startup,crypto,NFT,blockchain,fintech,SaaS,API",
        description="Keywords to track for trending analysis (comma-separated)"
    )
    
    # Rate Limiting
    reddit_requests_per_minute: int = Field(default=60, description="Reddit API requests per minute")
    request_delay_seconds: float = Field(default=1.0, description="Delay between requests in seconds")
    
    # Analytics Configuration
    sentiment_analysis_enabled: bool = Field(default=True, description="Enable sentiment analysis")
    wordcloud_enabled: bool = Field(default=True, description="Enable word cloud generation")
    engagement_metrics_enabled: bool = Field(default=True, description="Enable engagement metrics")
    
    @validator("default_subreddits")
    def parse_default_subreddits(cls, v: str) -> List[str]:
        """Parse comma-separated subreddits."""
        return [s.strip() for s in v.split(",") if s.strip()]
    
    @validator("default_languages")
    def parse_default_languages(cls, v: str) -> List[str]:
        """Parse comma-separated languages."""
        return [s.strip().lower() for s in v.split(",") if s.strip()]
    
    @validator("trending_keywords")
    def parse_trending_keywords(cls, v: str) -> List[str]:
        """Parse comma-separated trending keywords."""
        return [s.strip() for s in v.split(",") if s.strip()]

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings() 