#!/usr/bin/env python3
"""
Face Pay Launcher
Easy access to all Face Pay features
"""

import sys
import os
import subprocess

def main():
    """Main launcher function"""
    print("🚀 Face Pay - Facial Recognition Payment System")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. 🎯 Launch Main Application")
        print("2. 👤 User Registration")
        print("3. 🧪 System Demo")
        print("4. 📋 System Status")
        print("5. 📖 View README")
        print("6. ❌ Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            launch_main_app()
        elif choice == "2":
            launch_registration()
        elif choice == "3":
            launch_demo()
        elif choice == "4":
            show_status()
        elif choice == "5":
            show_readme()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def launch_main_app():
    """Launch the main Face Pay application"""
    print("\n🎯 Launching Face Pay Application...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
    except FileNotFoundError:
        print("❌ main.py not found. Make sure you're in the correct directory.")

def launch_registration():
    """Launch the user registration script"""
    print("\n👤 Launching User Registration...")
    try:
        subprocess.run([sys.executable, "register_user.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching registration: {e}")
    except FileNotFoundError:
        print("❌ register_user.py not found. Make sure you're in the correct directory.")

def launch_demo():
    """Launch the demo script"""
    print("\n🧪 Launching System Demo...")
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching demo: {e}")
    except FileNotFoundError:
        print("❌ demo.py not found. Make sure you're in the correct directory.")

def show_status():
    """Show system status"""
    print("\n📋 System Status")
    print("=" * 30)
    
    # Check if required files exist
    files_to_check = [
        "main.py",
        "face_recognition_module.py", 
        "pin_verification.py",
        "gui.py",
        "requirements.txt"
    ]
    
    print("Required files:")
    for file in files_to_check:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
    
    # Check data directory
    data_dir = "data"
    data_exists = os.path.exists(data_dir)
    status = "✅" if data_exists else "❌"
    print(f"  {status} {data_dir}/")
    
    # Check dependencies
    print("\nDependencies:")
    try:
        import cv2
        print("  ✅ opencv-python")
    except ImportError:
        print("  ❌ opencv-python")
    
    try:
        import face_recognition
        print("  ✅ face-recognition")
    except ImportError:
        print("  ❌ face-recognition")
    
    try:
        import numpy
        print("  ✅ numpy")
    except ImportError:
        print("  ❌ numpy")

def show_readme():
    """Show README content"""
    print("\n📖 README Content")
    print("=" * 30)
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            # Show first 500 characters
            print(content[:500] + "..." if len(content) > 500 else content)
            print("\n📄 Full README available in README.md file")
    except FileNotFoundError:
        print("❌ README.md not found")
    except Exception as e:
        print(f"❌ Error reading README: {e}")

if __name__ == "__main__":
    main() 