"""
Main Application Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.login_window import LoginWindow
from gui.admin_dashboard import AdminDashboard
from gui.user_dashboard import UserDashboard
from gui.styles import MODERN_STYLESHEET
from config import APP_NAME, APP_VERSION

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    while True:
        # Login window
        login_window = LoginWindow()
        login_window.setStyleSheet(MODERN_STYLESHEET)
        
        if login_window.exec_() == LoginWindow.Accepted:
            user = login_window.get_logged_in_user()
            
            if user:
                try:
                    # Create appropriate dashboard based on user role
                    if user.role == 1:  # Admin
                        dashboard = AdminDashboard(user)
                    else:  # Teacher or Student
                        dashboard = UserDashboard(user)
                    
                    dashboard.setStyleSheet(MODERN_STYLESHEET)
                    dashboard.show()
                    
                    # Run the app event loop
                    app.exec_()
                    # After dashboard closes, loop back to login screen
                    
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to load dashboard:\n{str(e)}")
                    sys.exit(1)
            else:
                QMessageBox.critical(None, "Error", "Failed to load user information")
                sys.exit(1)
        else:
            sys.exit(0)

if __name__ == '__main__':
    main()
