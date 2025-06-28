#!/usr/bin/env python3
"""
GUI Module for Face Pay
Provides a modern, user-friendly interface using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
from typing import Optional
from transaction_manager import TransactionManager

class FacePayGUI:
    def __init__(self, face_module, pin_module):
        """Initialize the Face Pay GUI"""
        self.face_module = face_module
        self.pin_module = pin_module
        self.transaction_manager = TransactionManager()
        self.current_user = None
        self.recognition_thread = None
        self.is_scanning = False
        self.current_frame = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Face Pay - Facial Recognition Payment System")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
        # Configure window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start with amount entry screen
        self.show_amount_entry()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg='#2c3e50')
        self.main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title (always visible)
        title_frame = tk.Frame(self.main_container, bg='#2c3e50')
        title_frame.pack(pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Face Pay",
            font=("Arial", 28, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Facial Recognition Payment System",
            font=("Arial", 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Create different screens
        self.create_amount_entry_screen()
        self.create_face_scan_screen()
        self.create_pin_entry_screen()
        self.create_result_screen()
        
        # Register button (always visible at bottom)
        register_frame = tk.Frame(self.main_container, bg='#2c3e50')
        register_frame.pack(side='bottom', pady=(20, 0))
        
        register_button = tk.Button(
            register_frame,
            text="Register New User",
            command=self.register_user,
            font=("Arial", 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        register_button.pack()
    
    def create_amount_entry_screen(self):
        """Create the amount entry screen"""
        self.amount_frame = tk.Frame(self.main_container, bg='#2c3e50')
        
        # Amount entry section
        amount_section = tk.Frame(self.amount_frame, bg='#2c3e50')
        amount_section.pack(pady=20)
        
        amount_label = tk.Label(
            amount_section,
            text="Enter Payment Amount",
            font=("Arial", 18, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        amount_label.pack(pady=(0, 10))
        
        # Amount entry with currency symbol
        amount_entry_frame = tk.Frame(amount_section, bg='#2c3e50')
        amount_entry_frame.pack(pady=10)
        
        currency_label = tk.Label(
            amount_entry_frame,
            text="₹",
            font=("Arial", 24, "bold"),
            fg='#f39c12',
            bg='#2c3e50'
        )
        currency_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.amount_entry = tk.Entry(
            amount_entry_frame,
            font=("Arial", 24),
            width=15,
            justify='center',
            relief='flat',
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.amount_entry.pack(side=tk.LEFT)
        self.amount_entry.bind('<Return>', self.proceed_to_face_scan)
        self.amount_entry.focus()
        
        # Instructions
        instruction_label = tk.Label(
            amount_section,
            text="Enter the amount to be paid by the customer",
            font=("Arial", 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        instruction_label.pack(pady=10)
        
        # Proceed button
        self.proceed_button = tk.Button(
            amount_section,
            text="Proceed to Face Scan",
            command=self.proceed_to_face_scan,
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.proceed_button.pack(pady=20)
    
    def create_face_scan_screen(self):
        """Create the face scan screen"""
        self.face_scan_frame = tk.Frame(self.main_container, bg='#2c3e50')
        
        # Amount display
        self.amount_display_label = tk.Label(
            self.face_scan_frame,
            text="",
            font=("Arial", 16, "bold"),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.amount_display_label.pack(pady=10)
        
        # Status frame
        self.status_frame = tk.Frame(self.face_scan_frame, bg='#2c3e50')
        self.status_frame.pack(pady=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to scan",
            font=("Arial", 14),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.status_label.pack()
        
        # User info frame
        self.user_frame = tk.Frame(self.face_scan_frame, bg='#2c3e50')
        self.user_frame.pack(pady=10)
        
        self.user_label = tk.Label(
            self.user_frame,
            text="",
            font=("Arial", 12),
            fg='#3498db',
            bg='#2c3e50'
        )
        self.user_label.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.face_scan_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Start Scan button
        self.scan_button = tk.Button(
            button_frame,
            text="Start Face Scan",
            command=self.start_face_scan,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.scan_button.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_button = tk.Button(
            button_frame,
            text="Back to Amount",
            command=self.show_amount_entry,
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        back_button.pack(side=tk.LEFT, padx=10)
    
    def create_pin_entry_screen(self):
        """Create the PIN entry screen"""
        self.pin_frame = tk.Frame(self.main_container, bg='#2c3e50')
        
        # Amount and user display
        self.payment_info_label = tk.Label(
            self.pin_frame,
            text="",
            font=("Arial", 14, "bold"),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.payment_info_label.pack(pady=10)
        
        # PIN entry section
        pin_section = tk.Frame(self.pin_frame, bg='#2c3e50')
        pin_section.pack(pady=20)
        
        pin_label = tk.Label(
            pin_section,
            text="Enter UPI PIN:",
            font=("Arial", 14),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        pin_label.pack()
        
        self.pin_entry = tk.Entry(
            pin_section,
            font=("Arial", 16),
            show="*",
            width=20,
            justify='center',
            relief='flat',
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.pin_entry.pack(pady=10)
        self.pin_entry.bind('<Return>', self.verify_pin)
        
        # Buttons frame
        button_frame = tk.Frame(self.pin_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Verify & Pay button
        self.pay_button = tk.Button(
            button_frame,
            text="Verify & Pay",
            command=self.verify_pin,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.pay_button.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_button = tk.Button(
            button_frame,
            text="Back to Scan",
            command=self.show_face_scan,
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        back_button.pack(side=tk.LEFT, padx=10)
    
    def create_result_screen(self):
        """Create the result screen"""
        self.result_frame = tk.Frame(self.main_container, bg='#2c3e50')
        
        # Result display
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            wraplength=500
        )
        self.result_label.pack(pady=30)
        
        # Transaction details
        self.transaction_details_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 14),
            fg='#bdc3c7',
            bg='#2c3e50',
            wraplength=500
        )
        self.transaction_details_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.result_frame, bg='#2c3e50')
        button_frame.pack(pady=30)
        
        # New Transaction button
        new_transaction_button = tk.Button(
            button_frame,
            text="New Transaction",
            command=self.new_transaction,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        new_transaction_button.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.on_closing,
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        exit_button.pack(side=tk.LEFT, padx=10)
    
    def show_amount_entry(self):
        """Show the amount entry screen"""
        self.hide_all_frames()
        self.amount_frame.pack(expand=True, fill='both')
        self.current_frame = self.amount_frame
        self.amount_entry.focus()
    
    def show_face_scan(self):
        """Show the face scan screen"""
        self.hide_all_frames()
        self.face_scan_frame.pack(expand=True, fill='both')
        self.current_frame = self.face_scan_frame
        
        # Update amount display
        current_amount = self.transaction_manager.get_current_amount()
        if current_amount:
            self.amount_display_label.config(text=f"Amount: ₹{current_amount}")
    
    def show_pin_entry(self):
        """Show the PIN entry screen"""
        self.hide_all_frames()
        self.pin_frame.pack(expand=True, fill='both')
        self.current_frame = self.pin_frame
        
        # Update payment info
        current_amount = self.transaction_manager.get_current_amount()
        if self.current_user and current_amount:
            self.payment_info_label.config(
                text=f"Payment: ₹{current_amount} by {self.current_user}"
            )
        
        self.pin_entry.focus()
    
    def show_result(self, success: bool, message: str):
        """Show the result screen"""
        self.hide_all_frames()
        self.result_frame.pack(expand=True, fill='both')
        self.current_frame = self.result_frame
        
        # Set result message
        if success:
            self.result_label.config(text=message, fg='#27ae60')
        else:
            self.result_label.config(text=message, fg='#e74c3c')
        
        # Set transaction details
        current_amount = self.transaction_manager.get_current_amount()
        if self.current_user and current_amount:
            details = f"User: {self.current_user}\nAmount: ₹{current_amount}"
            self.transaction_details_label.config(text=details)
    
    def hide_all_frames(self):
        """Hide all frames"""
        self.amount_frame.pack_forget()
        self.face_scan_frame.pack_forget()
        self.pin_frame.pack_forget()
        self.result_frame.pack_forget()
    
    def proceed_to_face_scan(self, event=None):
        """Proceed from amount entry to face scan"""
        amount = self.amount_entry.get().strip()
        
        if not amount:
            messagebox.showerror("Error", "Please enter an amount")
            return
        
        try:
            # Convert to float and validate
            amount_float = float(amount)
            if amount_float <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
            
            # Start new transaction
            transaction_id = self.transaction_manager.start_new_transaction(f"{amount_float:.2f}")
            
            # Clear amount entry
            self.amount_entry.delete(0, tk.END)
            
            # Proceed to face scan
            self.show_face_scan()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def start_face_scan(self):
        """Start face recognition in a separate thread"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scan_button.config(text="Scanning...", state='disabled')
        self.status_label.config(text="Scanning for face...")
        
        # Start recognition in separate thread
        self.recognition_thread = threading.Thread(target=self._face_recognition_worker)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
    
    def _face_recognition_worker(self):
        """Worker thread for face recognition"""
        try:
            success, username = self.face_module.start_recognition()
            
            # Update GUI in main thread
            self.root.after(0, self._on_recognition_complete, success, username)
        except Exception as e:
            print(f"❌ Error during face recognition: {e}")
            self.root.after(0, self._on_recognition_complete, False, None)
    
    def _on_recognition_complete(self, success: bool, username: Optional[str]):
        """Handle face recognition completion"""
        self.is_scanning = False
        self.scan_button.config(text="Start Face Scan", state='normal')
        
        if success and username:
            self.current_user = username
            self.transaction_manager.set_user(username)
            self.status_label.config(text=f"Face recognized: {username}")
            self.user_label.config(text=f"Welcome, {username}!")
            
            # Check if user has PIN
            if not self.pin_module.user_exists(username):
                messagebox.showwarning(
                    "No PIN Found",
                    f"User '{username}' doesn't have a PIN set.\nPlease register a PIN first."
                )
                return
            
            # Proceed to PIN entry
            self.show_pin_entry()
        else:
            self.status_label.config(text="Face not recognized")
            self.current_user = None
            self.user_label.config(text="")
    
    def verify_pin(self, event=None):
        """Verify PIN and process payment"""
        if not self.current_user:
            messagebox.showerror("Error", "No user recognized. Please scan your face first.")
            return
        
        pin = self.pin_entry.get().strip()
        if not pin:
            messagebox.showerror("Error", "Please enter your PIN")
            return
        
        # Verify PIN
        if self.pin_module.verify_pin(self.current_user, pin):
            # Payment successful
            self.transaction_manager.verify_pin(True)
            current_amount = self.transaction_manager.get_current_amount()
            success_message = f"Payment of ₹{current_amount} by {self.current_user} is successful ✅"
            self.show_result(True, success_message)
            self.clear_pin_entry()
        else:
            # Payment failed
            self.transaction_manager.verify_pin(False)
            error_message = "❌ Incorrect PIN. Payment Failed."
            self.show_result(False, error_message)
            self.clear_pin_entry()
        
        # Complete and save transaction
        self.transaction_manager.complete_transaction()
    
    def new_transaction(self):
        """Start a new transaction"""
        # Reset transaction state
        self.transaction_manager.reset_transaction()
        self.current_user = None
        
        # Clear all entries
        self.amount_entry.delete(0, tk.END)
        self.clear_pin_entry()
        
        # Reset labels
        self.status_label.config(text="Ready to scan")
        self.user_label.config(text="")
        self.amount_display_label.config(text="")
        self.payment_info_label.config(text="")
        
        # Go back to amount entry
        self.show_amount_entry()
    
    def register_user(self):
        """Register a new user"""
        # Get user name
        name = simpledialog.askstring("Register User", "Enter your name:")
        if not name:
            return
        
        name = name.strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        
        # Register face
        if self.face_module.register_face(name):
            # Get PIN
            pin = simpledialog.askstring("Set PIN", f"Enter a 4-6 digit PIN for {name}:", show='*')
            if pin:
                if self.pin_module.set_pin(name, pin):
                    messagebox.showinfo("Success", f"User '{name}' registered successfully!")
                else:
                    messagebox.showerror("Error", "Invalid PIN format. PIN must be 4-6 digits.")
        else:
            messagebox.showerror("Error", "Face registration failed")
    
    def clear_pin_entry(self):
        """Clear PIN entry field"""
        self.pin_entry.delete(0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_scanning:
            self.face_module.stop_recognition()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop() 