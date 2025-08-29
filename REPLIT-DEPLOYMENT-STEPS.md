# 🚀 Replit Deployment Steps - Reddit Scout Pro Community Edition

## 📦 Files Ready!
Your `reddit-scout-pro-community.zip` file contains all the necessary code for deployment.

## 🎯 Step-by-Step Deployment

### **Step 1: Create Replit Project (2 minutes)**
1. **Go to**: [replit.com](https://replit.com)
2. **Sign in** to your account
3. **Create Repl**:
   - Click "Create Repl"
   - Select "Python" template
   - Name: `reddit-scout-pro-community`
   - Click "Create Repl"

### **Step 2: Upload Files (3 minutes)**
1. **Delete default files**: Remove `main.py` if it exists
2. **Upload zip file**:
   - Drag `reddit-scout-pro-community.zip` into the file panel
   - Or click "Upload file" and select the zip
3. **Extract files**:
   - Right-click the zip file
   - Select "Extract All" or "Unzip"
4. **Move files**: Move all extracted files to the root directory

### **Step 3: Enable Database (1 minute)**
1. **Open Tools**: Click "Tools" in the left sidebar
2. **Database**: Click "Database" 
3. **Enable PostgreSQL**: Click "Enable PostgreSQL"
4. **Wait**: Let Replit set up the database (30 seconds)

### **Step 4: Configure Secrets (2 minutes)**
1. **Open Secrets**: Click "Tools" → "Secrets" (🔒 icon)
2. **Add Secret**:
   - Key: `SECRET_KEY`
   - Value: `reddit-scout-pro-secret-key-2024-community-edition`
3. **Optional Debug**:
   - Key: `DEBUG`
   - Value: `true`

**Note**: `ENCRYPTION_KEY` will be auto-generated on first run

### **Step 5: Run the Application (2 minutes)**
1. **Click "Run"**: The big green "Run" button at the top
2. **Wait for install**: Dependencies will install automatically (1-2 minutes)
3. **Check console**: Look for success messages
4. **Open app**: Click "Open in new tab" when ready

### **Step 6: Create Your Account (1 minute)**
1. **Open the app**: Click the URL provided by Replit
2. **Create Account**: Click "Create Account"
3. **Fill details**:
   - Username: `admin` (or your preferred username)
   - Email: Your email address
   - Password: Strong password
4. **Register**: Click "Create Account"

### **Step 7: Configure Reddit API Keys (5 minutes)**
1. **Get Reddit API Keys**:
   - Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Name: "Reddit Scout Pro Community"
   - Type: **"script"** (important!)
   - Redirect URI: `http://localhost:8080`
   - Click "Create app"

2. **Copy Credentials**:
   - **Client ID**: Short string under "personal use script"
   - **Client Secret**: Long "secret" string

3. **Add to App**:
   - In Reddit Scout Pro, go to "API Keys" page
   - Paste your Client ID and Client Secret
   - Click "Save & Test API Keys"
   - Wait for validation ✅

### **Step 8: Test Everything (2 minutes)**
1. **Test Connection**: Click "Test Reddit Connection" 
2. **Explore Features**: Try "Subreddit Finder" or "Active Discussions"
3. **Share with Community**: Copy your Repl URL to share

## ✅ Success Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] User registration works
- [ ] Login/logout functions
- [ ] API key setup page loads
- [ ] Reddit connection test passes
- [ ] Database tables are created
- [ ] Can explore Reddit data

## 🎉 You're Live!

### Your Community App URL:
```
https://reddit-scout-pro-community.yourname.repl.co
```

### Share with Your Community:
1. **Send them the URL**
2. **They create their own accounts**
3. **They add their own Reddit API keys**
4. **Everyone gets personalized Reddit analytics!**

## 🔧 Troubleshooting

### "Database initialization failed"
- Ensure PostgreSQL is enabled in Tools → Database
- Restart the Repl

### "Encryption system test failed"
- Check console for generated ENCRYPTION_KEY
- Add it to Secrets if shown
- Restart the application

### "Requirements installation failed"
- Check internet connection
- Restart the Repl
- Try running manually: `pip install -r requirements_multi_user.txt`

### App won't start
- Check console for error messages
- Ensure all files are in the root directory
- Verify `main.py` exists
- Restart the Repl

## 🎯 Next Steps

1. **Test thoroughly** with your own account
2. **Create a few test users** to verify isolation
3. **Share with your community** when ready
4. **Monitor usage** and performance
5. **Upgrade to paid tier** if needed for always-on hosting

## 📞 Need Help?

- **Console Logs**: Check the console for error messages
- **Test Script**: Run `python test_setup.py` for diagnostics
- **Restart**: Try restarting the Repl as first troubleshooting step

---

**🚀 Ready to deploy? You've got this!** 

Your Reddit Scout Pro Community Edition is ready to serve your community with secure, multi-user Reddit analytics! 🎉
