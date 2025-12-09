#src/auth/signup_widget.py
"""Signup window for Disaster_Management_System."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
                           QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import os
import re
from datetime import datetime
from .auth_manager import AuthManager 

class SignupWindow(QMainWindow):
    signup_successful = pyqtSignal(dict)
    switch_to_login = pyqtSignal()
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager or AuthManager() 
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """Setup the main window properties."""
        self.setWindowTitle("Disaster Management System - Create Account")
        self.setFixedSize(900, 600)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel (logo and welcome message)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # Create right panel (signup form)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)
        
        self.setStyleSheet(self.get_stylesheet())
    
    def create_left_panel(self):
        """Create the left panel with branding."""
        left_panel = QFrame()
        left_panel.setObjectName("auth-panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Add logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_large.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if pixmap and not pixmap.isNull():
                logo_label.setPixmap(pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                logo_label.setStyleSheet("margin-bottom: 20px;")
        
        # Add welcome message
        welcome_label = QLabel("Join Disaster Management System")
        welcome_label.setObjectName("welcome-text")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        
        description_label = QLabel("Create your account to start coordinating emergency responses effectively")
        description_label.setObjectName("description-text")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(welcome_label)
        left_layout.addWidget(description_label)
        
        return left_panel
    
    def create_right_panel(self):
        """Create the right panel with signup form."""
        right_panel = QFrame()
        right_panel.setObjectName("auth-panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Add signup form
        signup_label = QLabel("Create your account")
        signup_label.setObjectName("form-title")
        signup_label.setAlignment(Qt.AlignCenter)
        
        # Full Name
        name_container = QFrame()
        name_container.setObjectName("input-container")
        name_layout = QHBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name *")
        self.first_name_input.setObjectName("auth-input")
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name *")
        self.last_name_input.setObjectName("auth-input")
        
        name_layout.addWidget(self.first_name_input)
        name_layout.addWidget(self.last_name_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address *")
        self.email_input.setObjectName("auth-input")
        
        # Organization and Role
        org_container = QFrame()
        org_container.setObjectName("input-container")
        org_layout = QHBoxLayout(org_container)
        org_layout.setContentsMargins(0, 0, 0, 0)
        
        self.org_input = QLineEdit()
        self.org_input.setPlaceholderText("Organization")
        self.org_input.setObjectName("auth-input")
        
        self.role_input = QComboBox()
        self.role_input.addItems([
            "Emergency Responder",
            "Coordinator",
            "Administrator",
            "Medical Staff",
            "Logistics",
            "Other"
        ])
        self.role_input.setObjectName("auth-input")
        
        org_layout.addWidget(self.org_input)
        org_layout.addWidget(self.role_input)
        
        # Password
        password_container = QFrame()
        password_container.setObjectName("input-container")
        password_layout = QVBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password *")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("auth-input")
        self.password_input.textChanged.connect(self.validate_password)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password *")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setObjectName("auth-input")
        self.confirm_password_input.textChanged.connect(self.validate_password)
        
        self.password_strength_label = QLabel()
        self.password_strength_label.setObjectName("password-strength")
        
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.confirm_password_input)
        password_layout.addWidget(self.password_strength_label)
        
        # Create Account Button
        self.signup_button = QPushButton("Create Account")
        self.signup_button.setObjectName("primary-button")
        self.signup_button.clicked.connect(self.create_account)
        
        # Login Link
        login_container = QFrame()
        login_layout = QHBoxLayout(login_container)
        login_layout.setAlignment(Qt.AlignCenter)
        
        login_label = QLabel("Already have an account?")
        login_button = QPushButton("Log In")
        login_button.setObjectName("link-button")
        login_button.clicked.connect(self.switch_to_login.emit)
        
        login_layout.addWidget(login_label)
        login_layout.addWidget(login_button)
        
        # Add all widgets to right panel
        right_layout.addWidget(signup_label)
        right_layout.addWidget(name_container)
        right_layout.addWidget(self.email_input)
        right_layout.addWidget(org_container)
        right_layout.addWidget(password_container)
        right_layout.addWidget(self.signup_button)
        right_layout.addWidget(login_container)
        
        return right_panel
    
    def get_stylesheet(self):
        """Return the stylesheet for the window."""
        return """
            #auth-panel {
                background: white;
                border-radius: 8px;
                padding: 20px;
                max-width: 400px;
            }
            #welcome-text {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px 0;
            }
            #description-text {
                font-size: 16px;
                color: #7f8c8d;
                margin-bottom: 20px;
            }
            #form-title {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }
            #auth-input {
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                margin: 5px 0;
                font-size: 14px;
            }
            #auth-input:focus {
                border-color: #3498db;
            }
            #primary-button {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 4px;
                font-size: 16px;
                margin: 20px 0;
                min-width: 200px;
            }
            #primary-button:hover {
                background: #2980b9;
            }
            #primary-button:disabled {
                background: #bdc3c7;
            }
            #link-button {
                background: none;
                border: none;
                color: #3498db;
                text-decoration: underline;
                font-size: 14px;
            }
            #link-button:hover {
                color: #2980b9;
            }
            #password-strength {
                font-size: 12px;
                margin-top: 5px;
            }
        """
    
    def validate_password(self):
        """Validate password strength and match."""
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Check password strength
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        is_long_enough = len(password) >= 8
        
        strength = 0
        strength += has_upper + has_lower + has_digit + has_special + is_long_enough
        
        # Update strength label
        if strength == 0:
            self.password_strength_label.setText("")
        elif strength < 3:
            self.password_strength_label.setText("Weak Password")
            self.password_strength_label.setStyleSheet("color: #e74c3c;")
        elif strength < 5:
            self.password_strength_label.setText("Moderate Password")
            self.password_strength_label.setStyleSheet("color: #f39c12;")
        else:
            self.password_strength_label.setText("Strong Password")
            self.password_strength_label.setStyleSheet("color: #27ae60;")
        
        # Check if passwords match
        if confirm_password and password != confirm_password:
            self.password_strength_label.setText("Passwords do not match")
            self.password_strength_label.setStyleSheet("color: #e74c3c;")
    
    def create_account(self):
        """Create a new user account using auth_manager."""
        # Validate inputs
        if not all([
            self.first_name_input.text().strip(),
            self.last_name_input.text().strip(),
            self.email_input.text().strip(),
            self.password_input.text(),
            self.confirm_password_input.text()
        ]):
            QMessageBox.warning(self, "Validation Error", 
                              "Please fill in all required fields (*).")
            return
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email_input.text().strip()):
            QMessageBox.warning(self, "Validation Error", 
                              "Please enter a valid email address.")
            return
        
        # Validate password match
        if self.password_input.text() != self.confirm_password_input.text():
            QMessageBox.warning(self, "Validation Error", 
                              "Passwords do not match.")
            return
        
        try:
            # Create user document
            user_data = {
                "first_name": self.first_name_input.text().strip(),
                "last_name": self.last_name_input.text().strip(),
                "email": self.email_input.text().strip().lower(),
                "organization": self.org_input.text().strip(),
                "role": self.role_input.currentText(),
                "password": self.password_input.text(),
                "created_at": datetime.utcnow(),
                "last_login": None,
                "is_active": True
            }
            
            # Use auth_manager to register user
            if self.auth_manager.register_user(user_data):
                QMessageBox.information(self, "Success", 
                                      "Account created successfully! Please log in.")
                self.switch_to_login.emit()
            else:
                QMessageBox.warning(self, "Account Exists", 
                                  "An account with this email already exists.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to create account: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields."""
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.org_input.clear()
        self.role_input.setCurrentIndex(0)
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.password_strength_label.clear()