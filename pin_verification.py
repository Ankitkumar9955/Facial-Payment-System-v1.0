#!/usr/bin/env python3
"""
PIN Verification Module for Face Pay
Handles PIN storage, validation, and security
"""

import json
import os
import hashlib
import secrets
from typing import Dict, Optional

class PINVerification:
    def __init__(self, pin_file: str = "data/pin_data.json"):
        """Initialize the PIN verification module"""
        self.pin_file = pin_file
        self.pin_data = {}
        self.load_pins()
    
    def load_pins(self):
        """Load PIN data from JSON file"""
        try:
            if os.path.exists(self.pin_file):
                with open(self.pin_file, 'r') as f:
                    self.pin_data = json.load(f)
                print(f"✅ Loaded PIN data for {len(self.pin_data)} users")
            else:
                print("ℹ️  No PIN data found. Creating new PIN file.")
                self.pin_data = {}
        except Exception as e:
            print(f"❌ Error loading PIN data: {e}")
            self.pin_data = {}
    
    def save_pins(self):
        """Save PIN data to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.pin_file), exist_ok=True)
            with open(self.pin_file, 'w') as f:
                json.dump(self.pin_data, f, indent=2)
            print(f"✅ Saved PIN data for {len(self.pin_data)} users")
        except Exception as e:
            print(f"❌ Error saving PIN data: {e}")
    
    def hash_pin(self, pin: str) -> str:
        """Hash a PIN using SHA-256 with salt"""
        # In a real system, you'd use a proper salt per user
        # For this prototype, we'll use a simple hash
        salt = "face_pay_salt_2024"
        return hashlib.sha256((pin + salt).encode()).hexdigest()
    
    def set_pin(self, username: str, pin: str) -> bool:
        """Set PIN for a user"""
        if not self._validate_pin_format(pin):
            return False
        
        hashed_pin = self.hash_pin(pin)
        self.pin_data[username] = hashed_pin
        self.save_pins()
        print(f"✅ PIN set for user: {username}")
        return True
    
    def verify_pin(self, username: str, pin: str) -> bool:
        """Verify PIN for a user"""
        if username not in self.pin_data:
            print(f"❌ User '{username}' not found in PIN database")
            return False
        
        hashed_pin = self.hash_pin(pin)
        stored_hash = self.pin_data[username]
        
        if hashed_pin == stored_hash:
            print(f"✅ PIN verified for user: {username}")
            return True
        else:
            print(f"❌ Invalid PIN for user: {username}")
            return False
    
    def _validate_pin_format(self, pin: str) -> bool:
        """Validate PIN format (4-6 digits)"""
        if not pin.isdigit():
            print("❌ PIN must contain only digits")
            return False
        
        if len(pin) < 4 or len(pin) > 6:
            print("❌ PIN must be 4-6 digits long")
            return False
        
        return True
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists in PIN database"""
        return username in self.pin_data
    
    def get_users(self) -> list:
        """Get list of users with PINs"""
        return list(self.pin_data.keys())
    
    def remove_user(self, username: str) -> bool:
        """Remove user from PIN database"""
        if username in self.pin_data:
            del self.pin_data[username]
            self.save_pins()
            print(f"✅ Removed user: {username}")
            return True
        else:
            print(f"❌ User '{username}' not found")
            return False
    
    def change_pin(self, username: str, old_pin: str, new_pin: str) -> bool:
        """Change PIN for a user"""
        if not self.verify_pin(username, old_pin):
            return False
        
        return self.set_pin(username, new_pin) 