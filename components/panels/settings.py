import customtkinter as ctk
import json
import os
import random
import smtplib
from email.message import EmailMessage
import time

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.verification_code = None
        self.code_expiry = None
        self.temp_credentials = {}
        self._create_widgets()
    
    def _create_widgets(self):
       
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 28, "bold"),
            text_color=("#2B65EC", "#4FC3F7")
        )
        self.header.grid(row=0, column=0, pady=(30, 20), sticky="n")
        
 
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=1, column=0, sticky="nsew", padx=100)
        
   
        self.make_setting(
            "Appearance Mode:", 
            ["Light", "Dark", "System"],
            self.change_appearance,
            icon="🌓"
        )
        
        self.create_account_section()
    
    def create_account_section(self):
        """Create the account login/creation UI"""
        account_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        account_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            account_frame,
            text="🔐 Account",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Check if user is already logged in
        if self.check_existing_credentials():
            self.show_account_status(account_frame)
        else:
            self.show_login_creation_ui(account_frame)
    
    def show_account_status(self, parent_frame):
        """Show logged in status"""
        with open("creds.json", "r") as f:
            creds = json.load(f)
        
        ctk.CTkLabel(
            parent_frame,
            text=f"Logged in as: {creds['email']}",
            font=("Arial", 14)
        ).pack(anchor="w")
        
        logout_btn = ctk.CTkButton(
            parent_frame,
            text="Logout",
            command=self.logout,
            width=100,
            fg_color="#FF5555",
            hover_color="#FF3333"
        )
        logout_btn.pack(anchor="w", pady=10)
    
    def show_login_creation_ui(self, parent_frame):
        """Show login/account creation UI"""
        self.login_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.login_frame.pack(fill="x")
        
        # Email Entry
        ctk.CTkLabel(
            self.login_frame,
            text="Email:",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10)
        
        self.email_entry = ctk.CTkEntry(self.login_frame)
        self.email_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Password Entry
        ctk.CTkLabel(
            self.login_frame,
            text="Password:",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10)
        
        self.password_entry = ctk.CTkEntry(self.login_frame, show="•")
        self.password_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Login",
            command=self.attempt_login,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Create Account",
            command=self.start_account_creation,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color=("#FF0000", "#FF5555")
        )
        self.status_label.pack(anchor="w", padx=10)
    
    def check_existing_credentials(self):
        """Check if creds.json exists and is valid"""
        if not os.path.exists("creds.json"):
            return False
        
        try:
            with open("creds.json", "r") as f:
                creds = json.load(f)
                return bool(creds.get("email")) and bool(creds.get("password"))
        except:
            return False
    
    def attempt_login(self):
        """Try to log in with provided credentials"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.status_label.configure(text="Please enter both email and password")
            return
            
        if not os.path.exists("creds.json"):
            self.status_label.configure(text="No account found. Please create one.")
            return
            
        try:
            with open("creds.json", "r") as f:
                creds = json.load(f)
                
                if creds["email"] == email and creds["password"] == password:
                    self.status_label.configure(text="Login successful!", text_color=("#00AA00", "#55FF55"))
                    self.login_frame.pack_forget()
                    self.create_account_section()
                else:
                    self.status_label.configure(text="Invalid email or password")
        except:
            self.status_label.configure(text="Error reading account data")
    
    def start_account_creation(self):
        """Begin the account creation process"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.status_label.configure(text="Please enter both email and password")
            return
            
        if len(password) < 8:
            self.status_label.configure(text="Password must be at least 8 characters")
            return
            
        # Store temp credentials
        self.temp_credentials = {
            "email": email,
            "password": password
        }
        
        # Generate verification code
        self.verification_code = str(random.randint(100000, 999999))
        self.code_expiry = time.time() + 300  # 5 minutes from now
        
        # Send verification email
        if self.send_verification_email(email):
            self.show_verification_ui()
        else:
            self.status_label.configure(text="Failed to send verification email")
    
    def send_verification_email(self, recipient):
        """Send verification code to email"""
        try:
            # Configure email settings
            sender_email = ""  
            sender_password = ""  
            
            msg = EmailMessage()
            msg['Subject'] = "Your Verification Code"
            msg['From'] = sender_email
            msg['To'] = recipient
            msg.set_content(f"Your verification code is: {self.verification_code}")
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def show_verification_ui(self):
        """Show verification code input UI"""
        self.login_frame.pack_forget()
        
        self.verify_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.verify_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            self.verify_frame,
            text="Enter verification code sent to your email:",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10)
        
        self.code_entry = ctk.CTkEntry(self.verify_frame)
        self.code_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(self.verify_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Verify",
            command=self.verify_code,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.cancel_verification,
            width=100,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="left", padx=5)
        
        self.verify_status = ctk.CTkLabel(
            self.verify_frame,
            text="",
            text_color=("#FF0000", "#FF5555")
        )
        self.verify_status.pack(anchor="w", padx=10)
    
    def verify_code(self):
        """Verify the entered code"""
        entered_code = self.code_entry.get()
        
        if not entered_code:
            self.verify_status.configure(text="Please enter the verification code")
            return
            
        if time.time() > self.code_expiry:
            self.verify_status.configure(text="Verification code expired")
            return
            
        if entered_code == self.verification_code:
            # Save credentials
            with open("creds.json", "w") as f:
                json.dump(self.temp_credentials, f)
            
            self.verify_frame.pack_forget()
            self.create_account_section()
        else:
            self.verify_status.configure(text="Invalid verification code")
    
    def cancel_verification(self):
        """Cancel the verification process"""
        self.verify_frame.pack_forget()
        self.login_frame.pack(fill="x")
        self.status_label.configure(text="Account creation cancelled")
    
    def logout(self):
        """Log out the user"""
        try:
            os.remove("creds.json")
            self.settings_frame.pack_forget()
            self.create_account_section()
        except:
            pass
    
    def make_setting(self, label_text, options, callback, icon=""):
        """Creates a setting row with label and dropdown"""
        frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame,
            text=f"{icon} {label_text}",
            font=("Arial", 14),
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Dropdown menu
        menu = ctk.CTkOptionMenu(
            frame,
            values=options,
            command=callback,
            fg_color="#2B65EC",
            button_color="#1E4BCC",
            button_hover_color="#163A99"
        )
        menu.pack(side="right", padx=10)
        menu.set(options[0])
    
    def change_appearance(self, choice):
        """When appearance mode changes"""
        ctk.set_appearance_mode(choice.lower())
        print(f"Changed appearance to: {choice}")
