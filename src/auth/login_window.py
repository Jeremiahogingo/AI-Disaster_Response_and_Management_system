"""Login window for Disaster_Management_System."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os
from .auth_manager import AuthManager

class LoginWindow(QMainWindow):
    """Login window for the application."""
    
    login_successful = pyqtSignal(dict)
    switch_to_signup = pyqtSignal()
    switch_to_forgot_password = pyqtSignal()
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager or AuthManager()
        self.setup_window()
        self.setup_ui()
        self.setup_styles()
        
    def setup_window(self):
        """Setup the main window properties."""
        self.setWindowTitle("Disaster Management System - Login")
        self.setFixedSize(1200, 700)
        
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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create and add left panel (branding)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # Create and add right panel (login form)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)
        
    def create_left_panel(self):
        """Create the left panel with branding."""
        left_panel = QFrame()
        left_panel.setObjectName("left-panel")
        left_panel.setFixedWidth(550)  # Slightly reduced to make room
        
        layout = QVBoxLayout(left_panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        # Add logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_large.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if pixmap and not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                logo_label.setFixedSize(320, 320)
        else:
            # Fallback text if logo not found
            logo_label.setText("🚨 DisasterConnect")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("font-size: 48px; color: white;")
        
        # Add welcome text
        welcome_label = QLabel("Welcome to DisasterConnect")
        welcome_label.setObjectName("welcome-text")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        
        description_label = QLabel("Your comprehensive disaster management solution for coordinating emergency responses and resources")
        description_label.setObjectName("description-text")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setMaximumWidth(450)
        
        # Add feature points
        features_frame = QFrame()
        features_frame.setObjectName("features-frame")
        features_layout = QVBoxLayout(features_frame)
        features_layout.setSpacing(10)
        
        features = [
            "✅ Real-time emergency coordination",
            "✅ Resource management and tracking",
            "✅ Multi-agency collaboration",
            "✅ Crisis communication tools"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setObjectName("feature-text")
            feature_label.setAlignment(Qt.AlignLeft)
            features_layout.addWidget(feature_label)
        
        layout.addStretch(1)
        layout.addWidget(logo_label)
        layout.addWidget(welcome_label)
        layout.addWidget(description_label)
        layout.addWidget(features_frame)
        layout.addStretch(1)
        
        return left_panel
    
    def create_right_panel(self):
        """Create the right panel with login form."""
        right_panel = QFrame()
        right_panel.setObjectName("right-panel")
        right_panel.setFixedWidth(650) 
        
        layout = QVBoxLayout(right_panel)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create login form container
        form_container = QFrame()
        form_container.setObjectName("form-container")
        form_container.setFixedWidth(550) 
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        form_layout.setContentsMargins(40, 40, 40, 40)
        
        # Login title with icon
        title_container = QHBoxLayout()
        title_container.setAlignment(Qt.AlignCenter)
        
        # You can add an icon here if you have one
        title = QLabel("🔐 Login to Your Account")
        title.setObjectName("form-title")
        title.setAlignment(Qt.AlignCenter)
        
        title_container.addWidget(title)
        
        # Email field
        email_label = QLabel("Email Address")
        email_label.setObjectName("input-label")
        self.email_input = QLineEdit()
        self.email_input.setObjectName("input-field")
        self.email_input.setPlaceholderText("Enter your registered email")
        self.email_input.setFixedHeight(50)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("input-label")
        self.password_input = QLineEdit()
        self.password_input.setObjectName("input-field")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Login button
        login_button = QPushButton("Login to Dashboard")
        login_button.setObjectName("primary-button")
        login_button.setFixedHeight(55)
        login_button.clicked.connect(self.handle_login)
        
        # Links row - Forgot Password and Create Account side by side
        links_container = QFrame()
        links_container.setObjectName("links-container")
        links_layout = QHBoxLayout(links_container)
        links_layout.setContentsMargins(0, 0, 0, 0)
        links_layout.setSpacing(20)
        
        # Forgot Password link
        forgot_button = QPushButton("🔓 Forgot Password?")
        forgot_button.setObjectName("link-button")
        forgot_button.clicked.connect(self.show_forgot_password)
        
        # Separator
        separator = QLabel("|")
        separator.setObjectName("separator-text")
        separator.setAlignment(Qt.AlignCenter)
        
        # Create Account link
        signup_button = QPushButton("📝 Create Account")
        signup_button.setObjectName("link-button")
        signup_button.clicked.connect(self.show_signup)
        
        links_layout.addStretch()
        links_layout.addWidget(forgot_button)
        links_layout.addWidget(separator)
        links_layout.addWidget(signup_button)
        links_layout.addStretch()
        
        # Additional info
        info_label = QLabel("Secure login with encrypted credentials")
        info_label.setObjectName("info-text")
        info_label.setAlignment(Qt.AlignCenter)
        
        # Demo credentials hint (remove in production)
        demo_label = QLabel("Demo: admin@disaster.com / password123")
        demo_label.setObjectName("demo-text")
        demo_label.setAlignment(Qt.AlignCenter)
        
        # Add all elements to form
        form_layout.addLayout(title_container)
        form_layout.addSpacing(20)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addSpacing(15)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(25)
        form_layout.addWidget(login_button)
        form_layout.addSpacing(15)
        form_layout.addWidget(links_container)
        form_layout.addSpacing(10)
        form_layout.addWidget(info_label)
        form_layout.addSpacing(5)
        form_layout.addWidget(demo_label)
        
        # Add form to right panel
        layout.addWidget(form_container)
        
        return right_panel
    
    def setup_styles(self):
        """Setup the stylesheet for the window."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            #left-panel {
                background-color: #2C3E50;
                border: none;
            }
            
            #right-panel {
                background-color: white;
                border: none;
            }
            
            #features-frame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                max-width: 450px;
            }
            
            #welcome-text {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
                padding: 0 20px;
            }
            
            #description-text {
                color: #bbdefb;
                font-size: 16px;
                padding: 0 30px;
            }
            
            #feature-text {
                color: #e3f2fd;
                font-size: 14px;
                padding: 5px 0;
            }
            
            #form-container {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
            
            #form-title {
                color: #2C3E50;
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            #input-label {
                color: #34495e;
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            #input-field {
                padding: 15px;
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                font-size: 16px;
                background-color: #f8fafc;
                color: #2d3748;
            }
            
            #input-field:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
            
            #primary-button {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 17px;
                font-weight: 600;
                padding: 12px;
            }
            
            #primary-button:hover {
                background-color: #2980b9;
            }
            
            #primary-button:disabled {
                background-color: #bdc3c7;
            }
            
            #links-container {
                margin: 0;
                padding: 0;
            }
            
            #link-button {
                background: none;
                border: none;
                color: #3498db;
                font-size: 15px;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 4px;
            }
            
            #link-button:hover {
                color: #2980b9;
                text-decoration: underline;
            }
            
            #separator-text {
                color: #bdc3c7;
                font-size: 14px;
                font-weight: normal;
            }
            
            #info-text {
                color: #7f8c8d;
                font-size: 13px;
                font-style: italic;
                margin: 5px;
            }
            
            #demo-text {
                color: #95a5a6;
                font-size: 12px;
                font-style: italic;
                margin: 5px;
                background-color: #f8f9fa;
                padding: 8px;
                border-radius: 4px;
                border: 1px dashed #bdc3c7;
            }
            
            QLabel, QPushButton, QLineEdit {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
    
    def handle_login(self):
        """Handle login button click with actual authentication."""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Error", 
                              "Please enter both email and password.",
                              QMessageBox.Ok)
            return
        
        # Show loading state
        original_text = self.sender().text() if hasattr(self.sender(), 'text') else "Login"
        if hasattr(self.sender(), 'setText'):
            self.sender().setText("Authenticating...")
            self.sender().setEnabled(False)
        
        try:
            # Use auth_manager for authentication
            user_data = self.auth_manager.login(email, password)
            
            if user_data:
                self.login_successful.emit(user_data)
            else:
                QMessageBox.warning(self, "Login Error", 
                                  "Invalid email or password.\n\nPlease check your credentials and try again.",
                                  QMessageBox.Ok)
                
        except Exception as e:
            QMessageBox.critical(self, "Login Error", 
                               f"An error occurred during login:\n\n{str(e)}",
                               QMessageBox.Ok)
        finally:
            # Restore button state
            if hasattr(self.sender(), 'setText'):
                self.sender().setText("Login to Dashboard")
                self.sender().setEnabled(True)
    
    def show_signup(self):
        """Emit signal to switch to signup window."""
        self.switch_to_signup.emit()
    
    def show_forgot_password(self):
        """Emit signal to switch to forgot password window."""
        self.switch_to_forgot_password.emit()
    
    def clear_form(self):
        """Clear login form fields."""
        self.email_input.clear()
        self.password_input.clear()
        self.email_input.setFocus()