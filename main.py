#!/usr/bin/env python3
"""
Face Pay - Facial Recognition Payment System
Main entry point for the application
"""

import sys
import os
from gui import FacePayGUI
from face_recognition_module import FaceRecognitionModule
from pin_verification import PINVerification

def main():
    """Main function to start the Face Pay application"""
    print("🚀 Starting Face Pay - Facial Recognition Payment System")
    print("=" * 50)
    
    # Initialize modules
    face_module = FaceRecognitionModule()
    pin_module = PINVerification()
    
    # Start GUI
    app = FacePayGUI(face_module, pin_module)
    app.run()

if __name__ == "__main__":
    main() 