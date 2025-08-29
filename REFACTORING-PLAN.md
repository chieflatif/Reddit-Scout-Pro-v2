# 🚀 Reddit Scout Pro - Community Edition Refactoring Plan

## 📋 Project Overview
Transform Reddit Scout Pro into a multi-user community application hosted on Render.com with:
- User authentication (login/signup)
- Personal Reddit API key management
- Session management
- Secure API key storage
- Community-friendly features (no complex billing)

## 🏗️ Architecture Overview

### Current Architecture (Single-User)
```
app.py → dashboard.py → reddit_scout.py → Reddit API
         ↓
    config.py (.env file)
```

### New Architecture (Multi-User)
```
app.py → auth_manager.py → dashboard.py → reddit_scout.py → Reddit API
         ↓                  ↓              ↓
    database.py        session_manager   user_config
         ↓
    PostgreSQL/SQLite
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### API Keys Table
```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    reddit_client_id VARCHAR(255),
    reddit_client_secret_encrypted VARCHAR(255),
    reddit_user_agent VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Development Phases

### Phase 1: Backend Infrastructure (Week 1)
1. **Database Setup**
   - [ ] Choose database (PostgreSQL for Render or SQLite for simplicity)
   - [ ] Create database models with SQLAlchemy
   - [ ] Setup database migrations with Alembic
   - [ ] Create connection pooling

2. **Authentication System**
   - [ ] Implement user registration
   - [ ] Implement login/logout
   - [ ] Password hashing with bcrypt
   - [ ] Session management
   - [ ] Password reset functionality (optional)

3. **API Key Management**
   - [ ] Encrypted storage for Reddit API keys
   - [ ] API key validation
   - [ ] Per-user Reddit client initialization

### Phase 2: Frontend Updates (Week 1-2)
1. **Authentication UI**
   - [ ] Login page
   - [ ] Registration page
   - [ ] API key management page
   - [ ] User profile/settings page

2. **Session Management**
   - [ ] Streamlit session state integration
   - [ ] Auto-logout on inactivity
   - [ ] Remember me functionality

3. **Multi-User Support**
   - [ ] User-specific data isolation
   - [ ] Personalized dashboards
   - [ ] User preferences storage

### Phase 3: Security & Performance (Week 2)
1. **Security Enhancements**
   - [ ] Input validation
   - [ ] SQL injection prevention
   - [ ] XSS protection
   - [ ] Rate limiting per user
   - [ ] API key encryption/decryption

2. **Performance Optimization**
   - [ ] Caching layer (Redis optional)
   - [ ] Database query optimization
   - [ ] Lazy loading for heavy components

### Phase 4: Deployment (Week 2-3)
1. **Render.com Configuration**
   - [ ] Docker containerization
   - [ ] Environment variables setup
   - [ ] Database service configuration
   - [ ] Auto-deploy from GitHub

2. **Production Setup**
   - [ ] SSL/TLS configuration
   - [ ] Domain setup (optional)
   - [ ] Monitoring and logging
   - [ ] Backup strategy

## 📁 New File Structure

```
Reddit-Scout-Pro-Community/
├── src/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth_manager.py      # Authentication logic
│   │   ├── session_manager.py   # Session handling
│   │   └── decorators.py        # Auth decorators
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── database.py          # Database connection
│   │   └── migrations/          # Alembic migrations
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # App configuration
│   │   ├── reddit_scout.py      # Reddit API client (refactored)
│   │   └── encryption.py        # API key encryption
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── pages/
│   │   │   ├── login.py         # Login page
│   │   │   ├── register.py      # Registration page
│   │   │   ├── dashboard.py     # Main dashboard
│   │   │   ├── settings.py      # User settings
│   │   │   └── api_keys.py      # API key management
│   │   └── components/          # Reusable UI components
│   └── utils/
│       ├── __init__.py
│       ├── validators.py        # Input validation
│       └── helpers.py           # Utility functions
├── app.py                       # Main entry point
├── requirements.txt             # Dependencies
├── render.yaml                  # Render deployment config
├── Dockerfile                   # Docker configuration
├── .env.example                 # Environment template
└── README.md                    # Documentation
```

## 🔧 Key Code Changes

### 1. Authentication Manager (New)
```python
# src/auth/auth_manager.py
class AuthManager:
    - register_user(username, email, password)
    - login_user(username, password)
    - logout_user(session_token)
    - validate_session(session_token)
    - hash_password(password)
    - verify_password(password, hash)
```

### 2. Reddit Scout Refactor
```python
# src/core/reddit_scout.py
class RedditScout:
    def __init__(self, user_id):
        self.user_id = user_id
        self.api_keys = self.load_user_api_keys()
        self.reddit_client = self.initialize_reddit()
```

### 3. Session State Management
```python
# Streamlit session state structure
st.session_state = {
    'user_id': None,
    'username': None,
    'session_token': None,
    'reddit_scout': None,
    'authenticated': False
}
```

## 📦 New Dependencies

```txt
# Add to requirements.txt
sqlalchemy==2.0.23
alembic==1.13.0
bcrypt==4.1.2
cryptography==41.0.7
psycopg2-binary==2.9.9  # For PostgreSQL
python-jose==3.3.0      # For JWT tokens
email-validator==2.1.0
```

## 🚀 Render.com Deployment Configuration

### render.yaml
```yaml
services:
  - type: web
    name: reddit-scout-pro-community
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run app.py --server.port $PORT"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: reddit-scout-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ENCRYPTION_KEY
        generateValue: true

databases:
  - name: reddit-scout-db
    plan: free
    databaseName: reddit_scout
    user: reddit_scout_user
```

## 🔒 Security Considerations

1. **API Key Encryption**
   - Use Fernet symmetric encryption
   - Store encryption key in environment variable
   - Never log or display decrypted keys

2. **Password Security**
   - Bcrypt with salt rounds >= 12
   - Password strength requirements
   - Optional 2FA (future enhancement)

3. **Session Security**
   - JWT tokens or secure random tokens
   - Session timeout (configurable)
   - HTTP-only cookies (if using cookies)

4. **Rate Limiting**
   - Per-user API request limits
   - Login attempt limits
   - Global rate limiting for protection

## 📈 Migration Strategy

### Step 1: Create Feature Branch
```bash
git checkout -b feature/multi-user-support
```

### Step 2: Incremental Development
1. Build authentication system
2. Test locally with SQLite
3. Add UI components
4. Test with multiple users
5. Deploy to Render staging
6. Production deployment

### Step 3: Data Migration
- No existing user data to migrate
- Document setup process for community

## 🎯 Success Metrics

- [ ] Users can register and login
- [ ] Users can add their Reddit API keys
- [ ] API keys are securely stored
- [ ] Each user sees only their data
- [ ] Application runs on Render.com
- [ ] < 3 second page load times
- [ ] Support 50+ concurrent users

## 📝 Documentation Updates

1. **User Guide**
   - How to register
   - How to get Reddit API keys
   - How to add API keys
   - Feature overview

2. **Admin Guide**
   - Database backup
   - User management
   - Monitoring
   - Troubleshooting

3. **Developer Guide**
   - Local development setup
   - Contributing guidelines
   - API documentation

## 🚦 Testing Plan

### Unit Tests
- Authentication functions
- Encryption/decryption
- Database operations
- API key validation

### Integration Tests
- User registration flow
- Login/logout flow
- API key management
- Reddit API integration

### Load Testing
- 50 concurrent users
- 1000 API requests/hour
- Database performance

## 📅 Timeline

**Week 1:**
- Days 1-2: Database setup and models
- Days 3-4: Authentication system
- Days 5-7: API key management

**Week 2:**
- Days 1-2: UI updates for auth
- Days 3-4: Multi-user support
- Days 5-7: Security and testing

**Week 3:**
- Days 1-2: Render.com setup
- Days 3-4: Deployment and testing
- Days 5-7: Documentation and polish

## 🎉 Next Steps

1. Review and approve this plan
2. Set up development environment
3. Create feature branch
4. Start with Phase 1: Backend Infrastructure
5. Regular testing and code reviews

## 📌 Notes

- Keep it simple for community use
- No complex billing or payment systems
- Focus on security and usability
- Optimize for 50-100 users initially
- Plan for future enhancements (OAuth, social login, etc.)
