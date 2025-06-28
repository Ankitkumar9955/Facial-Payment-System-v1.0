#!/usr/bin/env python3
"""
User Registration Script for Face Pay
Standalone script to register new users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_recognition_module import FaceRecognitionModule
from pin_verification import PINVerification

def register_new_user():
    """Register a new user with face and PIN"""
    print("=" * 50)
    print("Face Pay - User Registration")
    print("=" * 50)
    
    # Initialize modules
    face_module = FaceRecognitionModule()
    pin_module = PINVerification()
    
    while True:
        print("\n1. Register New User")
        print("2. List Registered Users")
        print("3. Remove User")
        print("4. Change PIN")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            register_user(face_module, pin_module)
        elif choice == "2":
            list_users(face_module, pin_module)
        elif choice == "3":
            remove_user(face_module, pin_module)
        elif choice == "4":
            change_user_pin(pin_module)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def register_user(face_module, pin_module):
    """Register a new user"""
    print("\n--- Register New User ---")
    
    # Get user name
    name = input("Enter user name: ").strip()
    if not name:
        print("❌ Name cannot be empty")
        return
    
    # Check if user already exists
    if name in face_module.get_registered_users():
        print(f"⚠️  User '{name}' already exists.")
        overwrite = input("Do you want to update their face and PIN? (y/n): ").strip().lower()
        if overwrite != 'y':
            return
    
    # Register face
    print(f"\n📸 Registering face for: {name}")
    print("Please look at the camera and press 'R' to register your face...")
    print("Press 'Q' to quit registration")
    
    if face_module.register_face(name):
        # Get PIN
        while True:
            pin = input(f"Enter a 4-6 digit PIN for {name}: ").strip()
            if pin_module.set_pin(name, pin):
                print(f"✅ User '{name}' registered successfully!")
                break
            else:
                print("❌ Invalid PIN format. PIN must be 4-6 digits.")
    else:
        print("❌ Face registration failed")

def list_users(face_module, pin_module):
    """List all registered users"""
    print("\n--- Registered Users ---")
    
    face_users = face_module.get_registered_users()
    pin_users = pin_module.get_users()
    
    if not face_users and not pin_users:
        print("No users registered yet.")
        return
    
    print(f"{'Name':<20} {'Face':<10} {'PIN':<10}")
    print("-" * 40)
    
    all_users = set(face_users + pin_users)
    for user in sorted(all_users):
        has_face = "✅" if user in face_users else "❌"
        has_pin = "✅" if user in pin_users else "❌"
        print(f"{user:<20} {has_face:<10} {has_pin:<10}")

def remove_user(face_module, pin_module):
    """Remove a user"""
    print("\n--- Remove User ---")
    
    users = face_module.get_registered_users()
    if not users:
        print("No users to remove.")
        return
    
    print("Registered users:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user}")
    
    try:
        choice = int(input("\nEnter user number to remove: ")) - 1
        if 0 <= choice < len(users):
            user = users[choice]
            confirm = input(f"Are you sure you want to remove '{user}'? (y/n): ").strip().lower()
            if confirm == 'y':
                # Remove from face module (would need to implement this)
                print(f"⚠️  Face data removal not implemented yet")
                # Remove from PIN module
                if pin_module.remove_user(user):
                    print(f"✅ User '{user}' removed from PIN database")
        else:
            print("❌ Invalid user number")
    except ValueError:
        print("❌ Invalid input")

def change_user_pin(pin_module):
    """Change user PIN"""
    print("\n--- Change User PIN ---")
    
    users = pin_module.get_users()
    if not users:
        print("No users with PINs found.")
        return
    
    print("Users with PINs:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user}")
    
    try:
        choice = int(input("\nEnter user number: ")) - 1
        if 0 <= choice < len(users):
            user = users[choice]
            old_pin = input(f"Enter current PIN for {user}: ").strip()
            new_pin = input(f"Enter new PIN for {user}: ").strip()
            
            if pin_module.change_pin(user, old_pin, new_pin):
                print(f"✅ PIN changed successfully for '{user}'")
            else:
                print("❌ Failed to change PIN. Check your current PIN.")
        else:
            print("❌ Invalid user number")
    except ValueError:
        print("❌ Invalid input")

if __name__ == "__main__":
    register_new_user() 