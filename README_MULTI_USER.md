# 🔍 Reddit Scout Pro - Community Edition

A powerful multi-user Reddit analytics platform with secure authentication and personal API key management.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-ready-brightgreen)

## 🎯 What's New in Community Edition

### 🔐 **Multi-User Authentication**
- Secure user registration and login
- Password hashing with bcrypt
- Session management with automatic expiration
- Personal user profiles and preferences

### 🔑 **Personal API Key Management**
- Each user manages their own Reddit API keys
- Encrypted storage using Fernet encryption
- Easy API key setup with guided instructions
- Secure key validation and testing

### 🏢 **Community Ready**
- Host for your entire community on Replit
- Users create their own accounts
- Isolated data per user
- No complex billing or enterprise features

### 🚀 **Easy Deployment**
- Optimized for Replit hosting
- Built-in PostgreSQL database support
- Environment variable configuration
- One-click deployment

## 📋 Features

### 🔍 **Reddit Analytics** (Same as Original)
- Subreddit discovery and search
- Active discussion tracking
- Trending topic analysis
- Sentiment analysis
- Word cloud generation
- Multi-subreddit search
- Engagement metrics

### 🆕 **New Community Features**
- User dashboard with personal stats
- API key management interface
- Session management and security
- User preferences and settings
- Secure multi-tenant architecture

## 🚀 Quick Start

### For Replit (Recommended)

1. **Import to Replit**:
   ```
   1. Go to replit.com
   2. Click "Create Repl" → "Import from GitHub"
   3. Enter: https://github.com/yourusername/reddit-scout-pro
   4. Click "Import from GitHub"
   ```

2. **Enable Database**:
   ```
   1. Tools → Database
   2. Enable PostgreSQL
   3. Wait for setup completion
   ```

3. **Configure Secrets**:
   ```
   1. Tools → Secrets
   2. Add: SECRET_KEY = your-secret-key-here
   3. Add: ENCRYPTION_KEY = (will be generated automatically)
   ```

4. **Run the App**:
   ```
   1. Click "Run"
   2. Wait for dependencies to install
   3. Open the provided URL
   ```

5. **Create Your Account**:
   ```
   1. Click "Create Account"
   2. Fill in your details
   3. Configure Reddit API keys
   4. Start exploring!
   ```

### For Local Development

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/reddit-scout-pro.git
   cd reddit-scout-pro
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements_multi_user.txt
   ```

3. **Setup Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize Database**:
   ```bash
   python test_setup.py  # Test setup
   python main.py        # Run application
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `SECRET_KEY` | ✅ | Session encryption key | `your-super-secret-key` |
| `ENCRYPTION_KEY` | ⚠️ | API key encryption (auto-generated) | Auto-generated Fernet key |
| `DEBUG` | ❌ | Enable debug mode | `true` or `false` |

### Reddit API Setup (Per User)

Each user needs their own Reddit API keys:

1. **Go to Reddit Apps**: [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. **Create New App**:
   - Name: "My Reddit Scout"
   - Type: **"script"**
   - Redirect URI: `http://localhost:8080`
3. **Get Credentials**:
   - Client ID: Short string under "personal use script"
   - Client Secret: Long "secret" string
4. **Add to App**: Use the "API Keys" page in Reddit Scout Pro

## 🏗️ Architecture

### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- API keys table (encrypted)
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    reddit_client_id VARCHAR(255),
    reddit_client_secret_encrypted TEXT,
    reddit_user_agent VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sessions table
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Security Features
- 🔒 **Password Hashing**: bcrypt with salt rounds
- 🔐 **API Key Encryption**: Fernet symmetric encryption
- 🎫 **Session Management**: Secure token-based sessions
- 🛡️ **Input Validation**: Comprehensive validation for all inputs
- 🔍 **SQL Injection Protection**: SQLAlchemy ORM
- 👤 **Data Isolation**: Each user sees only their own data

## 📁 Project Structure

```
Reddit-Scout-Pro-Community/
├── main.py                      # Replit entry point
├── app_multi_user.py           # Main application
├── requirements_multi_user.txt  # Dependencies
├── src/
│   ├── database/
│   │   ├── models.py           # Database models
│   │   └── database.py         # Database connection
│   ├── auth/
│   │   ├── auth_manager.py     # Authentication logic
│   │   └── decorators.py       # Auth decorators
│   ├── core/
│   │   ├── encryption.py       # API key encryption
│   │   └── reddit_scout_multi.py # Multi-user Reddit client
│   └── ui/
│       └── pages/
│           ├── login.py        # Login/registration
│           └── api_keys.py     # API key management
├── test_setup.py               # Setup verification
├── REPLIT-SETUP.md            # Replit deployment guide
└── README_MULTI_USER.md       # This file
```

## 🧪 Testing

### Run Setup Tests
```bash
python test_setup.py
```

This will test:
- ✅ Database connection and models
- ✅ Encryption system
- ✅ Authentication system
- ✅ Reddit client initialization
- ✅ Environment configuration

### Manual Testing
1. **User Registration**: Create a test account
2. **Login/Logout**: Test authentication flow
3. **API Keys**: Add and validate Reddit API keys
4. **Reddit Features**: Test subreddit search and data retrieval

## 🚀 Deployment Options

### 1. Replit (Recommended for Communities)
- ✅ **Pros**: Easy setup, built-in database, community sharing
- ✅ **Cost**: $20/month for always-on hosting
- ✅ **Users**: 20-50 concurrent users
- 📖 **Guide**: See [REPLIT-SETUP.md](REPLIT-SETUP.md)

### 2. Render.com (Cost Optimized)
- ✅ **Pros**: Lower cost, better scaling, production-focused
- ✅ **Cost**: $7-14/month
- ✅ **Users**: 50-100+ concurrent users
- 📖 **Guide**: See [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)

### 3. Local/Self-Hosted
- ✅ **Pros**: Full control, no monthly costs
- ❌ **Cons**: Requires technical setup
- 📖 **Guide**: Standard Python deployment

## 👥 Community Usage

### For Community Owners
1. **Deploy**: Set up on Replit or Render.com
2. **Share**: Give members your app URL
3. **Support**: Help users with Reddit API setup
4. **Monitor**: Keep an eye on resource usage

### For Community Members
1. **Register**: Create your personal account
2. **API Keys**: Add your Reddit API credentials
3. **Explore**: Use all Reddit analytics features
4. **Privacy**: Your data stays private and isolated

## 🔒 Privacy & Security

### What We Store
- ✅ **User Accounts**: Username, email (hashed password)
- ✅ **API Keys**: Encrypted Reddit credentials
- ✅ **Sessions**: Temporary login tokens
- ✅ **Preferences**: User settings and preferences

### What We DON'T Store
- ❌ **Reddit Data**: No posts, comments, or personal Reddit info
- ❌ **Browsing History**: No tracking of your Reddit exploration
- ❌ **API Responses**: Data is processed in real-time only
- ❌ **Personal Info**: Only what you provide during registration

### Data Control
- 🔧 **Update**: Change your API keys anytime
- 🗑️ **Delete**: Remove your account and all data
- 🔒 **Isolate**: Your data is completely separate from other users
- 🛡️ **Encrypt**: API keys are encrypted with industry-standard methods

## 🛠️ Troubleshooting

### Common Issues

#### "Database initialization failed"
```bash
# Solution:
1. Ensure PostgreSQL is enabled (Replit: Tools → Database)
2. Check DATABASE_URL environment variable
3. Restart the application
```

#### "Encryption system test failed"
```bash
# Solution:
1. Check console for generated ENCRYPTION_KEY
2. Add the key to your environment variables
3. Restart the application
```

#### "Invalid Reddit API credentials"
```bash
# Solution:
1. Verify Client ID and Secret are correct
2. Ensure app type is "script" in Reddit
3. Check that redirect URI is set to http://localhost:8080
```

#### "Session expired" errors
```bash
# Solution:
1. This is normal after 7 days of inactivity
2. Simply log in again
3. Sessions automatically clean up expired tokens
```

### Getting Help
1. **Check Logs**: Look at console output for errors
2. **Run Tests**: Use `python test_setup.py` to diagnose issues
3. **Enable Debug**: Set `DEBUG=true` for detailed logging
4. **Restart**: Try restarting the application

## 🔄 Migration from Single-User Version

### Automatic Migration
The multi-user version is a complete rewrite, so migration requires:

1. **Export Data**: Save any important Reddit data from the original
2. **Deploy New Version**: Set up the community edition
3. **Create Accounts**: Users register new accounts
4. **Configure API**: Users add their Reddit API keys
5. **Resume Usage**: All original features available

### No Data Loss
- Reddit data isn't stored permanently in either version
- Users just need to reconfigure their API keys
- All analytics features work identically

## 🚀 Future Enhancements

### Planned Features
- 📊 **User Analytics**: Personal usage statistics
- 🔔 **Notifications**: Alert users to trending topics
- 📱 **Mobile UI**: Responsive design improvements
- 🎨 **Themes**: Dark mode and custom themes
- 📈 **Advanced Analytics**: More sophisticated Reddit analysis

### Community Requests
- 💬 **Comments**: Submit feature requests as GitHub issues
- 🗳️ **Voting**: Community votes on priority features
- 🤝 **Contributions**: Open to community contributions

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📞 Support

### For Users
- 📖 **Documentation**: Check this README and setup guides
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Community**: Ask questions in GitHub Discussions

### For Developers
- 🔧 **API**: Well-documented code with type hints
- 🧪 **Tests**: Comprehensive test suite
- 📋 **Architecture**: Clear separation of concerns

---

## 🎉 Ready to Start?

1. **Deploy** on Replit using [REPLIT-SETUP.md](REPLIT-SETUP.md)
2. **Share** with your community
3. **Explore** Reddit data like never before!

**Built with ❤️ for the Reddit community** 🚀
