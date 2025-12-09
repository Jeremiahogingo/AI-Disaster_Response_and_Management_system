from dotenv import load_dotenv
load_dotenv()

import sys
from PyQt5.QtWidgets import QApplication
from src.auth.login_window import LoginWindow
from src.auth.signup_widget import SignupWindow
from src.auth.forgot_password_widget import ForgotPasswordWindow
from src.ui.main_window import MainWindow
from src.utils.mongodb_client import mongodb_client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point of the Disaster_Management_System application
    """
    try:
        # Initialize the application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Create authentication windows
        login_window = LoginWindow()
        signup_window = SignupWindow()
        forgot_window = ForgotPasswordWindow()
        
        # Connect navigation signals
        login_window.switch_to_signup.connect(signup_window.show)
        login_window.switch_to_signup.connect(login_window.hide)
        
        login_window.switch_to_forgot_password.connect(forgot_window.show)
        login_window.switch_to_forgot_password.connect(login_window.hide)
        
        signup_window.switch_to_login.connect(login_window.show)
        signup_window.switch_to_login.connect(signup_window.hide)
        
        forgot_window.switch_to_login.connect(login_window.show)
        forgot_window.switch_to_login.connect(forgot_window.hide)
        
        # Store reference to main window
        main_window = None
        
        # Handle successful login
        def on_login_success(user_data):
            nonlocal main_window
            
            logger.info(f"User logged in: {user_data.get('email', 'Unknown')}")
            
            # Hide all auth windows
            login_window.hide()
            if signup_window.isVisible():
                signup_window.hide()
            if forgot_window.isVisible():
                forgot_window.hide()
            
            try:
                # Create main window with user data
                main_window = MainWindow(user_data)
                main_window.show()
                
                # Connect logout signal
                main_window.logout_signal.connect(lambda: (
                    main_window.close(),
                    login_window.clear_form(),
                    login_window.show()
                ))
                
            except Exception as e:
                logger.error(f"Failed to create main window: {str(e)}")
                import traceback
                traceback.print_exc()
                # Show error and return to login
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(None, "Error", 
                                   f"Failed to load application:\n\n{str(e)}")
                login_window.show()
        
        login_window.login_successful.connect(on_login_success)
        
        # Show login window first
        login_window.show()
        
        # Start the application event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up resources
        mongodb_client.close_connection()

if __name__ == '__main__':
    main()