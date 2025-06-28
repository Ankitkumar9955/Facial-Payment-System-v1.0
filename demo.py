#!/usr/bin/env python3
"""
Demo Script for Face Pay
Demonstrates the system functionality and provides testing capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_recognition_module import FaceRecognitionModule
from pin_verification import PINVerification

def demo_face_recognition():
    """Demo face recognition functionality"""
    print("=" * 50)
    print("Face Recognition Demo")
    print("=" * 50)
    
    face_module = FaceRecognitionModule()
    
    print(f"Registered users: {face_module.get_registered_users()}")
    
    if not face_module.get_registered_users():
        print("No users registered. Please register a user first.")
        return
    
    print("\nStarting face recognition demo...")
    print("Look at the camera and press 'C' when recognized, or 'Q' to quit")
    
    success, username = face_module.start_recognition()
    
    if success:
        print(f"✅ Demo successful! Recognized user: {username}")
    else:
        print("❌ Demo failed - no face recognized")

def demo_pin_verification():
    """Demo PIN verification functionality"""
    print("=" * 50)
    print("PIN Verification Demo")
    print("=" * 50)
    
    pin_module = PINVerification()
    
    print(f"Users with PINs: {pin_module.get_users()}")
    
    if not pin_module.get_users():
        print("No users with PINs found. Please register a user with PIN first.")
        return
    
    # Demo with first user
    username = pin_module.get_users()[0]
    print(f"\nTesting PIN verification for user: {username}")
    
    # Test with correct PIN (this would normally come from user input)
    print("Note: This demo cannot test actual PIN verification without user input")
    print("Use the main application or registration script to test PIN functionality")

def demo_registration():
    """Demo user registration"""
    print("=" * 50)
    print("User Registration Demo")
    print("=" * 50)
    
    face_module = FaceRecognitionModule()
    pin_module = PINVerification()
    
    print("This demo shows the registration process")
    print("To actually register a user, use the registration script:")
    print("python register_user.py")
    
    print(f"\nCurrent registered users: {face_module.get_registered_users()}")
    print(f"Users with PINs: {pin_module.get_users()}")

def run_full_demo():
    """Run complete system demo"""
    print("🚀 Face Pay System Demo")
    print("=" * 50)
    
    while True:
        print("\nDemo Options:")
        print("1. Face Recognition Demo")
        print("2. PIN Verification Demo")
        print("3. Registration Demo")
        print("4. System Status")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_face_recognition()
        elif choice == "2":
            demo_pin_verification()
        elif choice == "3":
            demo_registration()
        elif choice == "4":
            show_system_status()
        elif choice == "5":
            print("👋 Demo completed!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def show_system_status():
    """Show current system status"""
    print("=" * 50)
    print("System Status")
    print("=" * 50)
    
    face_module = FaceRecognitionModule()
    pin_module = PINVerification()
    
    face_users = face_module.get_registered_users()
    pin_users = pin_module.get_users()
    
    print(f"Registered faces: {len(face_users)}")
    print(f"Users with PINs: {len(pin_users)}")
    
    if face_users:
        print(f"Face users: {', '.join(face_users)}")
    
    if pin_users:
        print(f"PIN users: {', '.join(pin_users)}")
    
    # Check data files
    import os
    faces_file = "data/faces.pkl"
    pin_file = "data/pin_data.json"
    
    print(f"\nData files:")
    print(f"Faces file exists: {os.path.exists(faces_file)}")
    print(f"PIN file exists: {os.path.exists(pin_file)}")

if __name__ == "__main__":
    run_full_demo() 