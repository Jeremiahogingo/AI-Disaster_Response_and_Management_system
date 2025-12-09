#src/auth/auth_manager.py
"""Authentication manager for Disaster_Management_System."""
import os
from typing import Optional, Dict
from pymongo import MongoClient
from datetime import datetime
import hashlib
import secrets
import bcrypt

class AuthManager:
    """Manages user authentication, registration, and session management."""
    
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.mongo_client.disasterconnect
        self.users = self.db.users
        self._current_user = None
        
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt (more secure than custom implementation)."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, stored_hash: str, password: str) -> bool:
        """Verify password against stored bcrypt hash."""
        try:
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception:
            return False
    
    def register_user(self, user_data: Dict) -> bool:
        """Register a new user with comprehensive data."""
        try:
            # Check if email already exists
            if self.users.find_one({'email': user_data['email']}):
                return False
            
            # Hash password
            user_data['password'] = self.hash_password(user_data['password'])
            user_data['created_at'] = datetime.utcnow()
            user_data['last_login'] = None
            user_data['is_active'] = True
            
            # Insert user
            result = self.users.insert_one(user_data)
            return result.inserted_id is not None
            
        except Exception as e:
            print(f"Registration error: {str(e)}")
            return False
    
    def login(self, email: str, password: str) -> Optional[Dict]:
        """Login user and return user data if successful."""
        try:
            user = self.users.find_one({'email': email, 'is_active': True})
            if not user or not self.verify_password(user['password'], password):
                return None
                
            # Update last login
            self.users.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            
            # Return user data (excluding password)
            self._current_user = {
                'user_id': str(user['_id']),
                'email': user['email'],
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', ''),
                'organization': user.get('organization', ''),
                'role': user.get('role', 'User'),
                'created_at': user.get('created_at')
            }
            
            return self._current_user
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None
    
    def logout(self):
        """Logout current user."""
        self._current_user = None
    
    def update_password(self, email: str, new_password: str) -> bool:
        """Update user password."""
        try:
            hashed_password = self.hash_password(new_password)
            result = self.users.update_one(
                {'email': email},
                {'$set': {'password': hashed_password}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Password update error: {str(e)}")
            return False
    
    def user_exists(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        try:
            return self.users.find_one({'email': email}) is not None
        except Exception:
            return False
    
    @property
    def current_user(self) -> Optional[Dict]:
        """Get current logged in user."""
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self._current_user is not None
    
    def close_connection(self):
        """Close database connection."""
        if self.mongo_client:
            self.mongo_client.close()