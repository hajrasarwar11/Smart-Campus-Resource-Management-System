"""
Login Window Module
"""

import sys
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from models.user import User
from gui.styles import MODERN_STYLESHEET, TITLE_STYLE
from utils.validation import FormValidator

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.logged_in_user = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Smart Campus - Login")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet(MODERN_STYLESHEET)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Smart Campus Resource Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2563EB; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Login to Your Account")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6B7280; margin-bottom: 30px;")
        main_layout.addWidget(subtitle)
        
        # Username
        username_label = QLabel("Username or Email:")
        username_label.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username or email")
        self.username_input.setMinimumHeight(40)
        main_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        main_layout.addWidget(self.password_input)
        
        # Remember me
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 9))
        main_layout.addWidget(self.remember_checkbox)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(40)
        login_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(login_button)
        
        signup_button = QPushButton("Sign Up")
        signup_button.setMinimumHeight(40)
        signup_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        signup_button.setObjectName("SignupButton")
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        signup_button.clicked.connect(self.open_signup)
        button_layout.addWidget(signup_button)
        
        main_layout.addLayout(button_layout)
        
        # Footer
        main_layout.addStretch()
        footer = QLabel("© 2026 Smart Campus. All rights reserved.")
        footer.setFont(QFont("Segoe UI", 8))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #9CA3AF;")
        main_layout.addWidget(footer)
        
        # Connect keyboard shortcuts
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        validator = FormValidator()
        if not validator.validate_login_form(username, password):
            error_msg = "\n".join(list(validator.get_errors().values())[0])
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        # Attempt login
        user = User.login(username, password)
        
        if user:
            self.logged_in_user = user
            QMessageBox.information(self, "Success", f"Welcome back, {user.fullname}!")
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", 
                               "Invalid username/email or password. Please try again.")
            self.password_input.clear()
            self.username_input.setFocus()
    
    def open_signup(self):
        """Open signup dialog"""
        from gui.signup_window import SignupWindow
        signup = SignupWindow(self)
        if signup.exec_():
            QMessageBox.information(self, "Success", 
                                  "Account created successfully! Please login with your credentials.")
    
    def get_logged_in_user(self):
        """Get the logged-in user"""
        return self.logged_in_user
