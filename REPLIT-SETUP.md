# 🚀 Replit Setup Guide for Reddit Scout Pro Community Edition

## 📋 Quick Setup Checklist

### Step 1: Import to Replit (5 minutes)
1. **Create Replit Account**: Go to [replit.com](https://replit.com)
2. **Import from GitHub**: 
   - Click "Create Repl"
   - Select "Import from GitHub"
   - Enter your repository URL: `https://github.com/yourusername/reddit-scout-pro`
   - Click "Import from GitHub"

### Step 2: Enable PostgreSQL Database (2 minutes)
1. **Open Database Tab**: In your Repl, click on "Tools" → "Database"
2. **Enable PostgreSQL**: Click "Enable PostgreSQL"
3. **Wait for Setup**: Replit will automatically configure the database

### Step 3: Configure Environment Variables (5 minutes)
1. **Open Secrets**: Click on "Tools" → "Secrets" (🔒 icon)
2. **Add Required Secrets**:

```bash
# Required Secrets to Add:
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ENCRYPTION_KEY=fernet-encryption-key-will-be-generated-automatically

# Optional (for debugging):
DEBUG=true
```

**To generate a SECRET_KEY:**
- Use any long random string (32+ characters)
- Example: `my-super-secret-reddit-scout-key-2024`

**ENCRYPTION_KEY:**
- Will be auto-generated on first run
- Check the console output for the generated key
- Add it to Secrets to persist across restarts

### Step 4: Run the Application (2 minutes)
1. **Click "Run"**: The green "Run" button at the top
2. **Wait for Installation**: First run will install all dependencies
3. **Open Web View**: Click "Open in new tab" when the app starts

## 🔧 Detailed Configuration

### Database Configuration
Replit automatically provides these environment variables when PostgreSQL is enabled:
- `DATABASE_URL` - Complete connection string
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS` - Individual components

**No additional database setup required!**

### File Structure After Setup
```
your-repl/
├── main.py                    # Replit entry point
├── app_multi_user.py         # Main application
├── requirements_multi_user.txt # Dependencies
├── src/
│   ├── auth/                 # Authentication system
│   ├── database/             # Database models
│   ├── core/                 # Reddit API client
│   └── ui/                   # Streamlit pages
├── REPLIT-SETUP.md          # This file
└── README.md                # Original documentation
```

### Environment Variables Explained

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `SECRET_KEY` | ✅ Yes | Session security | `my-secret-key-123` |
| `ENCRYPTION_KEY` | ⚠️ Auto | API key encryption | Auto-generated |
| `DATABASE_URL` | ✅ Auto | PostgreSQL connection | Auto-provided by Replit |
| `DEBUG` | ❌ Optional | Development mode | `true` or `false` |

## 🚀 First Run Process

### What Happens on First Run:
1. **Dependencies Install**: All Python packages are installed
2. **Database Tables Created**: User, API keys, sessions tables
3. **Encryption Key Generated**: If not provided in Secrets
4. **Application Starts**: Streamlit server launches

### Expected Console Output:
```
Installing requirements...
Requirements installed successfully
Database initialized with URL: postgresql://***
Database tables created successfully
Generated new encryption key: [KEY_HERE]
Add this to your Replit Secrets as ENCRYPTION_KEY

Application initialized successfully
You can now view your Streamlit app in your browser.
```

## 👥 User Registration Flow

### For the First User (You):
1. **Access the App**: Click "Open in new tab"
2. **Create Account**: Click "Create Account"
3. **Fill Registration**: Username, email, password
4. **Auto-Login**: You'll be logged in automatically
5. **Configure Reddit API**: Add your Reddit API keys

### For Community Members:
1. **Share Your Repl URL**: Give them your Repl's public URL
2. **They Register**: Each user creates their own account
3. **They Configure API**: Each user adds their own Reddit API keys
4. **Independent Usage**: Each user has their own isolated experience

## 🔑 Reddit API Keys Setup

### Each User Needs Their Own Keys:
1. **Go to Reddit**: [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. **Create App**: 
   - Name: "My Reddit Scout"
   - Type: "script"
   - Redirect URI: `http://localhost:8080`
3. **Get Credentials**:
   - Client ID: Short string under "personal use script"
   - Client Secret: Long "secret" string
4. **Add to App**: Use the "API Keys" page in Reddit Scout Pro

## 🔒 Security Features

### Built-in Security:
- ✅ **Password Hashing**: bcrypt with salt
- ✅ **API Key Encryption**: Fernet symmetric encryption
- ✅ **Session Management**: Secure token-based sessions
- ✅ **Input Validation**: Email, username, password validation
- ✅ **SQL Injection Protection**: SQLAlchemy ORM

### User Data Isolation:
- Each user sees only their own data
- API keys are encrypted per-user
- Sessions are isolated
- No cross-user data leakage

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "Database initialization failed"
**Solution:**
- Ensure PostgreSQL is enabled in Tools → Database
- Check that DATABASE_URL is automatically set
- Restart the Repl

#### 2. "Encryption system test failed"
**Solution:**
- Check console for generated ENCRYPTION_KEY
- Add the key to Replit Secrets
- Restart the application

#### 3. "Requirements installation failed"
**Solution:**
- Check internet connection
- Clear pip cache: `pip cache purge`
- Restart the Repl

#### 4. "Session expired" errors
**Solution:**
- This is normal after inactivity
- Users just need to log in again
- Sessions last 7 days by default

### Getting Help:
1. **Check Console**: Look for error messages in the console
2. **Enable Debug**: Set `DEBUG=true` in Secrets for detailed logs
3. **Restart Repl**: Sometimes a fresh start helps
4. **Check Database**: Ensure PostgreSQL is running

## 📊 Monitoring Your Community App

### User Management:
- No admin panel needed for small communities
- Users self-register and manage their accounts
- Each user is independent

### Resource Usage:
- **Free Tier**: Good for 10-20 concurrent users
- **Paid Tier**: Supports 50+ concurrent users
- **Database**: PostgreSQL free tier handles hundreds of users

### Scaling Considerations:
- Monitor Repl performance
- Consider upgrading to paid tier for larger communities
- Database should handle growth automatically

## 🎉 Success Checklist

After setup, verify these work:
- [ ] App loads without errors
- [ ] User registration works
- [ ] Login/logout functions
- [ ] API key configuration page loads
- [ ] Database tables are created
- [ ] Encryption system is working

## 🚀 Going Live

### Share with Your Community:
1. **Get Public URL**: Your Repl's URL (looks like `https://reddit-scout-pro.yourname.repl.co`)
2. **Enable Always-On**: Upgrade to paid tier for 24/7 availability
3. **Share Instructions**: Give users this setup guide
4. **Monitor Usage**: Watch for performance or issues

### Optional Enhancements:
- **Custom Domain**: Point your domain to the Repl
- **Analytics**: Monitor user registrations and usage
- **Backups**: Export database periodically

## 📞 Support

### For Technical Issues:
- Check the troubleshooting section above
- Review console logs for errors
- Restart the Repl as first step

### For Feature Requests:
- This is the community edition
- Core features are implemented
- Advanced features can be added based on community needs

---

**🎉 You're all set!** Your Reddit Scout Pro community edition is ready to use. Share the URL with your community and let them start exploring Reddit data with their own personalized analytics! 🚀
