"""
Signup Window Module
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QComboBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.user import User
from gui.styles import MODERN_STYLESHEET
from utils.validation import FormValidator
from config import DEPARTMENTS

class SignupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Smart Campus - Sign Up")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet(MODERN_STYLESHEET)
        
        # Scroll area for long form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Create New Account")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2563EB; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Full Name
        label_fullname = QLabel("Full Name:")
        label_fullname.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_fullname.setMinimumWidth(100)
        label_fullname.setWordWrap(True)
        main_layout.addWidget(label_fullname)
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter your full name")
        self.fullname_input.setMinimumHeight(35)
        main_layout.addWidget(self.fullname_input)
        
        # Username
        label_username = QLabel("Username:")
        label_username.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_username.setMinimumWidth(100)
        label_username.setWordWrap(True)
        main_layout.addWidget(label_username)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username (at least 3 characters)")
        self.username_input.setMinimumHeight(35)
        main_layout.addWidget(self.username_input)
        
        # Email
        label_email = QLabel("Email:")
        label_email.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_email.setMinimumWidth(100)
        label_email.setWordWrap(True)
        main_layout.addWidget(label_email)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        self.email_input.setMinimumHeight(35)
        main_layout.addWidget(self.email_input)
        
        # Phone
        label_phone = QLabel("Phone Number:")
        label_phone.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_phone.setMinimumWidth(100)
        label_phone.setWordWrap(True)
        main_layout.addWidget(label_phone)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setMinimumHeight(35)
        main_layout.addWidget(self.phone_input)
        
        # Department
        label_dept = QLabel("Department:")
        label_dept.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_dept.setMinimumWidth(100)
        label_dept.setWordWrap(True)
        main_layout.addWidget(label_dept)
        self.dept_combo = QComboBox()
        self.dept_combo.addItems(DEPARTMENTS)
        self.dept_combo.setMinimumHeight(35)
        main_layout.addWidget(self.dept_combo)
        
        # Role (Student by default)
        label_role = QLabel("Role:")
        label_role.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_role.setMinimumWidth(100)
        label_role.setWordWrap(True)
        main_layout.addWidget(label_role)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Teacher"])
        self.role_combo.setMinimumHeight(35)
        main_layout.addWidget(self.role_combo)
        
        # Password
        label_password = QLabel("Password:")
        label_password.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_password.setMinimumWidth(100)
        label_password.setWordWrap(True)
        main_layout.addWidget(label_password)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter a strong password (min. 6 characters with digits)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        main_layout.addWidget(self.password_input)
        
        # Confirm Password
        label_confirm = QLabel("Confirm Password:")
        label_confirm.setStyleSheet("color: #E0E7FF; font-weight: bold; margin-bottom: 5px;")
        label_confirm.setMinimumWidth(100)
        label_confirm.setWordWrap(True)
        main_layout.addWidget(label_confirm)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Re-enter your password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setMinimumHeight(35)
        main_layout.addWidget(self.confirm_input)
        
        main_layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        signup_button = QPushButton("Create Account")
        signup_button.setMinimumHeight(40)
        signup_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        signup_button.setObjectName("SuccessButton")
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        signup_button.clicked.connect(self.handle_signup)
        button_layout.addWidget(signup_button)
        
        cancel_button = QPushButton("Back to Login")
        cancel_button.setMinimumHeight(40)
        cancel_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        cancel_button.setObjectName("CancelButton")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)
    
    def handle_signup(self):
        """Handle signup button click"""
        fullname = self.fullname_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validation
        validator = FormValidator()
        data = {
            'fullname': fullname,
            'username': username,
            'email': email,
            'password': password
        }
        
        if not validator.validate_registration_form(data):
            errors = validator.get_errors()
            error_msg = "\n".join([f"{k}: {', '.join(v)}" for k, v in errors.items()])
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        # Check password match
        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", 
                              "Passwords do not match. Please try again.")
            self.password_input.clear()
            self.confirm_input.clear()
            return
        
        # Check if username exists
        if User.username_exists(username):
            QMessageBox.warning(self, "Username Taken", 
                              f"Username '{username}' is already taken. Please choose another.")
            self.username_input.clear()
            self.username_input.setFocus()
            return
        
        # Check if email exists
        if User.email_exists(email):
            QMessageBox.warning(self, "Email in Use", 
                              f"Email '{email}' is already registered. Please use another.")
            self.email_input.clear()
            self.email_input.setFocus()
            return
        
        # Create user
        role = 3 if self.role_combo.currentText() == "Student" else 2
        user = User(
            username=username,
            fullname=fullname,
            email=email,
            password=password,
            phone=phone,
            role=role,
            status=1,
            department=self.dept_combo.currentText()
        )
        
        if user.register():
            QMessageBox.information(self, "Success", 
                                  "Account created successfully! You can now login.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", 
                               "Failed to create account. Please try again.")
