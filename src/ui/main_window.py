#src/ui/main_window.py
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from ..dashboard.dashboard_widget import DashboardWidget
from ..incidents.incidents_widget import IncidentWidget
from ..resources.resources_widget import ResourcesWidget
from ..auth.login_widget import LoginWidget
from ..utils.mongodb_client import get_mongodb_client
import os

class MainWindow(QMainWindow):
    # Add logout signal
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data=None):
        super().__init__()
        
        # Store user data if provided
        self.user_data = user_data
        
        self.setWindowTitle("Disaster Management System")
        
        # Set initial size - smaller for login, will be maximized after login
        if user_data:
            # If user data provided, start maximized
            self.showMaximized()
            self.setWindowTitle(f"Disaster Management System - Welcome {user_data.get('username', 'User')}")
        else:
            # If no user data, show login size
            self.setGeometry(100, 100, 400, 500)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'resources', 'images', 'logo_new.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Initialize authentication (only if no user data provided)
        self.login_widget = LoginWidget(self)
        self.login_widget.login_success.connect(self.on_login_success)
        
        # Initialize main content
        self.main_content = QWidget()
        self.main_layout = QVBoxLayout(self.main_content)
        
        # Add logout button in a horizontal layout at the top
        top_bar = QHBoxLayout()
        top_bar.addStretch()  # Push the logout button to the right
        
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        top_bar.addWidget(self.logout_button)
        
        self.main_layout.addLayout(top_bar)
        
        # Add tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Initialize tabs
        self.init_tabs()
        
        # Add both widgets to layout
        self.layout.addWidget(self.login_widget)
        self.layout.addWidget(self.main_content)
        
        # Show appropriate content based on whether user data is provided
        if user_data:
            # User data provided (direct login), skip login screen
            self.login_widget.hide()
            self.main_content.show()
            self.refresh_all_tabs()
        else:
            # No user data, show login screen
            self.login_widget.show()
            self.main_content.hide()
    
    def init_tabs(self):
        """Initialize application tabs"""
        # Dashboard Tab
        self.dashboard = DashboardWidget()
        self.tab_widget.addTab(self.dashboard, "Dashboard")
        
        # Incidents Tab
        self.incidents = IncidentWidget()
        self.tab_widget.addTab(self.incidents, "Incidents")
        
        # Resources Tab
        self.resources = ResourcesWidget()
        self.tab_widget.addTab(self.resources, "Resources")
    
    def on_login_success(self, user_data):
        """Handle successful login from login widget"""
        self.user_data = user_data  # Store user data
        
        print(f"Login successful for user: {user_data.get('username')}")
        
        # Switch to main content
        self.login_widget.hide()
        self.main_content.show()
        
        # Set window to maximum size after login
        self.showMaximized()
        
        # Update window title with username
        self.setWindowTitle(f"Disaster Management System - Welcome {user_data.get('username')}")
        
        # Refresh data in all tabs
        self.refresh_all_tabs()
    
    def refresh_all_tabs(self):
        """Refresh data in all tabs"""
        if hasattr(self, 'dashboard'):
            self.dashboard.refresh_data()
        if hasattr(self, 'incidents'):
            self.incidents.refresh_data()
        if hasattr(self, 'resources'):
            self.resources.refresh_table()
    
    def logout(self):
        """Handle logout"""
        # Clear user data
        self.user_data = None
        
        # Hide main content and show login widget
        self.main_content.hide()
        self.login_widget.show()
        
        # Clear login fields
        if hasattr(self.login_widget, 'clear_fields'):
            self.login_widget.clear_fields()
        
        # Reset window size and title
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle("Disaster Management System")
        
        # Clear data in tabs (optional)
        if hasattr(self.incidents, 'clear_data'):
            self.incidents.clear_data()
        if hasattr(self.dashboard, 'clear_data'):
            self.dashboard.clear_data()
        if hasattr(self.resources, 'clear_data'):
            self.resources.clear_data()
        
        # Emit logout signal for main.py to handle
        self.logout_signal.emit()