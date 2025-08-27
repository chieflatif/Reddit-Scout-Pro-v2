# 🔍 Reddit Scout Pro

A comprehensive Reddit analysis and discovery tool with an intuitive Streamlit dashboard.

## Features

### 🔍 **Subreddit Discovery**
- Search for relevant subreddits by keywords
- Explore subreddit information and statistics
- Find communities based on topics and interests

### 🔥 **Active Discussions**
- View the most active discussions happening now
- Filter by subreddit and engagement levels
- Real-time activity scoring and ranking

### 📈 **Trending Analysis**
- Discover trending discussions across time periods
- Analyze viral content patterns
- Engagement distribution visualization

### 🆕 **Latest Content**
- Browse newest discussions and posts
- Track emerging topics and conversations
- Monitor fresh content in communities

### 📊 **Subreddit Analytics**
- Comprehensive subreddit metrics and insights
- Posting patterns and engagement analysis
- Author activity and content distribution
- Engagement level categorization

### 💭 **Sentiment Analysis**
- Analyze community mood and sentiment
- Positive/negative/neutral distribution
- Sample text analysis with sentiment scores

### 🔎 **Keyword Search**
- Search for discussions across multiple subreddits
- Multi-keyword and multi-subreddit support
- Targeted content discovery

### ☁️ **Word Cloud Generation**
- Visualize common words in discussions
- Frequency analysis and vocabulary diversity
- Text pattern insights

## Installation

### Prerequisites
- Python 3.11 or higher
- Poetry (recommended) or pip

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Scrapers
```

2. **Install dependencies with Poetry:**
```bash
poetry install
```

Or with pip:
```bash
pip install -r requirements.txt
```

3. **Reddit API Setup:**
   - Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
   - Create a new app (script type for personal use)
   - Note your Client ID and Client Secret

4. **Configure environment variables:**
   Create a `.env` file in the project root:
```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=RedditScoutPro/1.0
```

## Usage

### Running the Dashboard

**🎯 EASIEST WAY (Recommended):**
```bash
reddit-scout
```
*Note: Run `./setup_alias.sh` first, then restart terminal or run `source ~/.zshrc`*

**🚀 ALTERNATIVE (Direct script):**
```bash
./start.sh
```

**📘 MANUAL (Poetry):**
```bash
poetry run streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### ⚡ Quick Setup (One-time)
```bash
cd "/Users/martin/Reddit Scout Pro"
./setup_alias.sh
# Restart terminal or: source ~/.zshrc
reddit-scout
```

### Navigation

The dashboard includes several main sections:

- **🏠 Home**: Overview and quick access
- **🔍 Subreddit Finder**: Discover relevant communities  
- **🔥 Active Discussions**: Current hot topics
- **📈 Trending Discussions**: Viral content analysis
- **🆕 New Discussions**: Latest posts and conversations
- **📊 Subreddit Analytics**: Deep metrics and insights
- **💭 Sentiment Analysis**: Community mood analysis
- **🔎 Keyword Search**: Multi-subreddit content search
- **☁️ Word Cloud**: Text visualization
- **⚙️ Settings**: Configuration and preferences

### Example Workflows

#### 1. **Discovering Communities**
1. Go to "🔍 Subreddit Finder"
2. Search for topics like "machine learning" or "startup"
3. Explore results and subscriber counts
4. Click "Analyze" for detailed insights

#### 2. **Analyzing Trends**
1. Go to "📈 Trending Discussions"
2. Enter a subreddit name (e.g., "technology")
3. Select time period (day, week, month)
4. View engagement patterns and trending topics

#### 3. **Sentiment Analysis**
1. Go to "💭 Sentiment Analysis"
2. Enter a subreddit (e.g., "politics", "cryptocurrency")
3. View positive/negative/neutral distribution
4. Review sample texts with sentiment scores

#### 4. **Cross-Subreddit Search**
1. Go to "🔎 Keyword Search"
2. Enter keywords (one per line)
3. Enter target subreddits (one per line)
4. Find relevant discussions across communities

## Configuration

### Environment Variables

The application supports the following environment variables:

```bash
# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=RedditScoutPro/1.0

# Content Filtering
MIN_SCORE_THRESHOLD=5
MIN_COMMENTS_THRESHOLD=3
EXCLUDE_NSFW=true
EXCLUDE_SPOILERS=true

# Analytics
SENTIMENT_ANALYSIS_ENABLED=true
WORDCLOUD_ENABLED=true
ENGAGEMENT_METRICS_ENABLED=true

# Defaults
DEFAULT_SUBREDDITS=python,programming,technology
DEFAULT_TIME_FILTER=week
MAX_POSTS_PER_REQUEST=100
```

### Settings Page

Use the "⚙️ Settings" page in the dashboard to:
- Test Reddit API connection
- Configure content filtering
- Set analytics preferences
- Manage default subreddits

## API Rate Limiting

The application respects Reddit's API rate limits:
- 60 requests per minute (default)
- Automatic request delays
- Error handling for rate limit issues

## Features in Detail

### Subreddit Analytics
- **Engagement Metrics**: Average scores, comments, upvote ratios
- **User Activity**: Top authors and posting patterns
- **Content Distribution**: Self-posts vs. external links
- **Time Patterns**: Activity by hour of day
- **Engagement Levels**: High/medium/low categorization

### Sentiment Analysis
- **TextBlob Integration**: Polarity-based sentiment scoring
- **Community Mood**: Overall positive/negative trends
- **Sample Analysis**: Representative text examples
- **Score Correlation**: Sentiment vs. post engagement

### Word Cloud & Text Analysis
- **Frequency Analysis**: Most common words and phrases
- **Vocabulary Diversity**: Unique word ratios
- **Content Filtering**: Minimum word length filtering
- **Text Preprocessing**: Cleaned and normalized text

## Development

### Project Structure
```
Reddit Scout Pro/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── reddit_scout.py    # Reddit API client and data processing
│   └── dashboard.py       # Streamlit interface
├── app.py                 # Main entry point
├── pyproject.toml         # Poetry dependencies
└── README.md             # This file
```

### Dependencies

- **streamlit**: Web dashboard framework
- **praw**: Python Reddit API Wrapper
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **textblob**: Natural language processing
- **langdetect**: Language detection
- **wordcloud**: Word cloud generation
- **pydantic**: Configuration validation

## Troubleshooting

### Common Issues

1. **Reddit API Connection Failed**
   - Verify client ID and secret in `.env` file
   - Check Reddit app configuration
   - Ensure user agent is properly set

2. **No Data Retrieved**
   - Check subreddit names for typos
   - Verify subreddit exists and is public
   - Check content filters (NSFW, score thresholds)

3. **Slow Performance**
   - Reduce the number of posts to analyze
   - Check internet connection
   - Verify API rate limits aren't exceeded

4. **Import Errors**
   - Ensure all dependencies are installed
   - Verify Python version (3.11+ required)
   - Check virtual environment activation

### Error Messages

- **"Failed to connect to Reddit API"**: Check credentials
- **"No discussions found"**: Verify subreddit name and filters
- **"Rate limit exceeded"**: Wait and retry, reduce request frequency

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🚀 Deployment

### **Quick Deploy to Streamlit Cloud (FREE):**
1. Push this repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file: `app.py`
5. Add Reddit API credentials to Streamlit secrets
6. Deploy!

**📖 Detailed deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

### **Files for Deployment:**
- `requirements_deployment.txt` - Production dependencies
- `.streamlit/config.toml` - Streamlit configuration  
- `env.example` - Environment variables template
- `DEPLOYMENT.md` - Complete deployment guide

## Project Structure

```
Reddit Scout Pro/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── reddit_scout.py        # Reddit API client and data processing
│   └── dashboard.py           # Streamlit interface
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── app.py                    # Main entry point
├── start.sh                  # Easy startup script
├── setup_alias.sh           # Setup 'reddit-scout' command
├── requirements_deployment.txt # Production dependencies
├── pyproject.toml           # Poetry dependencies
├── DEPLOYMENT.md            # Deployment guide
└── README.md               # This file
```

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review Reddit API documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

---

**Happy Reddit Exploring! 🔍📊💭**
**Ready to deploy? Check [DEPLOYMENT.md](DEPLOYMENT.md)! 🚀** 