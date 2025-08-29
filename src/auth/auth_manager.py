"""Authentication manager for user registration, login, and session management."""

import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ..database.models import User, Session as UserSession
from ..database.database import get_db_session
import logging
import re

logger = logging.getLogger(__name__)

class AuthManager:
    """Handles user authentication and session management."""
    
    def __init__(self):
        self.session_timeout_days = 7  # Default session timeout
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            salt = bcrypt.gensalt(rounds=12)  # Strong salt
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise ValueError("Failed to hash password")
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username: str) -> bool:
        """Validate username format."""
        # Username: 3-50 characters, alphanumeric and underscores only
        pattern = r'^[a-zA-Z0-9_]{3,50}$'
        return re.match(pattern, username) is not None
    
    def validate_password(self, password: str) -> Dict[str, any]:
        """Validate password strength."""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def register_user(self, username: str, email: str, password: str) -> Dict[str, any]:
        """Register a new user."""
        db = get_db_session()
        try:
            # Validate input
            if not self.validate_username(username):
                return {"success": False, "message": "Invalid username format. Use 3-50 characters, letters, numbers, and underscores only."}
            
            if not self.validate_email(email):
                return {"success": False, "message": "Invalid email format"}
            
            password_validation = self.validate_password(password)
            if not password_validation["valid"]:
                return {"success": False, "message": "; ".join(password_validation["errors"])}
            
            # Check if user exists
            existing = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing:
                if existing.username == username:
                    return {"success": False, "message": "Username already exists"}
                else:
                    return {"success": False, "message": "Email already registered"}
            
            # Create new user
            user = User(
                username=username,
                email=email.lower(),  # Store email in lowercase
                password_hash=self.hash_password(password)
            )
            db.add(user)
            db.commit()
            
            logger.info(f"New user registered: {username}")
            return {
                "success": True, 
                "message": "Registration successful", 
                "user_id": user.id,
                "username": user.username
            }
        except Exception as e:
            db.rollback()
            logger.error(f"User registration failed: {e}")
            return {"success": False, "message": "Registration failed. Please try again."}
        finally:
            db.close()
    
    def login_user(self, username: str, password: str, user_agent: str = None, ip_address: str = None) -> Dict[str, any]:
        """Authenticate user and create session."""
        db = get_db_session()
        try:
            # Find user (allow login with username or email)
            user = db.query(User).filter(
                (User.username == username) | (User.email == username.lower())
            ).first()
            
            if not user:
                return {"success": False, "message": "Invalid credentials"}
            
            if not user.is_active:
                return {"success": False, "message": "Account is disabled"}
            
            if not self.verify_password(password, user.password_hash):
                return {"success": False, "message": "Invalid credentials"}
            
            # Create session token
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(days=self.session_timeout_days)
            
            session = UserSession(
                user_id=user.id,
                session_token=session_token,
                expires_at=expires_at,
                user_agent=user_agent,
                ip_address=ip_address
            )
            db.add(session)
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            logger.info(f"User logged in: {user.username}")
            return {
                "success": True,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "session_token": session_token,
                "expires_at": expires_at.isoformat()
            }
        except Exception as e:
            db.rollback()
            logger.error(f"User login failed: {e}")
            return {"success": False, "message": "Login failed. Please try again."}
        finally:
            db.close()
    
    def validate_session(self, session_token: str) -> Dict[str, any]:
        """Validate session token and return user info."""
        if not session_token:
            return {"valid": False, "message": "No session token provided"}
        
        db = get_db_session()
        try:
            session = db.query(UserSession).filter(
                UserSession.session_token == session_token,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not session:
                return {"valid": False, "message": "Invalid or expired session"}
            
            if not session.user.is_active:
                return {"valid": False, "message": "Account is disabled"}
            
            return {
                "valid": True,
                "user_id": session.user_id,
                "username": session.user.username,
                "email": session.user.email,
                "expires_at": session.expires_at.isoformat()
            }
        except Exception as e:
            logger.error(f"Session validation failed: {e}")
            return {"valid": False, "message": "Session validation failed"}
        finally:
            db.close()
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by invalidating session."""
        if not session_token:
            return False
        
        db = get_db_session()
        try:
            session = db.query(UserSession).filter(
                UserSession.session_token == session_token
            ).first()
            
            if session:
                db.delete(session)
                db.commit()
                logger.info(f"User logged out: session {session_token[:10]}...")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Logout failed: {e}")
            return False
        finally:
            db.close()
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        db = get_db_session()
        try:
            expired_sessions = db.query(UserSession).filter(
                UserSession.expires_at <= datetime.utcnow()
            ).all()
            
            count = len(expired_sessions)
            for session in expired_sessions:
                db.delete(session)
            
            db.commit()
            logger.info(f"Cleaned up {count} expired sessions")
            return count
        except Exception as e:
            db.rollback()
            logger.error(f"Session cleanup failed: {e}")
            return 0
        finally:
            db.close()
    
    def get_user_sessions(self, user_id: int) -> list:
        """Get all active sessions for a user."""
        db = get_db_session()
        try:
            sessions = db.query(UserSession).filter(
                UserSession.user_id == user_id,
                UserSession.expires_at > datetime.utcnow()
            ).all()
            
            return [{
                "id": session.id,
                "created_at": session.created_at.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "user_agent": session.user_agent,
                "ip_address": session.ip_address
            } for session in sessions]
        except Exception as e:
            logger.error(f"Failed to get user sessions: {e}")
            return []
        finally:
            db.close()
