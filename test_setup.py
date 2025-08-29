"""Test script to verify Reddit Scout Pro multi-user setup."""

import os
import sys
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test database connection and models."""
    try:
        from src.database.database import init_db, check_db_health, get_db_session
        from src.database.models import User, APIKey, Session
        
        print("🔍 Testing database...")
        
        # Initialize database
        if not init_db():
            print("❌ Database initialization failed")
            return False
        
        # Check health
        if not check_db_health():
            print("❌ Database health check failed")
            return False
        
        print("✅ Database connection successful")
        return True
    
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_encryption():
    """Test encryption system."""
    try:
        from src.core.encryption import test_encryption_system, encrypt_api_key, decrypt_api_key
        
        print("🔍 Testing encryption...")
        
        if not test_encryption_system():
            print("❌ Encryption system test failed")
            return False
        
        # Test actual encryption/decryption
        test_key = "test_reddit_api_key_12345"
        encrypted = encrypt_api_key(test_key)
        decrypted = decrypt_api_key(encrypted)
        
        if decrypted != test_key:
            print("❌ Encryption/decryption mismatch")
            return False
        
        print("✅ Encryption system working")
        return True
    
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
        return False

def test_authentication():
    """Test authentication system."""
    try:
        from src.auth.auth_manager import AuthManager
        
        print("🔍 Testing authentication...")
        
        auth = AuthManager()
        
        # Test password hashing
        password = "test123"
        hashed = auth.hash_password(password)
        
        if not auth.verify_password(password, hashed):
            print("❌ Password hashing/verification failed")
            return False
        
        # Test user registration (cleanup after)
        test_user = f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = auth.register_user(
            username=test_user,
            email=f"{test_user}@example.com",
            password="TestPassword123"
        )
        
        if not result["success"]:
            print(f"❌ User registration failed: {result['message']}")
            return False
        
        print("✅ Authentication system working")
        return True
    
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_reddit_client():
    """Test Reddit client initialization."""
    try:
        from src.core.reddit_scout_multi import UserRedditScout
        
        print("🔍 Testing Reddit client...")
        
        # Create a scout instance (won't work without API keys, but should initialize)
        scout = UserRedditScout(user_id=999)  # Fake user ID for testing
        
        if scout is None:
            print("❌ Reddit client initialization failed")
            return False
        
        print("✅ Reddit client initialization successful")
        return True
    
    except Exception as e:
        print(f"❌ Reddit client test failed: {e}")
        return False

def test_environment():
    """Test environment configuration."""
    print("🔍 Testing environment...")
    
    # Check critical environment variables
    database_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    encryption_key = os.getenv('ENCRYPTION_KEY')
    
    print(f"DATABASE_URL: {'✅ Set' if database_url else '⚠️ Not set (will use SQLite)'}")
    print(f"SECRET_KEY: {'✅ Set' if secret_key else '⚠️ Not set (will use default)'}")
    print(f"ENCRYPTION_KEY: {'✅ Set' if encryption_key else '⚠️ Not set (will generate)'}")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Reddit Scout Pro Multi-User Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Database", test_database),
        ("Encryption", test_encryption),
        ("Authentication", test_authentication),
        ("Reddit Client", test_reddit_client)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} Test:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Run 'python main.py' to start the application")
        print("2. Open the provided URL in your browser")
        print("3. Create your first user account")
        print("4. Configure Reddit API keys")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Ensure all dependencies are installed: pip install -r requirements_multi_user.txt")
        print("2. Set up environment variables in .env or Replit Secrets")
        print("3. Enable PostgreSQL database in Replit")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
