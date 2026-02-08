"""
Dialog Forms for Admin Dashboard
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QSpinBox, QTimeEdit)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont
from models.user import User
from models.classroom import Classroom
from models.schedule import Schedule
from database.db_setup import DatabaseManager
from config import DEPARTMENTS
from utils.validation import FormValidator




class EditUserDialog(QDialog):
    """Dialog for editing user information"""
    
    def __init__(self, user, parent=None):
        try:
            super().__init__(parent)
            self.user = user
            self.validator = FormValidator()
            self.init_ui()
        except Exception as e:
            print(f"EditUserDialog init error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def init_ui(self):
        """Initialize the user interface"""
        try:
            self.setWindowTitle(f"Edit User - {self.user.fullname}")
            self.setGeometry(100, 100, 500, 500)
            self.setModal(True)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Edit User Information")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            layout.addWidget(title)
            
            # Full Name
            layout.addWidget(QLabel("Full Name:"))
            self.fullname_input = QLineEdit()
            self.fullname_input.setText(self.user.fullname if self.user.fullname else "")
            self.fullname_input.setMinimumHeight(35)
            layout.addWidget(self.fullname_input)
            
            # Email
            layout.addWidget(QLabel("Email:"))
            self.email_input = QLineEdit()
            self.email_input.setText(self.user.email if self.user.email else "")
            self.email_input.setMinimumHeight(35)
            layout.addWidget(self.email_input)
            
            # Phone
            layout.addWidget(QLabel("Phone:"))
            self.phone_input = QLineEdit()
            self.phone_input.setText(self.user.phone if self.user.phone else "")
            self.phone_input.setMinimumHeight(35)
            layout.addWidget(self.phone_input)
            
            # Department
            layout.addWidget(QLabel("Department:"))
            self.dept_combo = QComboBox()
            self.dept_combo.addItems(DEPARTMENTS)
            if self.user.department:
                index = self.dept_combo.findText(self.user.department)
                if index >= 0:
                    self.dept_combo.setCurrentIndex(index)
            self.dept_combo.setMinimumHeight(35)
            layout.addWidget(self.dept_combo)
            
            # Status
            layout.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItem("Active", 1)
            self.status_combo.addItem("Inactive", 0)
            # Set current status
            status_value = self.user.status if self.user.status else 1
            status_index = self.status_combo.findData(status_value)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
            self.status_combo.setMinimumHeight(35)
            layout.addWidget(self.status_combo)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_button = QPushButton("Save")
            save_button.setMinimumHeight(40)
            save_button.clicked.connect(self.save_user)
            button_layout.addWidget(save_button)
            
            cancel_button = QPushButton("Cancel")
            cancel_button.setMinimumHeight(40)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
        except Exception as e:
            print(f"EditUserDialog init_ui error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def save_user(self):
        """Save the edited user"""
        try:
            fullname = self.fullname_input.text().strip()
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()
            department = self.dept_combo.currentText()
            status = self.status_combo.currentData()
            
            # Validate inputs
            if not all([fullname, email]):
                QMessageBox.warning(self, "Validation Error", "Full name and email are required!")
                return
            
            # Update user in database
            db = DatabaseManager()
            query = '''
                UPDATE users 
                SET fullname = ?, email = ?, phone = ?, department = ?, status = ?
                WHERE id = ?
            '''
            db.execute_update(query, (fullname, email, phone, department, status, self.user.id))
            
            QMessageBox.information(self, "Success", "User updated successfully!")
            self.accept()
        except Exception as e:
            print(f"Save user error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to update user:\n{str(e)}")


class AddUserDialog(QDialog):
    """Dialog for adding a new user"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.validator = FormValidator()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Add New User")
        self.setGeometry(100, 100, 500, 500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Add New User")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Full Name
        layout.addWidget(QLabel("Full Name:"))
        self.fullname_input = QLineEdit()
        self.fullname_input.setMinimumHeight(35)
        layout.addWidget(self.fullname_input)
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setMinimumHeight(35)
        layout.addWidget(self.username_input)
        
        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setMinimumHeight(35)
        layout.addWidget(self.email_input)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        layout.addWidget(self.password_input)
        
        # Phone
        layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        self.phone_input.setMinimumHeight(35)
        layout.addWidget(self.phone_input)
        
        # Role
        layout.addWidget(QLabel("Role:"))
        self.role_combo = QComboBox()
        self.role_combo.addItem("Admin", 1)
        self.role_combo.addItem("Teacher", 2)
        self.role_combo.addItem("Student", 3)
        self.role_combo.setMinimumHeight(35)
        layout.addWidget(self.role_combo)
        
        # Department
        layout.addWidget(QLabel("Department:"))
        self.dept_combo = QComboBox()
        self.dept_combo.addItems(DEPARTMENTS)
        self.dept_combo.setMinimumHeight(35)
        layout.addWidget(self.dept_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setMinimumHeight(40)
        save_button.clicked.connect(self.save_user)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_user(self):
        """Save the new user"""
        fullname = self.fullname_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        phone = self.phone_input.text().strip()
        role = self.role_combo.currentData()
        department = self.dept_combo.currentText()
        
        # Validate inputs
        if not all([fullname, username, email, password, phone]):
            QMessageBox.warning(self, "Validation Error", "All fields are required!")
            return
        
        try:
            user = User(
                username=username,
                fullname=fullname,
                email=email,
                password=password,
                phone=phone,
                role=role,
                department=department
            )
            
            if user.register():
                QMessageBox.information(self, "Success", "User added successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to add user. Username or email may already exist.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding user: {str(e)}")


class AddClassroomDialog(QDialog):
    """Dialog for adding a new classroom"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Add New Classroom")
        self.setGeometry(100, 100, 400, 500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Add New Classroom")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Room Number
        layout.addWidget(QLabel("Room Number:"))
        self.room_number_input = QLineEdit()
        self.room_number_input.setMinimumHeight(35)
        layout.addWidget(self.room_number_input)
        
        # Room Type
        layout.addWidget(QLabel("Room Type:"))
        self.room_type_input = QLineEdit()
        self.room_type_input.setPlaceholderText("e.g., Lecture Hall, Lab, Seminar")
        self.room_type_input.setMinimumHeight(35)
        layout.addWidget(self.room_type_input)
        
        # Building
        layout.addWidget(QLabel("Building:"))
        self.building_input = QLineEdit()
        self.building_input.setMinimumHeight(35)
        layout.addWidget(self.building_input)
        
        # Floor
        layout.addWidget(QLabel("Floor:"))
        self.floor_spin = QSpinBox()
        self.floor_spin.setMinimum(0)
        self.floor_spin.setMaximum(20)
        self.floor_spin.setMinimumHeight(35)
        layout.addWidget(self.floor_spin)
        
        # Capacity
        layout.addWidget(QLabel("Capacity:"))
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setMinimum(1)
        self.capacity_spin.setMaximum(500)
        self.capacity_spin.setValue(30)
        self.capacity_spin.setMinimumHeight(35)
        layout.addWidget(self.capacity_spin)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_input = QLineEdit()
        self.description_input.setMinimumHeight(35)
        layout.addWidget(self.description_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setMinimumHeight(40)
        save_button.clicked.connect(self.save_classroom)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_classroom(self):
        """Save the new classroom"""
        room_number = self.room_number_input.text().strip()
        room_type = self.room_type_input.text().strip()
        building = self.building_input.text().strip()
        floor = self.floor_spin.value()
        capacity = self.capacity_spin.value()
        description = self.description_input.text().strip()
        
        if not all([room_number, room_type, building]):
            QMessageBox.warning(self, "Validation Error", "Please enter room number, room type, and building!")
            return
        
        try:
            classroom = Classroom(
                room_number=room_number,
                room_type=room_type,
                building=building,
                floor=floor,
                capacity=capacity,
                description=description
            )
            
            if classroom.create():
                QMessageBox.information(self, "Success", "Classroom added successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to add classroom.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding classroom: {str(e)}")


class AddScheduleDialog(QDialog):
    """Dialog for adding a new schedule"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Add New Schedule")
        self.setGeometry(100, 100, 400, 550)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Add New Schedule")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Teacher
        layout.addWidget(QLabel("Teacher:"))
        self.teacher_combo = QComboBox()
        self.load_teachers()
        self.teacher_combo.setMinimumHeight(35)
        layout.addWidget(self.teacher_combo)
        
        # Classroom
        layout.addWidget(QLabel("Classroom:"))
        self.classroom_combo = QComboBox()
        self.load_classrooms()
        self.classroom_combo.setMinimumHeight(35)
        layout.addWidget(self.classroom_combo)
        
        # Course Name
        layout.addWidget(QLabel("Course Name:"))
        self.course_input = QLineEdit()
        self.course_input.setMinimumHeight(35)
        layout.addWidget(self.course_input)
        
        # Day of Week
        layout.addWidget(QLabel("Day of Week:"))
        self.day_combo = QComboBox()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_combo.addItems(days)
        self.day_combo.setMinimumHeight(35)
        layout.addWidget(self.day_combo)
        
        # Start Time
        layout.addWidget(QLabel("Start Time:"))
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime(9, 0))
        self.start_time.setMinimumHeight(35)
        layout.addWidget(self.start_time)
        
        # End Time
        layout.addWidget(QLabel("End Time:"))
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime(10, 0))
        self.end_time.setMinimumHeight(35)
        layout.addWidget(self.end_time)
        
        # Semester
        layout.addWidget(QLabel("Semester:"))
        self.semester_input = QLineEdit()
        self.semester_input.setPlaceholderText("e.g., Spring 2026, Fall 2025")
        self.semester_input.setMinimumHeight(35)
        layout.addWidget(self.semester_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setMinimumHeight(40)
        save_button.clicked.connect(self.save_schedule)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_teachers(self):
        """Load teachers from database"""
        try:
            db = DatabaseManager()
            query = 'SELECT id, fullname FROM users WHERE role = 2'
            results = db.execute_query(query)
            if results:
                for teacher in results:
                    self.teacher_combo.addItem(teacher[1], teacher[0])
        except Exception as e:
            print(f"Error loading teachers: {e}")
    
    def load_classrooms(self):
        """Load classrooms from database"""
        try:
            classrooms = Classroom.get_all_classrooms()
            if classrooms:
                for classroom in classrooms:
                    self.classroom_combo.addItem(f"{classroom.room_number} - {classroom.building}", classroom.id)
        except Exception as e:
            print(f"Error loading classrooms: {e}")
    
    def save_schedule(self):
        """Save the new schedule"""
        teacher_id = self.teacher_combo.currentData()
        classroom_id = self.classroom_combo.currentData()
        course_name = self.course_input.text().strip()
        day = self.day_combo.currentText()
        start_time = self.start_time.time().toString("HH:mm")
        end_time = self.end_time.time().toString("HH:mm")
        semester = self.semester_input.text().strip()
        
        if not all([teacher_id, classroom_id, course_name, semester]):
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields!")
            return
        
        try:
            schedule = Schedule(
                teacher_id=teacher_id,
                classroom_id=classroom_id,
                course_name=course_name,
                day_of_week=day,
                start_time=start_time,
                end_time=end_time,
                semester=semester
            )
            
            if schedule.create():
                QMessageBox.information(self, "Success", "Schedule added successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to add schedule.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding schedule: {str(e)}")
