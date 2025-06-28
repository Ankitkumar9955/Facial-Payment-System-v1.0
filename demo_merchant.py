#!/usr/bin/env python3
"""
Merchant Payment Flow Demo
Demonstrates the complete merchant payment flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_face_detection import SimpleFaceDetection
from pin_verification import PINVerification
from transaction_manager import TransactionManager

def demo_merchant_flow():
    """Demo the complete merchant payment flow"""
    print("=" * 60)
    print("Face Pay - Merchant Payment Flow Demo")
    print("=" * 60)
    
    # Initialize modules
    face_module = SimpleFaceDetection()
    pin_module = PINVerification()
    transaction_manager = TransactionManager()
    
    print("\n📋 Demo Flow:")
    print("1. Merchant enters payment amount")
    print("2. Customer scans face for recognition")
    print("3. Customer enters PIN for verification")
    print("4. System shows payment result")
    print("5. Transaction is recorded")
    
    while True:
        print("\n" + "=" * 40)
        print("Merchant Payment Flow Options:")
        print("1. 🎯 Start Complete Payment Flow")
        print("2. 📊 View Transaction History")
        print("3. 👤 Register New User")
        print("4. 📈 View System Statistics")
        print("5. ❌ Exit Demo")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            run_payment_flow(face_module, pin_module, transaction_manager)
        elif choice == "2":
            view_transaction_history(transaction_manager)
        elif choice == "3":
            register_user(face_module, pin_module)
        elif choice == "4":
            view_system_stats(face_module, pin_module, transaction_manager)
        elif choice == "5":
            print("👋 Demo completed!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def run_payment_flow(face_module, pin_module, transaction_manager):
    """Run a complete payment flow"""
    print("\n" + "=" * 40)
    print("🛒 Starting Payment Flow")
    print("=" * 40)
    
    # Step 1: Amount Entry
    print("\n💰 Step 1: Amount Entry")
    amount = input("Enter payment amount (₹): ").strip()
    
    if not amount:
        print("❌ No amount entered. Cancelling payment.")
        return
    
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            print("❌ Invalid amount. Must be greater than 0.")
            return
    except ValueError:
        print("❌ Invalid amount format.")
        return
    
    # Start transaction
    transaction_id = transaction_manager.start_new_transaction(f"{amount_float:.2f}")
    print(f"✅ Transaction started: {transaction_id}")
    
    # Step 2: Face Recognition
    print(f"\n👤 Step 2: Face Recognition (Amount: ₹{amount_float:.2f})")
    
    if not face_module.get_registered_users():
        print("❌ No users registered. Please register a user first.")
        return
    
    print("Look at the camera and press 'C' when recognized, or 'Q' to quit")
    success, username = face_module.start_recognition()
    
    if not success or not username:
        print("❌ Face recognition failed. Cancelling payment.")
        transaction_manager.verify_pin(False)
        transaction_manager.complete_transaction()
        return
    
    # Set user in transaction
    transaction_manager.set_user(username)
    print(f"✅ Face recognized: {username}")
    
    # Step 3: PIN Verification
    print(f"\n🔐 Step 3: PIN Verification")
    print(f"User: {username}, Amount: ₹{amount_float:.2f}")
    
    if not pin_module.user_exists(username):
        print(f"❌ User '{username}' doesn't have a PIN set.")
        transaction_manager.verify_pin(False)
        transaction_manager.complete_transaction()
        return
    
    pin = input("Enter PIN: ").strip()
    
    if not pin:
        print("❌ No PIN entered. Payment failed.")
        transaction_manager.verify_pin(False)
        transaction_manager.complete_transaction()
        return
    
    # Verify PIN
    if pin_module.verify_pin(username, pin):
        print("✅ PIN verified successfully!")
        transaction_manager.verify_pin(True)
        
        # Step 4: Payment Result
        print(f"\n🎉 Step 4: Payment Result")
        print(f"✅ Payment of ₹{amount_float:.2f} by {username} is successful!")
        print(f"Transaction ID: {transaction_id}")
        
    else:
        print("❌ Incorrect PIN. Payment failed.")
        transaction_manager.verify_pin(False)
    
    # Complete transaction
    transaction_manager.complete_transaction()
    print(f"💾 Transaction recorded in history.")

def view_transaction_history(transaction_manager):
    """View recent transaction history"""
    print("\n" + "=" * 40)
    print("📊 Transaction History")
    print("=" * 40)
    
    recent_transactions = transaction_manager.get_recent_transactions(10)
    
    if not recent_transactions:
        print("No transaction history found.")
        return
    
    print(f"{'ID':<12} {'Amount':<10} {'User':<15} {'Status':<10} {'Time':<20}")
    print("-" * 70)
    
    for tx in recent_transactions:
        # Extract time from timestamp
        timestamp = tx.get('timestamp', '')
        if timestamp:
            time_str = timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp[:8]
        else:
            time_str = 'N/A'
        
        print(f"{tx.get('transaction_id', 'N/A')[:12]:<12} "
              f"₹{tx.get('amount', 'N/A'):<9} "
              f"{tx.get('user_name', 'N/A')[:14]:<15} "
              f"{tx.get('status', 'N/A'):<10} "
              f"{time_str:<20}")

def register_user(face_module, pin_module):
    """Register a new user"""
    print("\n" + "=" * 40)
    print("👤 User Registration")
    print("=" * 40)
    
    name = input("Enter user name: ").strip()
    if not name:
        print("❌ Name cannot be empty")
        return
    
    print(f"\n📸 Registering face for: {name}")
    print("Please look at the camera and press 'R' to capture samples...")
    
    if face_module.register_face(name):
        pin = input(f"Enter a 4-6 digit PIN for {name}: ").strip()
        if pin:
            if pin_module.set_pin(name, pin):
                print(f"✅ User '{name}' registered successfully!")
            else:
                print("❌ Invalid PIN format. PIN must be 4-6 digits.")
        else:
            print("❌ No PIN entered.")
    else:
        print("❌ Face registration failed")

def view_system_stats(face_module, pin_module, transaction_manager):
    """View system statistics"""
    print("\n" + "=" * 40)
    print("📈 System Statistics")
    print("=" * 40)
    
    # User statistics
    registered_users = face_module.get_registered_users()
    pin_users = pin_module.get_users()
    
    print(f"👥 Users:")
    print(f"   - Registered faces: {len(registered_users)}")
    print(f"   - Users with PINs: {len(pin_users)}")
    
    if registered_users:
        print(f"   - Registered users: {', '.join(registered_users)}")
    
    # Transaction statistics
    stats = transaction_manager.get_transaction_stats()
    print(f"\n💰 Transactions:")
    print(f"   - Total transactions: {stats['total']}")
    print(f"   - Successful payments: {stats['successful']}")
    print(f"   - Failed payments: {stats['failed']}")
    print(f"   - Total amount processed: ₹{stats['total_amount']}")
    
    if stats['total'] > 0:
        success_rate = (stats['successful'] / stats['total']) * 100
        print(f"   - Success rate: {success_rate:.1f}%")

if __name__ == "__main__":
    demo_merchant_flow() 