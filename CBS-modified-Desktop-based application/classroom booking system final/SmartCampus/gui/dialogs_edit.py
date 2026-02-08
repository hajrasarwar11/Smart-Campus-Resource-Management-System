"""
Edit Dialog Classes for Admin Dashboard
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox, QSpinBox, QTimeEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTime, QDate
from database.db_setup import DatabaseManager
from models.user import User
from models.classroom import Classroom
from models.booking import Booking
from models.schedule import Schedule
from utils.email_notification import EmailNotificationService


class EditClassroomDialog(QDialog):
    """Dialog for editing classroom information"""
    
    def __init__(self, classroom, parent=None):
        try:
            super().__init__(parent)
            self.classroom = classroom
            self.init_ui()
        except Exception as e:
            print(f"EditClassroomDialog init error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def init_ui(self):
        """Initialize the user interface"""
        try:
            self.setWindowTitle(f"Edit Classroom - {self.classroom.room_number}")
            self.setGeometry(100, 100, 500, 450)
            self.setModal(True)
            
            # Apply dark theme styling
            self.setStyleSheet("""
                QDialog {
                    background-color: #1E293B;
                }
                QLabel {
                    color: #E2E8F0;
                    font-size: 11px;
                }
                QLineEdit, QSpinBox, QComboBox {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    border: 2px solid #334155;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                    border: 2px solid #06B6D4;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    background-color: #334155;
                    border: none;
                }
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                    background-color: #475569;
                }
                QComboBox::drop-down {
                    border: none;
                    background-color: #334155;
                }
                QComboBox QAbstractItemView {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    selection-background-color: #06B6D4;
                }
                QPushButton {
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Edit Classroom Information")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            title.setStyleSheet("color: #06B6D4; font-size: 14px; margin-bottom: 10px;")
            layout.addWidget(title)
            
            # Room Number
            layout.addWidget(QLabel("Room Number:"))
            self.room_number_input = QLineEdit()
            self.room_number_input.setText(self.classroom.room_number if self.classroom.room_number else "")
            self.room_number_input.setMinimumHeight(35)
            layout.addWidget(self.room_number_input)
            
            # Room Type
            layout.addWidget(QLabel("Room Type:"))
            self.room_type_input = QLineEdit()
            self.room_type_input.setText(self.classroom.room_type if self.classroom.room_type else "")
            self.room_type_input.setMinimumHeight(35)
            layout.addWidget(self.room_type_input)
            
            # Capacity
            layout.addWidget(QLabel("Capacity:"))
            self.capacity_input = QSpinBox()
            self.capacity_input.setMinimum(1)
            self.capacity_input.setMaximum(500)
            self.capacity_input.setValue(self.classroom.capacity if self.classroom.capacity else 30)
            self.capacity_input.setMinimumHeight(35)
            layout.addWidget(self.capacity_input)
            
            # Building
            layout.addWidget(QLabel("Building:"))
            self.building_input = QLineEdit()
            self.building_input.setText(self.classroom.building if self.classroom.building else "")
            self.building_input.setMinimumHeight(35)
            layout.addWidget(self.building_input)
            
            # Floor
            layout.addWidget(QLabel("Floor:"))
            self.floor_input = QSpinBox()
            self.floor_input.setMinimum(0)
            self.floor_input.setMaximum(10)
            self.floor_input.setValue(self.classroom.floor if self.classroom.floor else 0)
            self.floor_input.setMinimumHeight(35)
            layout.addWidget(self.floor_input)
            
            # Status
            layout.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItem("Active", 1)
            self.status_combo.addItem("Inactive", 0)
            status_value = self.classroom.status if self.classroom.status else 1
            status_index = self.status_combo.findData(status_value)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
            self.status_combo.setMinimumHeight(35)
            layout.addWidget(self.status_combo)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_button = QPushButton("Save")
            save_button.setMinimumHeight(40)
            save_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0891B2);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0E7490);
                }
            """)
            save_button.clicked.connect(self.save_classroom)
            button_layout.addWidget(save_button)
            
            cancel_button = QPushButton("Cancel")
            cancel_button.setMinimumHeight(40)
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #475569;
                }
                QPushButton:hover {
                    background-color: #64748B;
                }
            """)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
        except Exception as e:
            print(f"EditClassroomDialog init_ui error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def save_classroom(self):
        """Save the edited classroom"""
        try:
            room_number = self.room_number_input.text().strip()
            room_type = self.room_type_input.text().strip()
            capacity = self.capacity_input.value()
            building = self.building_input.text().strip()
            floor = self.floor_input.value()
            status = self.status_combo.currentData()
            
            if not all([room_number, room_type]):
                QMessageBox.warning(self, "Validation Error", "Room number and type are required!")
                return
            
            db = DatabaseManager()
            query = '''
                UPDATE classrooms 
                SET room_number = ?, room_type = ?, capacity = ?, building = ?, floor = ?, status = ?
                WHERE id = ?
            '''
            db.execute_update(query, (room_number, room_type, capacity, building, floor, status, self.classroom.id))
            
            QMessageBox.information(self, "Success", "Classroom updated successfully!")
            self.accept()
        except Exception as e:
            print(f"Save classroom error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to update classroom:\n{str(e)}")


class EditBookingDialog(QDialog):
    """Dialog for editing booking information"""
    
    def __init__(self, booking, parent=None):
        try:
            super().__init__(parent)
            self.booking = booking
            self.init_ui()
        except Exception as e:
            print(f"EditBookingDialog init error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def init_ui(self):
        """Initialize the user interface"""
        try:
            self.setWindowTitle(f"Edit Booking - ID {self.booking.id}")
            self.setGeometry(100, 100, 500, 450)
            self.setModal(True)
            
            # Apply dark theme styling
            self.setStyleSheet("""
                QDialog {
                    background-color: #1E293B;
                }
                QLabel {
                    color: #E2E8F0;
                    font-size: 11px;
                }
                QLineEdit, QTimeEdit, QComboBox {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    border: 2px solid #334155;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus, QTimeEdit:focus, QComboBox:focus {
                    border: 2px solid #06B6D4;
                }
                QTimeEdit::up-button, QTimeEdit::down-button {
                    background-color: #334155;
                    border: none;
                }
                QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
                    background-color: #475569;
                }
                QComboBox::drop-down {
                    border: none;
                    background-color: #334155;
                }
                QComboBox QAbstractItemView {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    selection-background-color: #06B6D4;
                }
                QPushButton {
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Edit Booking Information")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            title.setStyleSheet("color: #06B6D4; font-size: 14px; margin-bottom: 10px;")
            layout.addWidget(title)
            
            # Course Name
            layout.addWidget(QLabel("Course Name:"))
            self.course_name_input = QLineEdit()
            self.course_name_input.setText(self.booking.course_name if self.booking.course_name else "")
            self.course_name_input.setMinimumHeight(35)
            layout.addWidget(self.course_name_input)
            
            # Start Time
            layout.addWidget(QLabel("Start Time:"))
            self.start_time = QTimeEdit()
            if self.booking.start_time:
                self.start_time.setTime(QTime.fromString(self.booking.start_time, "HH:mm"))
            self.start_time.setMinimumHeight(35)
            layout.addWidget(self.start_time)
            
            # End Time
            layout.addWidget(QLabel("End Time:"))
            self.end_time = QTimeEdit()
            if self.booking.end_time:
                self.end_time.setTime(QTime.fromString(self.booking.end_time, "HH:mm"))
            self.end_time.setMinimumHeight(35)
            layout.addWidget(self.end_time)
            
            # Status
            layout.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItem("Pending", 2)
            self.status_combo.addItem("Approved", 1)
            self.status_combo.addItem("Rejected", 3)
            self.status_combo.addItem("Cancelled", 0)
            status_value = self.booking.status if self.booking.status else 2
            status_index = self.status_combo.findData(status_value)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
            self.status_combo.setMinimumHeight(35)
            layout.addWidget(self.status_combo)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_button = QPushButton("Save")
            save_button.setMinimumHeight(40)
            save_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0891B2);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0E7490);
                }
            """)
            save_button.clicked.connect(self.save_booking)
            button_layout.addWidget(save_button)
            
            cancel_button = QPushButton("Cancel")
            cancel_button.setMinimumHeight(40)
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #475569;
                }
                QPushButton:hover {
                    background-color: #64748B;
                }
            """)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
        except Exception as e:
            print(f"EditBookingDialog init_ui error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def save_booking(self):
        """Save the edited booking"""
        try:
            course_name = self.course_name_input.text().strip()
            start_time = self.start_time.time().toString("HH:mm")
            end_time = self.end_time.time().toString("HH:mm")
            new_status = self.status_combo.currentData()
            old_status = self.booking.status
            
            if not course_name:
                QMessageBox.warning(self, "Validation Error", "Course name is required!")
                return
            
            db = DatabaseManager()
            query = '''
                UPDATE bookings 
                SET course_name = ?, start_time = ?, end_time = ?, status = ?
                WHERE id = ?
            '''
            db.execute_update(query, (course_name, start_time, end_time, new_status, self.booking.id))
            
            # Send email notification if status changed
            if new_status != old_status:
                user = User.get_user_by_id(self.booking.user_id)
                if user:
                    # Update booking details for email
                    self.booking.start_time = start_time
                    self.booking.end_time = end_time
                    self.booking.course_name = course_name
                    
                    if new_status == 1:  # Approved
                        EmailNotificationService.send_approval_email(self.booking, user)
                    elif new_status == 3:  # Rejected
                        EmailNotificationService.send_rejection_email(self.booking, user)
                    elif new_status == 0:  # Cancelled
                        EmailNotificationService.send_cancellation_email(self.booking, user)
            
            QMessageBox.information(self, "Success", "Booking updated successfully!")
            self.accept()
        except Exception as e:
            print(f"Save booking error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to update booking:\n{str(e)}")


class EditScheduleDialog(QDialog):
    """Dialog for editing schedule information"""
    
    def __init__(self, schedule, parent=None):
        try:
            super().__init__(parent)
            self.schedule = schedule
            self.init_ui()
        except Exception as e:
            print(f"EditScheduleDialog init error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def init_ui(self):
        """Initialize the user interface"""
        try:
            self.setWindowTitle(f"Edit Schedule - ID {self.schedule.id}")
            self.setGeometry(100, 100, 500, 500)
            self.setModal(True)
            
            # Apply dark theme styling
            self.setStyleSheet("""
                QDialog {
                    background-color: #1E293B;
                }
                QLabel {
                    color: #E2E8F0;
                    font-size: 11px;
                }
                QLineEdit, QTimeEdit, QComboBox {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    border: 2px solid #334155;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus, QTimeEdit:focus, QComboBox:focus {
                    border: 2px solid #06B6D4;
                }
                QTimeEdit::up-button, QTimeEdit::down-button {
                    background-color: #334155;
                    border: none;
                }
                QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
                    background-color: #475569;
                }
                QComboBox::drop-down {
                    border: none;
                    background-color: #334155;
                }
                QComboBox QAbstractItemView {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    selection-background-color: #06B6D4;
                }
                QPushButton {
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Edit Schedule Information")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            title.setStyleSheet("color: #06B6D4; font-size: 14px; margin-bottom: 10px;")
            layout.addWidget(title)
            
            # Course Name
            layout.addWidget(QLabel("Course Name:"))
            self.course_name_input = QLineEdit()
            self.course_name_input.setText(self.schedule.course_name if self.schedule.course_name else "")
            self.course_name_input.setMinimumHeight(35)
            layout.addWidget(self.course_name_input)
            
            # Day of Week
            layout.addWidget(QLabel("Day of Week:"))
            self.day_combo = QComboBox()
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            self.day_combo.addItems(days)
            if self.schedule.day_of_week:
                day_index = self.day_combo.findText(self.schedule.day_of_week)
                if day_index >= 0:
                    self.day_combo.setCurrentIndex(day_index)
            self.day_combo.setMinimumHeight(35)
            layout.addWidget(self.day_combo)
            
            # Start Time
            layout.addWidget(QLabel("Start Time:"))
            self.start_time = QTimeEdit()
            if self.schedule.start_time:
                self.start_time.setTime(QTime.fromString(self.schedule.start_time, "HH:mm"))
            self.start_time.setMinimumHeight(35)
            layout.addWidget(self.start_time)
            
            # End Time
            layout.addWidget(QLabel("End Time:"))
            self.end_time = QTimeEdit()
            if self.schedule.end_time:
                self.end_time.setTime(QTime.fromString(self.schedule.end_time, "HH:mm"))
            self.end_time.setMinimumHeight(35)
            layout.addWidget(self.end_time)
            
            # Semester
            layout.addWidget(QLabel("Semester:"))
            self.semester_input = QLineEdit()
            self.semester_input.setText(self.schedule.semester if self.schedule.semester else "")
            self.semester_input.setMinimumHeight(35)
            layout.addWidget(self.semester_input)
            
            # Status
            layout.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItem("Active", 1)
            self.status_combo.addItem("Inactive", 0)
            status_value = self.schedule.status if self.schedule.status else 1
            status_index = self.status_combo.findData(status_value)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
            self.status_combo.setMinimumHeight(35)
            layout.addWidget(self.status_combo)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_button = QPushButton("Save")
            save_button.setMinimumHeight(40)
            save_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0891B2);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0E7490);
                }
            """)
            save_button.clicked.connect(self.save_schedule)
            button_layout.addWidget(save_button)
            
            cancel_button = QPushButton("Cancel")
            cancel_button.setMinimumHeight(40)
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #475569;
                }
                QPushButton:hover {
                    background-color: #64748B;
                }
            """)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
            
            layout.addLayout(button_layout)
            self.setLayout(layout)
        except Exception as e:
            print(f"EditScheduleDialog init_ui error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def save_schedule(self):
        """Save the edited schedule"""
        try:
            course_name = self.course_name_input.text().strip()
            day = self.day_combo.currentText()
            start_time = self.start_time.time().toString("HH:mm")
            end_time = self.end_time.time().toString("HH:mm")
            semester = self.semester_input.text().strip()
            status = self.status_combo.currentData()
            
            if not all([course_name, semester]):
                QMessageBox.warning(self, "Validation Error", "Course name and semester are required!")
                return
            
            db = DatabaseManager()
            query = '''
                UPDATE schedules 
                SET course_name = ?, day_of_week = ?, start_time = ?, end_time = ?, semester = ?, status = ?
                WHERE id = ?
            '''
            db.execute_update(query, (course_name, day, start_time, end_time, semester, status, self.schedule.id))
            
            QMessageBox.information(self, "Success", "Schedule updated successfully!")
            self.accept()
        except Exception as e:
            print(f"Save schedule error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to update schedule:\n{str(e)}")
