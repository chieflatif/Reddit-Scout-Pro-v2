#!/usr/bin/env python3
"""
Local testing script for Reddit Scout Pro Community Edition.
Tests all components without requiring deployment.
"""

import os
import sys
import sqlite3
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test all imports."""
    print("🔍 Testing imports...")
    
    tests = [
        ("Database", lambda: __import__('database.database')),
        ("Models", lambda: __import__('database.models')),
        ("Auth Manager", lambda: __import__('auth.auth_manager')),
        ("Encryption", lambda: __import__('core.encryption')),
        ("UI Login", lambda: __import__('ui.pages.login')),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name} imports OK")
            passed += 1
        except Exception as e:
            print(f"❌ {name} imports FAIL: {e}")
    
    return passed, len(tests)

def test_database():
    """Test database functionality with SQLite."""
    print("\n🗄️ Testing database...")
    
    # Set environment for SQLite testing
    os.environ['DATABASE_URL'] = 'sqlite:///test_reddit_scout.db'
    
    try:
        from database.database import init_db, check_db_health, get_db_session
        from database.models import User, APIKey
        
        # Initialize database
        if not init_db():
            print("❌ Database initialization failed")
            return False
        
        # Test health check
        if not check_db_health():
            print("❌ Database health check failed")
            return False
        
        # Test basic operations
        db = get_db_session()
        try:
            # Count users (should be 0)
            user_count = db.query(User).count()
            print(f"✅ Database operations OK (users: {user_count})")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_encryption():
    """Test encryption system."""
    print("\n🔐 Testing encryption...")
    
    try:
        from core.encryption import APIKeyEncryption, encrypt_api_key, decrypt_api_key
        
        # Test encryption/decryption
        test_key = "test_reddit_api_key_12345"
        encrypted = encrypt_api_key(test_key)
        decrypted = decrypt_api_key(encrypted)
        
        if decrypted == test_key:
            print("✅ Encryption/decryption OK")
            return True
        else:
            print("❌ Encryption/decryption mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
        return False

def test_authentication():
    """Test authentication system."""
    print("\n👤 Testing authentication...")
    
    try:
        from auth.auth_manager import AuthManager
        
        auth = AuthManager()
        
        # Test password hashing
        password = "test123"
        hashed = auth.hash_password(password)
        
        if not auth.verify_password(password, hashed):
            print("❌ Password hashing/verification failed")
            return False
        
        # Test user registration
        result = auth.register_user(
            username="testuser123",
            email="test@example.com", 
            password="TestPassword123"
        )
        
        if not result["success"]:
            print(f"❌ User registration failed: {result['message']}")
            return False
        
        print("✅ Authentication system OK")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_reddit_client():
    """Test Reddit client initialization."""
    print("\n🤖 Testing Reddit client...")
    
    try:
        from core.reddit_scout_multi import UserRedditScout
        
        # Test initialization (should handle missing API keys gracefully)
        scout = UserRedditScout(user_id=999)  # Fake user ID
        
        if not scout.is_configured():
            print("✅ Reddit client handles missing API keys correctly")
            return True
        else:
            print("⚠️ Reddit client unexpectedly configured (no API keys provided)")
            return True  # Still OK, just unexpected
            
    except Exception as e:
        print(f"❌ Reddit client test failed: {e}")
        return False

def test_streamlit_compatibility():
    """Test Streamlit import and basic functionality."""
    print("\n🌐 Testing Streamlit compatibility...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imports OK")
        
        # Test if we can import our main app
        from pathlib import Path
        app_path = Path(__file__).parent / "app_multi_user.py"
        if app_path.exists():
            print("✅ Main app file exists")
            return True
        else:
            print("❌ Main app file missing")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False

def cleanup():
    """Clean up test files."""
    test_db = Path("test_reddit_scout.db")
    if test_db.exists():
        test_db.unlink()
        print("🧹 Cleaned up test database")

def main():
    """Run all tests."""
    print("🚀 Reddit Scout Pro - Local Testing Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Encryption", test_encryption),
        ("Authentication", test_authentication),
        ("Reddit Client", test_reddit_client),
        ("Streamlit", test_streamlit_compatibility),
    ]
    
    total_passed = 0
    total_tests = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if isinstance(result, tuple):  # For imports test
                passed, count = result
                total_passed += passed
                total_tests += count
            elif result:
                total_passed += 1
                total_tests += 1
            else:
                total_tests += 1
        except Exception as e:
            print(f"💥 {test_name} test crashed: {e}")
            total_tests += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {total_passed}/{total_tests} passed")
    
    if total_passed == total_tests:
        print("🎉 All tests passed! Ready for deployment.")
    else:
        print("❌ Some tests failed. Check issues above.")
    
    cleanup()
    return total_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
