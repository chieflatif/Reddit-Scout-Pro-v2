"""API key encryption utilities for secure storage."""

import os
import base64
from cryptography.fernet import Fernet
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class APIKeyEncryption:
    """Handles encryption and decryption of API keys."""
    
    def __init__(self):
        self.cipher = self._initialize_cipher()
    
    def _initialize_cipher(self) -> Fernet:
        """Initialize the encryption cipher."""
        # Get encryption key from environment
        encryption_key = os.getenv('ENCRYPTION_KEY')
        
        if not encryption_key:
            # Generate a new key for development
            key = Fernet.generate_key()
            encryption_key = key.decode()
            logger.warning(f"No ENCRYPTION_KEY found in environment. Generated new key: {encryption_key}")
            logger.warning("Add this to your Replit Secrets as ENCRYPTION_KEY")
            print(f"\n🔑 IMPORTANT: Add this to your Replit Secrets:")
            print(f"ENCRYPTION_KEY={encryption_key}\n")
        
        try:
            # Handle both string and bytes
            if isinstance(encryption_key, str):
                key_bytes = encryption_key.encode()
            else:
                key_bytes = encryption_key
            
            return Fernet(key_bytes)
        except Exception as e:
            logger.error(f"Failed to initialize encryption cipher: {e}")
            # Generate a new key as fallback
            key = Fernet.generate_key()
            logger.warning(f"Using fallback encryption key: {key.decode()}")
            return Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext string.
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        if not plaintext:
            return ""
        
        try:
            # Encrypt the plaintext
            encrypted_bytes = self.cipher.encrypt(plaintext.encode('utf-8'))
            # Return as base64 string for database storage
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise ValueError("Failed to encrypt data")
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        """
        Decrypt a ciphertext string.
        
        Args:
            ciphertext: Base64 encoded encrypted string
            
        Returns:
            Decrypted plaintext string or None if decryption fails
        """
        if not ciphertext:
            return ""
        
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(ciphertext.encode('utf-8'))
            # Decrypt
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None
    
    def test_encryption(self) -> bool:
        """Test encryption/decryption functionality."""
        try:
            test_data = "test_api_key_12345"
            encrypted = self.encrypt(test_data)
            decrypted = self.decrypt(encrypted)
            return decrypted == test_data
        except Exception as e:
            logger.error(f"Encryption test failed: {e}")
            return False

# Global encryption instance
encryption = APIKeyEncryption()

def encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key for storage."""
    return encryption.encrypt(api_key)

def decrypt_api_key(encrypted_key: str) -> Optional[str]:
    """Decrypt an API key from storage."""
    return encryption.decrypt(encrypted_key)

def test_encryption_system() -> bool:
    """Test the encryption system."""
    return encryption.test_encryption()
