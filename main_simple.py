#!/usr/bin/env python3
"""
Face Pay - Merchant Payment System
Main entry point using simple face detection (OpenCV only)
"""

import sys
import os
from gui import FacePayGUI
from simple_face_detection import SimpleFaceDetection
from pin_verification import PINVerification
from transaction_manager import TransactionManager

def main():
    """Main function to start the Face Pay application (simplified version)"""
    print("🚀 Starting Face Pay - Merchant Payment System")
    print("=" * 60)
    print("ℹ️  Using OpenCV-based face detection (no face_recognition library required)")
    print("ℹ️  Merchant Flow: Amount Entry → Face Scan → PIN Verification → Payment Result")
    print("ℹ️  Transaction tracking and history enabled")
    print("=" * 60)
    
    # Initialize modules
    face_module = SimpleFaceDetection()
    pin_module = PINVerification()
    transaction_manager = TransactionManager()
    
    # Show system status
    print(f"📊 System Status:")
    print(f"   - Registered users: {len(face_module.get_registered_users())}")
    print(f"   - Users with PINs: {len(pin_module.get_users())}")
    
    stats = transaction_manager.get_transaction_stats()
    print(f"   - Total transactions: {stats['total']}")
    print(f"   - Successful payments: {stats['successful']}")
    print(f"   - Total amount processed: ₹{stats['total_amount']}")
    print("=" * 60)
    
    # Start GUI
    app = FacePayGUI(face_module, pin_module)
    app.run()

if __name__ == "__main__":
    main() 