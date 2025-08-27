# Reddit API Credentials Setup Guide

## The Issue
Your Reddit Explorer is not fetching results because it needs Reddit API credentials to access Reddit's data.

## How to Get Reddit API Credentials

### Step 1: Create a Reddit App
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **Name**: `Reddit Explorer` (or any name you prefer)
   - **App type**: Select "script"
   - **Description**: `Personal Reddit data explorer` (optional)
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8080` (required but not used)
4. Click "Create app"

### Step 2: Get Your Credentials
After creating the app, you'll see:
- **Client ID**: The string under the app name (14 characters)
- **Client Secret**: The longer string labeled "secret"

### Step 3: Create .env File
Create a file named `.env` in your project root with:

```env
# Reddit API Configuration - REQUIRED
REDDIT_CLIENT_ID=your_14_character_client_id
REDDIT_CLIENT_SECRET=your_longer_client_secret
REDDIT_USER_AGENT=RedditExplorer/1.0
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# Optional: Content Settings
DEFAULT_SUBREDDITS=python,programming,technology,startups
MAX_POSTS_PER_REQUEST=100
MIN_SCORE_THRESHOLD=5
EXCLUDE_NSFW=true
```

### Step 4: Restart the App
After creating the `.env` file:
1. Stop the current app (Ctrl+C in terminal)
2. Run: `poetry run streamlit run app.py`
3. The app should now fetch Reddit data successfully!

## Security Note
- Never share your `.env` file or commit it to version control
- These credentials are personal and tied to your Reddit account
- The app only reads public Reddit data - it cannot post or modify content

## Troubleshooting
- Make sure `.env` is in the same directory as `app.py`
- Check that your Reddit username/password are correct
- Ensure your Reddit account is verified (email confirmed) 