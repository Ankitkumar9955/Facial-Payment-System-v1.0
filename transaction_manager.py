#!/usr/bin/env python3
"""
Transaction Manager for Face Pay
Handles transaction state and data throughout the payment flow
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json
import os

@dataclass
class TransactionState:
    """Transaction state data class"""
    amount: Optional[str] = None
    user_name: Optional[str] = None
    pin_verified: bool = False
    transaction_id: Optional[str] = None
    timestamp: Optional[str] = None
    status: str = "pending"  # pending, success, failed

class TransactionManager:
    def __init__(self, transactions_file: str = "data/transactions.json"):
        """Initialize the transaction manager"""
        self.transactions_file = transactions_file
        self.current_transaction = TransactionState()
        self.transaction_history = []
        self.load_transactions()
    
    def load_transactions(self):
        """Load transaction history from file"""
        try:
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    self.transaction_history = json.load(f)
                print(f"✅ Loaded {len(self.transaction_history)} transaction records")
            else:
                print("ℹ️  No transaction history found. Creating new file.")
                self.transaction_history = []
        except Exception as e:
            print(f"❌ Error loading transactions: {e}")
            self.transaction_history = []
    
    def save_transactions(self):
        """Save transaction history to file"""
        try:
            os.makedirs(os.path.dirname(self.transactions_file), exist_ok=True)
            with open(self.transactions_file, 'w') as f:
                json.dump(self.transaction_history, f, indent=2)
            print(f"✅ Saved {len(self.transaction_history)} transaction records")
        except Exception as e:
            print(f"❌ Error saving transactions: {e}")
    
    def start_new_transaction(self, amount: str) -> str:
        """Start a new transaction"""
        # Generate transaction ID
        timestamp = datetime.now()
        transaction_id = f"TXN{timestamp.strftime('%Y%m%d%H%M%S')}"
        
        # Create new transaction state
        self.current_transaction = TransactionState(
            amount=amount,
            transaction_id=transaction_id,
            timestamp=timestamp.isoformat(),
            status="pending"
        )
        
        print(f"🔄 Started new transaction: {transaction_id} for ₹{amount}")
        return transaction_id
    
    def set_user(self, user_name: str):
        """Set the user for the current transaction"""
        self.current_transaction.user_name = user_name
        print(f"👤 User set for transaction: {user_name}")
    
    def verify_pin(self, success: bool):
        """Mark PIN verification result"""
        self.current_transaction.pin_verified = success
        if success:
            self.current_transaction.status = "success"
            print(f"✅ PIN verified successfully")
        else:
            self.current_transaction.status = "failed"
            print(f"❌ PIN verification failed")
    
    def complete_transaction(self):
        """Complete the current transaction and save to history"""
        if self.current_transaction.transaction_id:
            # Convert to dictionary for JSON serialization
            transaction_data = {
                "transaction_id": self.current_transaction.transaction_id,
                "amount": self.current_transaction.amount,
                "user_name": self.current_transaction.user_name,
                "timestamp": self.current_transaction.timestamp,
                "status": self.current_transaction.status,
                "pin_verified": self.current_transaction.pin_verified
            }
            
            self.transaction_history.append(transaction_data)
            self.save_transactions()
            
            print(f"💾 Transaction completed and saved: {self.current_transaction.transaction_id}")
    
    def reset_transaction(self):
        """Reset the current transaction"""
        self.current_transaction = TransactionState()
        print("🔄 Transaction reset")
    
    def get_current_amount(self) -> Optional[str]:
        """Get the current transaction amount"""
        return self.current_transaction.amount
    
    def get_current_user(self) -> Optional[str]:
        """Get the current transaction user"""
        return self.current_transaction.user_name
    
    def get_transaction_summary(self) -> str:
        """Get a summary of the current transaction"""
        if not self.current_transaction.transaction_id:
            return "No active transaction"
        
        summary = f"Transaction ID: {self.current_transaction.transaction_id}\n"
        summary += f"Amount: ₹{self.current_transaction.amount}\n"
        summary += f"User: {self.current_transaction.user_name or 'Not set'}\n"
        summary += f"Status: {self.current_transaction.status}\n"
        summary += f"PIN Verified: {self.current_transaction.pin_verified}"
        
        return summary
    
    def get_recent_transactions(self, limit: int = 10) -> list:
        """Get recent transactions"""
        return self.transaction_history[-limit:] if self.transaction_history else []
    
    def get_transaction_stats(self) -> dict:
        """Get transaction statistics"""
        if not self.transaction_history:
            return {"total": 0, "successful": 0, "failed": 0, "total_amount": 0}
        
        total = len(self.transaction_history)
        successful = sum(1 for t in self.transaction_history if t["status"] == "success")
        failed = sum(1 for t in self.transaction_history if t["status"] == "failed")
        total_amount = sum(float(t["amount"]) for t in self.transaction_history if t["status"] == "success")
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "total_amount": round(total_amount, 2)
        } 