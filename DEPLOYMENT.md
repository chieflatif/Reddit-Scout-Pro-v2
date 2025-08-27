# 🚀 Reddit Scout Pro - Deployment Guide

## 📋 Quick Deployment Options

### 🏆 **Recommended: Streamlit Community Cloud (FREE)**

**Pros:** ✅ Free, Easy, Integrated with GitHub, Automatic updates
**Cons:** ⚠️ Public repository required, Limited resources

**Steps:**
1. **Push to GitHub:** Your code needs to be in a public GitHub repository
2. **Visit:** [share.streamlit.io](https://share.streamlit.io)
3. **Connect GitHub:** Link your GitHub account
4. **Deploy:** Select your repository and `app.py`
5. **Add Secrets:** Configure Reddit API credentials in Streamlit secrets

### 🐙 **Alternative: Heroku**

**Pros:** ✅ Reliable, Custom domains, Private repos
**Cons:** ⚠️ Paid (starts ~$5/month)

### 🐋 **Advanced: Railway/Render**

**Pros:** ✅ Modern, Fast, Good free tier
**Cons:** ⚠️ Newer platforms

---

## 🔧 Pre-Deployment Checklist

### ✅ **Files Ready:**
- [x] `app.py` - Main application
- [x] `requirements_deployment.txt` - Dependencies  
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `env.example` - Environment variables template
- [x] `README.md` - Updated documentation

### ✅ **Reddit API Setup:**
1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Create new app (script type)
3. Note your Client ID and Secret
4. Set redirect URI: `http://localhost:8080` (for local) or your domain

---

## 🌐 **Streamlit Cloud Deployment (Detailed)**

### **Step 1: Prepare Repository**
```bash
# Commit all changes
git add .
git commit -m "🚀 Prepare for deployment"
git push origin main
```

### **Step 2: Deploy on Streamlit Cloud**
1. **Visit:** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **New app** → Select your repository
4. **Main file path:** `app.py`
5. **Advanced settings:**
   - Python version: `3.11`
   - Requirements file: `requirements_deployment.txt`

### **Step 3: Configure Secrets**
In Streamlit Cloud dashboard → **Settings** → **Secrets**:

```toml
# Add this to your Streamlit secrets
[default]
REDDIT_CLIENT_ID = "your_client_id_here"
REDDIT_CLIENT_SECRET = "your_client_secret_here"
REDDIT_USER_AGENT = "RedditScoutPro/1.0"

# Optional
REDDIT_USERNAME = "your_username"
REDDIT_PASSWORD = "your_password"

# App Configuration
ENVIRONMENT = "production"
DEBUG = false
MIN_SCORE_THRESHOLD = 5
MIN_COMMENTS_THRESHOLD = 3
```

### **Step 4: Deploy!**
- Click **Deploy**
- Wait 2-5 minutes
- Your app will be live at `https://yourapp-randomid.streamlit.app`

---

## 🐋 **Alternative: Railway Deployment**

### **Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli
railway login
```

### **Step 2: Deploy**
```bash
# In your project directory
railway deploy
```

### **Step 3: Configure Environment**
```bash
railway variables set REDDIT_CLIENT_ID=your_id
railway variables set REDDIT_CLIENT_SECRET=your_secret
# ... add other variables
```

---

## 🔐 **Environment Variables Guide**

### **Required:**
- `REDDIT_CLIENT_ID` - From Reddit app
- `REDDIT_CLIENT_SECRET` - From Reddit app
- `REDDIT_USER_AGENT` - App identifier

### **Optional:**
- `REDDIT_USERNAME` - For enhanced API access
- `REDDIT_PASSWORD` - For authenticated requests
- `MIN_SCORE_THRESHOLD` - Filter posts by score (default: 5)
- `MIN_COMMENTS_THRESHOLD` - Filter posts by comments (default: 3)

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. Import Errors**
```
ModuleNotFoundError: No module named 'X'
```
**Solution:** Check `requirements_deployment.txt` includes all dependencies

#### **2. Reddit API Issues**
```
prawcore.exceptions.ResponseException: received 401 HTTP response
```
**Solution:** Verify Reddit API credentials in secrets/environment

#### **3. Memory Issues**
```
MemoryError: Unable to allocate array
```
**Solution:** Reduce `MAX_POSTS_PER_REQUEST` in environment variables

#### **4. Timeout Issues**
**Solution:** 
- Use Global Search with lower limits (25-50 results)
- Disable "Include country-focused search" for faster results

---

## 📊 **Performance Optimization for Production**

### **1. Optimize Search Settings:**
```python
# In production, use these settings:
MAX_POSTS_PER_REQUEST = 50  # Instead of 100
DEFAULT_TIME_FILTER = "week"  # Instead of "all"
SEARCH_COMMENTS = False  # For faster searches
```

### **2. Caching Strategy:**
- Results are cached in `st.session_state`
- Consider adding `@st.cache_data` for expensive operations
- Clear cache periodically to manage memory

### **3. Rate Limiting:**
- Reddit API: 60 requests/minute
- App handles this automatically
- Monitor usage in production

---

## 🎯 **Post-Deployment**

### **✅ Test Core Features:**
1. **🔍 Subreddit Search** - Find communities
2. **🔥 Active Discussions** - Hot topics
3. **🌐 Global Search** - Cross-Reddit search
4. **☁️ Word Cloud** - Text visualization
5. **💭 Sentiment Analysis** - Community mood

### **📱 Share Your App:**
- Custom domain (Streamlit Pro)
- Social media promotion
- Add to portfolio
- GitHub stars ⭐

---

## 🔗 **Useful Links**

- **Streamlit Cloud:** [share.streamlit.io](https://share.streamlit.io)
- **Reddit API:** [reddit.com/dev/api](https://www.reddit.com/dev/api/)
- **Documentation:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community:** [discuss.streamlit.io](https://discuss.streamlit.io)

---

**🎉 Your Reddit Scout Pro is ready for the world!**
