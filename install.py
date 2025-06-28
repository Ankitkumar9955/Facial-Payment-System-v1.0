#!/usr/bin/env python3
"""
Face Pay Installation Script
Helps users install dependencies and set up the system
"""

import sys
import os
import subprocess
import platform

def main():
    """Main installation function"""
    print("🚀 Face Pay - Installation Script")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("Please run this script from the face_pay directory.")
        return
    
    print("✅ Found Face Pay files")
    
    # Install dependencies
    install_dependencies()
    
    # Test installation
    test_installation()
    
    print("\n🎉 Installation completed!")
    print("You can now run the system using:")
    print("  python run.py")
    print("  or")
    print("  python main.py")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip not found. Please install pip first.")
        return
    
    # Upgrade pip
    print("Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not upgrade pip: {e}")
    
    # Install dependencies from requirements.txt
    if os.path.exists("requirements.txt"):
        print("Installing from requirements.txt...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            print("\nTrying alternative installation method...")
            install_dependencies_alternative()
    else:
        print("❌ requirements.txt not found")
        install_dependencies_alternative()

def install_dependencies_alternative():
    """Alternative dependency installation method"""
    print("Installing dependencies individually...")
    
    dependencies = [
        "opencv-python",
        "face-recognition", 
        "numpy",
        "Pillow"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True)
            print(f"✅ {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            
            # Special handling for face-recognition
            if dep == "face-recognition":
                print("Trying to install face-recognition prerequisites...")
                install_face_recognition_prerequisites()

def install_face_recognition_prerequisites():
    """Install prerequisites for face-recognition library"""
    system = platform.system().lower()
    
    if system == "windows":
        print("Windows detected. Installing Visual C++ build tools...")
        print("Please install Visual Studio Build Tools manually if needed.")
        print("Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        
        # Try installing cmake first
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "cmake"], 
                          check=True)
            print("✅ cmake installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install cmake")
        
        # Try installing dlib
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "dlib"], 
                          check=True)
            print("✅ dlib installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dlib")
            print("Try installing from: https://github.com/sachadee/Dlib")
    
    elif system == "linux":
        print("Linux detected. Installing system dependencies...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "cmake"], check=True)
            print("✅ cmake installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install cmake")
    
    elif system == "darwin":  # macOS
        print("macOS detected. Installing system dependencies...")
        try:
            subprocess.run(["brew", "install", "cmake"], check=True)
            print("✅ cmake installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install cmake")
            print("Please install Homebrew first: https://brew.sh/")

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing installation...")
    
    tests = [
        ("opencv-python", "cv2"),
        ("face-recognition", "face_recognition"),
        ("numpy", "numpy"),
        ("Pillow", "PIL")
    ]
    
    all_passed = True
    
    for package, import_name in tests:
        try:
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All dependencies installed successfully!")
    else:
        print("\n⚠️  Some dependencies failed to install.")
        print("Please try installing them manually:")
        print("pip install opencv-python face-recognition numpy Pillow")
    
    # Test basic functionality
    print("\n🔍 Testing basic functionality...")
    try:
        from face_recognition_module import FaceRecognitionModule
        from pin_verification import PINVerification
        print("✅ Core modules imported successfully")
    except ImportError as e:
        print(f"❌ Error importing core modules: {e}")

if __name__ == "__main__":
    main() 