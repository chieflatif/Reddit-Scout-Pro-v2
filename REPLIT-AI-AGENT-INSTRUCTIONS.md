# 🤖 Replit AI Agent Deployment Instructions

## 📋 Clear Step-by-Step Guide for Reddit Scout Pro Community Edition

### **STEP 1: Verify File Structure**
Check that these key files exist in your project root:
```
main.py
app_multi_user.py
requirements_multi_user.txt
src/
```

**Command to verify:**
```bash
ls -la main.py app_multi_user.py requirements_multi_user.txt src/
```

### **STEP 2: Install Dependencies**
Install all required Python packages:
```bash
pip install -r requirements_multi_user.txt
```

**Wait for this to complete** - it will install about 20+ packages including:
- streamlit (web framework)
- sqlalchemy (database)
- bcrypt (password hashing)
- cryptography (encryption)
- praw (Reddit API)

### **STEP 3: Enable PostgreSQL Database**
1. Click **"Tools"** in the left sidebar
2. Click **"Database"**
3. Click **"Enable PostgreSQL"**
4. Wait 30-60 seconds for setup to complete
5. You should see "PostgreSQL enabled" message

### **STEP 4: Configure Environment Variables**
1. Click **"Tools"** in the left sidebar
2. Click **"Secrets"** (lock icon 🔒)
3. Add these secrets:

**Secret 1:**
- Key: `SECRET_KEY`
- Value: `reddit-scout-pro-community-secret-key-2024`

**Secret 2 (Optional for debugging):**
- Key: `DEBUG`
- Value: `true`

**Note:** `ENCRYPTION_KEY` will be auto-generated on first run

### **STEP 5: Set Main Entry Point**
Ensure Replit knows which file to run:
1. Check that `main.py` exists in root directory
2. If Replit asks for entry point, specify: `main.py`

### **STEP 6: Run the Application**
1. Click the big green **"Run"** button at the top
2. **Wait 2-3 minutes** for:
   - Dependencies to install
   - Database tables to be created
   - Encryption keys to be generated
   - Streamlit server to start

### **STEP 7: Check Console Output**
Look for these SUCCESS messages in the console:
```
Requirements installed successfully
Database initialized with URL: postgresql://***
Database tables created successfully
Generated new encryption key: [SOME_KEY]
Application initialized successfully
```

**If you see an ENCRYPTION_KEY in the console:**
1. Copy the key shown
2. Go to Tools → Secrets
3. Add new secret:
   - Key: `ENCRYPTION_KEY`
   - Value: [paste the key from console]
4. Restart the application

### **STEP 8: Open the Web Application**
1. Look for a URL in the console like: `http://localhost:8501`
2. Click **"Open in new tab"** button
3. Or copy the public Repl URL (looks like: `https://your-repl-name.yourname.repl.co`)

### **STEP 9: Test the Application**
1. **Registration Test:**
   - Click "Create Account"
   - Fill in: username, email, password
   - Click "Create Account"
   - Should see "Account created successfully!"

2. **Login Test:**
   - Use the credentials you just created
   - Should see welcome message and dashboard

3. **API Keys Page:**
   - Navigate to "API Keys" in the sidebar
   - Should see the API key configuration form

### **STEP 10: Configure Reddit API Keys (For Testing)**
To fully test the application:

1. **Get Reddit API Keys:**
   - Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
   - Click "Create App"
   - Name: "Test App"
   - Type: **"script"** (important!)
   - Redirect URI: `http://localhost:8080`
   - Click "Create app"

2. **Copy Credentials:**
   - Client ID: Short string under "personal use script"
   - Client Secret: Long "secret" string

3. **Add to Application:**
   - In Reddit Scout Pro, go to "API Keys" page
   - Paste Client ID and Client Secret
   - Click "Save & Test API Keys"
   - Should see "API keys saved and validated successfully!"

## ✅ Success Checklist

After deployment, verify these work:
- [ ] Application loads without errors
- [ ] User registration works
- [ ] Login/logout functions
- [ ] Database connection is established
- [ ] Encryption system is working
- [ ] API Keys page loads
- [ ] Reddit API connection test passes (if keys configured)

## 🚨 Common Issues and Solutions

### **Issue: "Database initialization failed"**
**Solution:**
```bash
# Check if PostgreSQL is enabled
echo $DATABASE_URL
# Should show a postgresql:// URL
# If empty, enable PostgreSQL in Tools → Database
```

### **Issue: "Encryption system test failed"**
**Solution:**
1. Check console for generated ENCRYPTION_KEY
2. Add it to Replit Secrets
3. Restart the application

### **Issue: "Module not found" errors**
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements_multi_user.txt
# Restart the application
```

### **Issue: "Permission denied" or import errors**
**Solution:**
```bash
# Check file structure
ls -la
# Ensure main.py is in root directory
# Ensure src/ directory exists with all modules
```

### **Issue: Application won't start**
**Solution:**
1. Check console for error messages
2. Ensure all files are in root directory (not in subdirectory)
3. Verify main.py exists
4. Restart the Repl completely

## 🔧 Debugging Commands

If something goes wrong, run these diagnostic commands:

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(streamlit|sqlalchemy|bcrypt|praw)"

# Check file structure
find . -name "*.py" | head -10

# Test database connection
python -c "import os; print('DB URL:', os.getenv('DATABASE_URL', 'Not set'))"

# Run the test script
python test_setup.py
```

## 🎯 Final Verification

When everything is working, you should be able to:
1. **Access the app** at your Repl's public URL
2. **Create user accounts** and log in
3. **Navigate between pages** (Dashboard, API Keys, etc.)
4. **Configure Reddit API keys** and test connection
5. **See no errors** in the console

## 📞 If You Need Help

**Check these in order:**
1. **Console logs** - look for error messages
2. **Database status** - ensure PostgreSQL is enabled
3. **Secrets** - verify SECRET_KEY is set
4. **File structure** - ensure all files are in correct locations
5. **Restart** - try restarting the entire Repl

## 🚀 Going Live

Once everything is working:
1. **Enable Always-On** (if you have paid Replit plan)
2. **Share your Repl URL** with your community
3. **Users can register** and add their own Reddit API keys
4. **Each user gets isolated** Reddit analytics experience

---

**🎉 That's it! Your Reddit Scout Pro Community Edition should now be running successfully on Replit!**
