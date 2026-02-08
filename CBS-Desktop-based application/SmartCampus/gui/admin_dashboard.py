"""
Admin Dashboard Module
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
                             QDialog, QMessageBox, QComboBox, QLineEdit, QSpinBox,
                             QDateEdit, QTimeEdit, QTextEdit, QHeaderView, QMenuBar, QMenu, QScrollArea)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from models.user import User
from models.classroom import Classroom
from models.booking import Booking
from models.schedule import Schedule
from gui.styles import MODERN_STYLESHEET, TITLE_STYLE
from gui.dialogs import AddUserDialog, AddClassroomDialog, AddScheduleDialog, EditUserDialog
from gui.dialogs_edit import EditClassroomDialog, EditBookingDialog, EditScheduleDialog
from database.db_setup import DatabaseManager
from utils.qrcode_generator import QRCodeGenerator
from utils.visualization import MatplotlibCanvas, VisualizationHelper
from datetime import datetime
import math

class AdminDashboard(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.db = DatabaseManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the admin dashboard"""
        self.setWindowTitle(f"Smart Campus - Admin Dashboard ({self.current_user.fullname})")
        self.setGeometry(0, 0, 1400, 900)
        self.setStyleSheet(MODERN_STYLESHEET)
        
        # Menu Bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 2px;
            }
        """)
        
        # Dashboard tab
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        
        # Users management tab
        self.tabs.addTab(self.create_users_tab(), "Users")
        
        # Classrooms tab
        self.tabs.addTab(self.create_classrooms_tab(), "Classrooms")
        
        # Bookings tab
        self.tabs.addTab(self.create_bookings_tab(), "Bookings")
        
        # Schedules tab
        self.tabs.addTab(self.create_schedules_tab(), "Schedules")
        
        # Reports tab
        self.tabs.addTab(self.create_reports_tab(), "Reports")
        
        main_layout.addWidget(self.tabs)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Backup Database", self.backup_database)
        file_menu.addAction("Settings", self.open_settings)
        file_menu.addSeparator()
        file_menu.addAction("Logout", self.logout)
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Refresh", self.refresh_data)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("Documentation", self.open_help)
    
    def create_header(self):
        """Create header widget"""
        header = QWidget()
        header.setStyleSheet("background-color: #2563EB; padding: 15px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Admin Dashboard")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        user_label = QLabel(f"Welcome, {self.current_user.fullname}")
        user_label.setFont(QFont("Segoe UI", 10))
        user_label.setStyleSheet("color: #FFFFFF;")
        header_layout.addWidget(user_label)
        
        return header
    
    def create_dashboard_tab(self):
        """Create dashboard overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Stats
        stats_layout = QHBoxLayout()
        
        stats = [
            ("Total Users", self.count_users(), "#0EA5E9"),
            ("Total Classrooms", self.count_classrooms(), "#059669"),
            ("Total Bookings", self.count_bookings(), "#F59E0B"),
            ("Pending Approvals", self.count_pending_bookings(), "#DC2626"),
        ]
        
        for title, count, color in stats:
            stat_widget = self.create_stat_card(title, count, color)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        # Quick actions
        actions_label = QLabel("Quick Actions")
        actions_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        actions = [
            ("Add User", self.add_user),
            ("Add Classroom", self.add_classroom),
            ("View Bookings", lambda: self.tabs.setCurrentIndex(3)),
            ("View Analytics", self.show_analytics),
            ("Generate Report", self.generate_report),
        ]
        
        for action_name, callback in actions:
            btn = QPushButton(action_name)
            btn.setMinimumHeight(40)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
        
        layout.addLayout(actions_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_stat_card(self, title, value, color):
        """Create a stat card widget"""
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {color};
            border-radius: 8px;
            padding: 20px;
            color: white;
        """)
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: rgba(255,255,255,0.8);")
        layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        layout.addWidget(value_label)
        
        return card
    
    def create_users_tab(self):
        """Create users management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("User Management")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add User")
        add_btn.clicked.connect(self.add_user)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(8)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Full Name", "Email", "Role", "Status", "Edit", "Delete"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setAlternatingRowColors(True)
        self.refresh_users_table()
        
        layout.addWidget(self.users_table)
        
        return widget
    
    def create_classrooms_tab(self):
        """Create classrooms management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Classroom Management")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add Classroom")
        add_btn.clicked.connect(self.add_classroom)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Classrooms table
        self.classrooms_table = QTableWidget()
        self.classrooms_table.setColumnCount(9)
        self.classrooms_table.setHorizontalHeaderLabels(["ID", "Room #", "Type", "Capacity", "Building", "Status", "Edit", "Delete", "QR Code"])
        self.classrooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.classrooms_table.setAlternatingRowColors(True)
        self.refresh_classrooms_table()
        
        layout.addWidget(self.classrooms_table)
        
        return widget
    
    def create_bookings_tab(self):
        """Create bookings management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Booking Management")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        
        self.booking_filter = QComboBox()
        self.booking_filter.addItems(["All", "Pending", "Approved", "Rejected", "Cancelled"])
        self.booking_filter.currentIndexChanged.connect(self.refresh_bookings_table)
        filter_layout.addWidget(self.booking_filter)
        filter_layout.addStretch()
        
        header_layout.addLayout(filter_layout)
        layout.addLayout(header_layout)
        
        # Bookings table
        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(10)
        self.bookings_table.setHorizontalHeaderLabels(["ID", "User", "Room", "Date", "Start", "End", "Status", "View", "Edit", "Delete"])
        self.bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bookings_table.setAlternatingRowColors(True)
        self.refresh_bookings_table()
        
        layout.addWidget(self.bookings_table)
        
        return widget
    
    def create_schedules_tab(self):
        """Create schedules management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Schedule Management")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add Schedule")
        add_btn.clicked.connect(self.add_schedule)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Schedules table
        self.schedules_table = QTableWidget()
        self.schedules_table.setColumnCount(9)
        self.schedules_table.setHorizontalHeaderLabels(["ID", "Teacher", "Course", "Room", "Day", "Time", "Semester", "Edit", "Delete"])
        self.schedules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedules_table.setAlternatingRowColors(True)
        self.refresh_schedules_table()
        
        layout.addWidget(self.schedules_table)
        
        return widget
    
    def create_reports_tab(self):
        """Create reports tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Reports & Analytics")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Report buttons
        buttons_layout = QHBoxLayout()
        
        reports = [
            ("Resource Usage Report", self.report_resource_usage),
            ("Booking Statistics", self.report_booking_stats),
            ("Teacher Schedule Report", self.report_teacher_schedule),
            ("Export All Data", self.export_data),
        ]
        
        for report_name, callback in reports:
            btn = QPushButton(report_name)
            btn.setMinimumHeight(40)
            btn.clicked.connect(callback)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        return widget
    
    # Data loading methods
    def refresh_users_table(self):
        """Refresh users table"""
        users = User.get_all_users()
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.fullname))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.email))
            
            roles = {1: "Admin", 2: "Teacher", 3: "Student"}
            self.users_table.setItem(row, 4, QTableWidgetItem(roles.get(user.role, "Unknown")))
            
            status = "Active" if user.status == 1 else "Inactive"
            self.users_table.setItem(row, 5, QTableWidgetItem(status))
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, u=user: self.edit_user(u))
            edit_btn.setMaximumWidth(80)
            self.users_table.setCellWidget(row, 6, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, u=user: self.delete_user(u))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
            self.users_table.setCellWidget(row, 7, delete_btn)
    
    def refresh_classrooms_table(self):
        """Refresh classrooms table"""
        classrooms = Classroom.get_all_classrooms()
        self.classrooms_table.setRowCount(len(classrooms))
        
        for row, classroom in enumerate(classrooms):
            self.classrooms_table.setItem(row, 0, QTableWidgetItem(str(classroom.id)))
            self.classrooms_table.setItem(row, 1, QTableWidgetItem(classroom.room_number))
            self.classrooms_table.setItem(row, 2, QTableWidgetItem(classroom.room_type))
            self.classrooms_table.setItem(row, 3, QTableWidgetItem(str(classroom.capacity)))
            self.classrooms_table.setItem(row, 4, QTableWidgetItem(classroom.building))
            
            status = "Active" if classroom.status == 1 else "Inactive"
            self.classrooms_table.setItem(row, 5, QTableWidgetItem(status))
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, c=classroom: self.edit_classroom(c))
            edit_btn.setMaximumWidth(80)
            self.classrooms_table.setCellWidget(row, 6, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, c=classroom: self.delete_classroom(c))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
            self.classrooms_table.setCellWidget(row, 7, delete_btn)
            
            # QR Code button
            qr_btn = QPushButton("QR Code")
            qr_btn.clicked.connect(lambda checked, c=classroom: self.generate_classroom_qr(c))
            qr_btn.setMaximumWidth(80)
            qr_btn.setStyleSheet("background-color: #9966ff; color: white;")
            self.classrooms_table.setCellWidget(row, 8, qr_btn)
    
    def refresh_bookings_table(self):
        """Refresh bookings table"""
        filter_index = self.booking_filter.currentIndex()
        status_map = {0: None, 1: 2, 2: 1, 3: 3, 4: 0}  # Filter index to status
        status = status_map.get(filter_index)
        
        bookings = Booking.get_all_bookings(status)
        self.bookings_table.setRowCount(len(bookings))
        
        for row, booking in enumerate(bookings):
            user = User.get_user_by_id(booking.user_id)
            classroom = Classroom.get_classroom_by_id(booking.classroom_id)
            
            self.bookings_table.setItem(row, 0, QTableWidgetItem(str(booking.id)))
            self.bookings_table.setItem(row, 1, QTableWidgetItem(user.fullname if user else "Unknown"))
            self.bookings_table.setItem(row, 2, QTableWidgetItem(classroom.room_number if classroom else "Unknown"))
            self.bookings_table.setItem(row, 3, QTableWidgetItem(str(booking.booking_date)))
            self.bookings_table.setItem(row, 4, QTableWidgetItem(booking.start_time))
            self.bookings_table.setItem(row, 5, QTableWidgetItem(booking.end_time))
            
            status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
            self.bookings_table.setItem(row, 6, QTableWidgetItem(status_map.get(booking.status, "Unknown")))
            
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda checked, b=booking: self.view_booking(b))
            view_btn.setMaximumWidth(80)
            self.bookings_table.setCellWidget(row, 7, view_btn)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, b=booking: self.edit_booking(b))
            edit_btn.setMaximumWidth(80)
            self.bookings_table.setCellWidget(row, 8, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, b=booking: self.delete_booking(b))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
            self.bookings_table.setCellWidget(row, 9, delete_btn)
    
    def refresh_schedules_table(self):
        """Refresh schedules table"""
        schedules = Schedule.get_all_schedules()
        self.schedules_table.setRowCount(len(schedules))
        
        for row, schedule in enumerate(schedules):
            teacher = User.get_user_by_id(schedule.teacher_id)
            classroom = Classroom.get_classroom_by_id(schedule.classroom_id)
            
            self.schedules_table.setItem(row, 0, QTableWidgetItem(str(schedule.id)))
            self.schedules_table.setItem(row, 1, QTableWidgetItem(teacher.fullname if teacher else "Unknown"))
            self.schedules_table.setItem(row, 2, QTableWidgetItem(schedule.course_name))
            self.schedules_table.setItem(row, 3, QTableWidgetItem(classroom.room_number if classroom else "Unknown"))
            self.schedules_table.setItem(row, 4, QTableWidgetItem(schedule.day_of_week))
            self.schedules_table.setItem(row, 5, QTableWidgetItem(f"{schedule.start_time}-{schedule.end_time}"))
            self.schedules_table.setItem(row, 6, QTableWidgetItem(schedule.semester or "N/A"))
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, s=schedule: self.edit_schedule(s))
            edit_btn.setMaximumWidth(80)
            self.schedules_table.setCellWidget(row, 7, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, s=schedule: self.delete_schedule(s))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
            self.schedules_table.setCellWidget(row, 8, delete_btn)
    
    # Count methods
    def count_users(self):
        """Count total users"""
        query = 'SELECT COUNT(*) FROM users WHERE role != 1'
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    def count_classrooms(self):
        """Count total classrooms"""
        query = 'SELECT COUNT(*) FROM classrooms WHERE status = 1'
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    def count_bookings(self):
        """Count total bookings"""
        query = 'SELECT COUNT(*) FROM bookings'
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    def count_pending_bookings(self):
        """Count pending bookings"""
        query = 'SELECT COUNT(*) FROM bookings WHERE status = 2'
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    def count_schedules(self):
        """Count total schedules"""
        query = 'SELECT COUNT(*) FROM schedules'
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    # Action methods
    def add_user(self):
        """Add new user"""
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_users_table()
    
    def edit_user(self, user):
        """Edit existing user"""
        try:
            dialog = EditUserDialog(user, self)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_users_table()
        except Exception as e:
            print(f"Edit user error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open edit dialog:\n{str(e)}")
    
    def delete_user(self, user):
        """Delete user"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete user '{user.fullname}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseManager()
                db.execute_update("DELETE FROM users WHERE id = ?", (user.id,))
                QMessageBox.information(self, "Success", "User deleted successfully!")
                self.refresh_users_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user:\n{str(e)}")
    
    def edit_classroom(self, classroom):
        """Edit existing classroom"""
        try:
            dialog = EditClassroomDialog(classroom, self)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_classrooms_table()
        except Exception as e:
            print(f"Edit classroom error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open edit dialog:\n{str(e)}")
    
    def delete_classroom(self, classroom):
        """Delete classroom"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete classroom '{classroom.room_number}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseManager()
                db.execute_update("DELETE FROM classrooms WHERE id = ?", (classroom.id,))
                QMessageBox.information(self, "Success", "Classroom deleted successfully!")
                self.refresh_classrooms_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete classroom:\n{str(e)}")
    
    def edit_booking(self, booking):
        """Edit existing booking"""
        try:
            dialog = EditBookingDialog(booking, self)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_bookings_table()
        except Exception as e:
            print(f"Edit booking error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open edit dialog:\n{str(e)}")
    
    def delete_booking(self, booking):
        """Delete booking"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete booking ID {booking.id}?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseManager()
                db.execute_update("DELETE FROM bookings WHERE id = ?", (booking.id,))
                QMessageBox.information(self, "Success", "Booking deleted successfully!")
                self.refresh_bookings_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete booking:\n{str(e)}")
    
    def edit_schedule(self, schedule):
        """Edit existing schedule"""
        try:
            dialog = EditScheduleDialog(schedule, self)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_schedules_table()
        except Exception as e:
            print(f"Edit schedule error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open edit dialog:\n{str(e)}")
    
    def delete_schedule(self, schedule):
        """Delete schedule"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete schedule ID {schedule.id}?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseManager()
                db.execute_update("DELETE FROM schedules WHERE id = ?", (schedule.id,))
                QMessageBox.information(self, "Success", "Schedule deleted successfully!")
                self.refresh_schedules_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete schedule:\n{str(e)}")
    
    def generate_classroom_qr(self, classroom):
        """Generate and display QR code for classroom"""
        try:
            # Generate QR code
            qr_image = QRCodeGenerator.generate_classroom_qr(
                classroom.id,
                classroom.room_number,
                classroom.building,
                classroom.capacity
            )
            
            if not qr_image:
                QMessageBox.warning(self, "Error", "Failed to generate QR code!")
                return
            
            # Save QR code
            filepath = QRCodeGenerator.generate_and_save_qr(
                classroom.id,
                classroom.room_number,
                classroom.building,
                classroom.capacity
            )
            
            # Display in dialog
            dialog = QDialog(self)
            dialog.setWindowTitle(f"QR Code - {classroom.room_number}")
            dialog.setGeometry(200, 200, 500, 550)
            
            layout = QVBoxLayout()
            
            # Title
            title = QLabel(f"Classroom QR Code: {classroom.room_number}")
            title.setFont(QFont("Segoe UI", 12, QFont.Bold))
            layout.addWidget(title)
            
            # Info
            info_text = QLabel(f"Building: {classroom.building}\nCapacity: {classroom.capacity}\nType: {classroom.room_type}")
            layout.addWidget(info_text)
            
            # QR Code image
            qr_label = QLabel()
            qr_pixmap = QPixmap()
            qr_pixmap.load(filepath)
            qr_pixmap = qr_pixmap.scaledToWidth(300)
            qr_label.setPixmap(qr_pixmap)
            qr_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(qr_label)
            
            # Info label
            info_label = QLabel(f"Saved to: {filepath}")
            info_label.setWordWrap(True)
            info_label.setFont(QFont("Segoe UI", 9))
            layout.addWidget(info_label)
            
            # Close button
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"QR code generation error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to generate QR code:\n{str(e)}")
    
    def show_analytics(self):
        """Show analytics and visualizations"""
        try:
            # Create analytics dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Analytics & Visualizations")
            dialog.setGeometry(100, 100, 1000, 700)
            
            layout = QVBoxLayout()
            
            # Title
            title = QLabel("System Analytics")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            layout.addWidget(title)
            
            # Get data
            bookings = Booking.get_all_bookings()
            classrooms = Classroom.get_all_classrooms()
            users = User.get_all_users()
            schedules = Schedule.get_all_schedules()
            teachers = [u for u in users if u.role == 2]
            
            # Create tabs for different visualizations
            tabs = QTabWidget()
            
            # Booking Status Tab
            status_data = VisualizationHelper.get_booking_status_data(bookings)
            canvas1 = MatplotlibCanvas(width=8, height=5, dpi=80)
            canvas1.plot_booking_status_pie(status_data)
            tabs.addTab(canvas1, "Booking Status")
            
            # Room Utilization Tab
            room_data = VisualizationHelper.get_room_utilization(classrooms, bookings)
            canvas2 = MatplotlibCanvas(width=8, height=5, dpi=80)
            canvas2.plot_room_utilization(room_data)
            tabs.addTab(canvas2, "Room Utilization")
            
            # Bookings by Day Tab
            day_data = VisualizationHelper.get_bookings_by_day(bookings)
            canvas3 = MatplotlibCanvas(width=8, height=5, dpi=80)
            canvas3.plot_bookings_by_day(day_data)
            tabs.addTab(canvas3, "Bookings by Day")
            
            # Teacher Workload Tab
            workload_data = VisualizationHelper.get_teacher_workload(teachers, schedules)
            if workload_data:
                canvas4 = MatplotlibCanvas(width=8, height=5, dpi=80)
                canvas4.plot_teacher_workload(workload_data)
                tabs.addTab(canvas4, "Teacher Workload")
            
            layout.addWidget(tabs)
            
            # Close button
            close_btn = QPushButton("Close")
            close_btn.setMinimumHeight(40)
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"Analytics error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to display analytics:\n{str(e)}")
    
    def add_classroom(self):
        """Add new classroom"""
        dialog = AddClassroomDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_classrooms_table()
    
    def add_schedule(self):
        """Add new schedule"""
        dialog = AddScheduleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_schedules_table()
    
    def view_booking(self, booking):
        """View booking details"""
        user = User.get_user_by_id(booking.user_id)
        classroom = Classroom.get_classroom_by_id(booking.classroom_id)
        
        status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
        
        message = f"""
        Booking Details:
        
        Booking ID: {booking.id}
        User: {user.fullname if user else 'Unknown'}
        Classroom: {classroom.room_number if classroom else 'Unknown'}
        Course: {booking.course_name}
        Date: {booking.booking_date}
        Time: {booking.start_time} - {booking.end_time}
        Status: {status_map.get(booking.status, 'Unknown')}
        Description: {booking.description}
        """
        
        if booking.status == 2:  # Pending
            reply = QMessageBox.question(self, "Booking Details", message + "\n\nApprove this booking?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                booking.approve(self.current_user.id)
                QMessageBox.information(self, "Success", "Booking approved!")
                self.refresh_bookings_table()
        else:
            QMessageBox.information(self, "Booking Details", message)
    
    def refresh_data(self):
        """Refresh all data"""
        self.refresh_users_table()
        self.refresh_classrooms_table()
        self.refresh_bookings_table()
        self.refresh_schedules_table()
        QMessageBox.information(self, "Success", "Data refreshed!")
    
    def backup_database(self):
        """Backup database"""
        backup_path = self.db.backup_database()
        QMessageBox.information(self, "Backup Complete", f"Database backed up to:\n{backup_path}")
    
    def open_settings(self):
        """Open settings dialog"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("System Settings")
            dialog.setGeometry(100, 100, 600, 500)
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("System Configuration")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            layout.addWidget(title)
            
            # Database Settings Section
            db_group = QLabel("Database Settings")
            db_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
            layout.addWidget(db_group)
            
            layout.addWidget(QLabel("Database Path:"))
            db_path_input = QLineEdit()
            from config import DB_PATH
            db_path_input.setText(DB_PATH)
            db_path_input.setReadOnly(True)
            db_path_input.setMinimumHeight(35)
            layout.addWidget(db_path_input)
            
            # University Settings
            uni_group = QLabel("University Settings")
            uni_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
            layout.addWidget(uni_group)
            
            layout.addWidget(QLabel("University Name:"))
            uni_input = QLineEdit()
            from config import UNIVERSITY_NAME
            uni_input.setText(UNIVERSITY_NAME)
            uni_input.setReadOnly(True)
            uni_input.setMinimumHeight(35)
            layout.addWidget(uni_input)
            
            # Session Info
            info_layout = QHBoxLayout()
            
            session_layout = QVBoxLayout()
            session_layout.addWidget(QLabel("Session:"))
            session_input = QLineEdit()
            from config import SESSION
            session_input.setText(SESSION)
            session_input.setReadOnly(True)
            session_input.setMinimumHeight(35)
            session_layout.addWidget(session_input)
            info_layout.addLayout(session_layout)
            
            semester_layout = QVBoxLayout()
            semester_layout.addWidget(QLabel("Semester:"))
            semester_input = QLineEdit()
            from config import SEMESTER
            semester_input.setText(str(SEMESTER))
            semester_input.setReadOnly(True)
            semester_input.setMinimumHeight(35)
            semester_layout.addWidget(semester_input)
            info_layout.addLayout(semester_layout)
            
            layout.addLayout(info_layout)
            
            # System Stats
            stats_group = QLabel("System Statistics")
            stats_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
            layout.addWidget(stats_group)
            
            stats_text = QTextEdit()
            stats_text.setReadOnly(True)
            stats_text.setMaximumHeight(120)
            stats_content = f"""Total Users: {self.count_users()}
Total Classrooms: {self.count_classrooms()}
Total Bookings: {self.count_bookings()}
Total Schedules: {self.count_schedules()}"""
            stats_text.setText(stats_content)
            layout.addWidget(stats_text)
            
            # Close button
            close_btn = QPushButton("Close")
            close_btn.setMinimumHeight(40)
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"Settings error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open settings:\n{str(e)}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        try:
            from reports.usage_report import ReportGenerator
            import os
            from datetime import datetime
            
            report_gen = ReportGenerator()
            
            # Create reports directory if it doesn't exist
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports_output')
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Generate report with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(reports_dir, f"comprehensive_report_{timestamp}.txt")
            
            with open(report_file, 'w') as f:
                f.write("="*80 + "\n")
                f.write("FATIMA JINNAH WOMEN UNIVERSITY\n")
                f.write("Smart Campus Resource Management System - Comprehensive Report\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                # Booking Statistics
                f.write("1. BOOKING STATISTICS\n")
                f.write("-" * 80 + "\n")
                stats = report_gen.get_booking_stats()
                f.write(f"Total Bookings: {stats['total']}\n")
                f.write(f"Approved: {stats['approved']}\n")
                f.write(f"Pending: {stats['pending']}\n")
                f.write(f"Rejected: {stats['rejected']}\n")
                f.write(f"Cancelled: {stats['cancelled']}\n\n")
                
                # Resource Usage
                f.write("2. CLASSROOM RESOURCE USAGE\n")
                f.write("-" * 80 + "\n")
                usage = report_gen.get_resource_usage()
                for classroom, count in usage.items():
                    f.write(f"{classroom}: {count} bookings\n")
                f.write("\n")
                
                # Classroom Information
                f.write("3. CLASSROOM INFORMATION\n")
                f.write("-" * 80 + "\n")
                classrooms = Classroom.get_all_classrooms()
                for classroom in classrooms:
                    f.write(f"Room {classroom.room_number}:\n")
                    f.write(f"  Type: {classroom.room_type}\n")
                    f.write(f"  Building: {classroom.building}\n")
                    f.write(f"  Floor: {classroom.floor}\n")
                    f.write(f"  Capacity: {classroom.capacity}\n\n")
                
                # Teacher Information
                f.write("4. TEACHER INFORMATION\n")
                f.write("-" * 80 + "\n")
                db = DatabaseManager()
                teachers = db.execute_query('SELECT id, fullname, email, phone FROM users WHERE role = 2')
                for teacher in teachers:
                    f.write(f"{teacher[1]}:\n")
                    f.write(f"  Email: {teacher[2]}\n")
                    f.write(f"  Phone: {teacher[3]}\n\n")
                
                f.write("="*80 + "\n")
                f.write("End of Report\n")
                f.write("="*80 + "\n")
            
            # Show success message with file location
            QMessageBox.information(self, "Report Generated", 
                                  f"Report has been generated successfully!\n\n"
                                  f"Location: {report_file}\n\n"
                                  f"The report contains:\n"
                                  f"- Booking Statistics\n"
                                  f"- Classroom Resource Usage\n"
                                  f"- Classroom Information\n"
                                  f"- Teacher Information")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")
    
    def report_resource_usage(self):
        """Generate resource usage report"""
        try:
            import os
            
            # Create reports directory in the same folder as the app
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, 'reports_output')
            
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(reports_dir, f"resource_usage_report_{timestamp}.txt")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("FATIMA JINNAH WOMEN UNIVERSITY\n")
                f.write("Classroom Resource Usage Report\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                from reports.usage_report import ReportGenerator
                report_gen = ReportGenerator()
                usage = report_gen.get_resource_usage()
                
                f.write("CLASSROOM RESOURCE USAGE STATISTICS\n")
                f.write("-" * 80 + "\n")
                f.write(f"{'Classroom':<20} {'Bookings':<15}\n")
                f.write("-" * 80 + "\n")
                
                total_bookings = 0
                for classroom, count in sorted(usage.items()):
                    f.write(f"{classroom:<20} {count:<15}\n")
                    total_bookings += count
                
                f.write("-" * 80 + "\n")
                f.write(f"{'TOTAL':<20} {total_bookings:<15}\n")
                f.write("="*80 + "\n")
            
            QMessageBox.information(self, "Report Generated", 
                                  f"✓ Report saved successfully!\n\n"
                                  f"File: resource_usage_report_{timestamp}.txt\n\n"
                                  f"Location:\n{reports_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")
    
    def report_booking_stats(self):
        """Generate booking statistics report"""
        try:
            import os
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, 'reports_output')
            
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(reports_dir, f"booking_statistics_{timestamp}.txt")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("FATIMA JINNAH WOMEN UNIVERSITY\n")
                f.write("Booking Statistics Report\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                from reports.usage_report import ReportGenerator
                report_gen = ReportGenerator()
                stats = report_gen.get_booking_stats()
                
                f.write("BOOKING STATISTICS\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Bookings:    {stats['total']}\n")
                f.write(f"Approved:          {stats['approved']}\n")
                f.write(f"Pending:           {stats['pending']}\n")
                f.write(f"Rejected:          {stats['rejected']}\n")
                f.write(f"Cancelled:         {stats['cancelled']}\n")
                f.write("-" * 80 + "\n")
                
                if stats['total'] > 0:
                    f.write(f"\nApproval Rate:     {(stats['approved']/stats['total']*100):.1f}%\n")
                    f.write(f"Pending Rate:      {(stats['pending']/stats['total']*100):.1f}%\n")
                
                f.write("="*80 + "\n")
            
            QMessageBox.information(self, "Report Generated", 
                                  f"✓ Report saved successfully!\n\n"
                                  f"File: booking_statistics_{timestamp}.txt\n\n"
                                  f"Location:\n{reports_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")
    
    def report_teacher_schedule(self):
        """Generate teacher schedule report"""
        try:
            import os
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, 'reports_output')
            
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(reports_dir, f"teacher_schedule_{timestamp}.txt")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("FATIMA JINNAH WOMEN UNIVERSITY\n")
                f.write("Teacher Schedule Report\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                db = DatabaseManager()
                teachers = db.execute_query('SELECT id, fullname FROM users WHERE role = 2 ORDER BY fullname')
                
                f.write("TEACHER SCHEDULES\n")
                f.write("-" * 80 + "\n\n")
                
                for teacher in teachers:
                    teacher_id = teacher[0]
                    teacher_name = teacher[1]
                    
                    f.write(f"Teacher: {teacher_name}\n")
                    f.write("-" * 60 + "\n")
                    
                    schedules = db.execute_query(
                        'SELECT s.course_name, s.day_of_week, s.start_time, s.end_time, c.room_number FROM schedules s '
                        'JOIN classrooms c ON s.classroom_id = c.id WHERE s.teacher_id = ? ORDER BY s.day_of_week, s.start_time',
                        (teacher_id,)
                    )
                    
                    if schedules:
                        for schedule in schedules:
                            course = schedule[0]
                            day = schedule[1]
                            start = schedule[2]
                            end = schedule[3]
                            room = schedule[4]
                            f.write(f"  {day:<12} {start}-{end}  {room:<8}  {course}\n")
                    else:
                        f.write("  No schedules assigned\n")
                    
                    f.write("\n")
                
                f.write("="*80 + "\n")
            
            QMessageBox.information(self, "Report Generated", 
                                  f"✓ Report saved successfully!\n\n"
                                  f"File: teacher_schedule_{timestamp}.txt\n\n"
                                  f"Location:\n{reports_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")
    
    def export_data(self):
        """Export all data to CSV files"""
        try:
            import os
            import csv
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, 'reports_output')
            
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            db = DatabaseManager()
            
            # Export Classrooms
            classrooms_file = os.path.join(reports_dir, f"classrooms_{timestamp}.csv")
            with open(classrooms_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Room Number', 'Type', 'Building', 'Floor', 'Capacity'])
                classrooms = Classroom.get_all_classrooms()
                for c in classrooms:
                    writer.writerow([c.room_number, c.room_type, c.building, c.floor, c.capacity])
            
            # Export Teachers
            teachers_file = os.path.join(reports_dir, f"teachers_{timestamp}.csv")
            with open(teachers_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Full Name', 'Username', 'Email', 'Phone', 'Department'])
                teachers = db.execute_query('SELECT fullname, username, email, phone, department FROM users WHERE role = 2')
                for t in teachers:
                    writer.writerow(t)
            
            # Export Schedules
            schedules_file = os.path.join(reports_dir, f"schedules_{timestamp}.csv")
            with open(schedules_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Course', 'Teacher', 'Classroom', 'Day', 'Start Time', 'End Time', 'Semester'])
                schedules = db.execute_query(
                    'SELECT s.course_name, u.fullname, c.room_number, s.day_of_week, s.start_time, s.end_time, s.semester '
                    'FROM schedules s JOIN users u ON s.teacher_id = u.id JOIN classrooms c ON s.classroom_id = c.id'
                )
                for s in schedules:
                    writer.writerow(s)
            
            QMessageBox.information(self, "Data Exported", 
                                  f"✓ All data exported successfully!\n\n"
                                  f"Files created:\n"
                                  f"- classrooms_{timestamp}.csv\n"
                                  f"- teachers_{timestamp}.csv\n"
                                  f"- schedules_{timestamp}.csv\n\n"
                                  f"Location:\n{reports_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export data:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Smart Campus Resource Management System
        Version 1.0.0
        
        © 2026 Smart Campus
        All rights reserved.
        
        A comprehensive solution for managing university resources.
        """
        QMessageBox.information(self, "About", about_text)
    
    def open_help(self):
        """Open help documentation"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Help - Admin Dashboard")
            dialog.setGeometry(100, 100, 700, 600)
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            layout.setSpacing(10)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Smart Campus - Admin Dashboard Help")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            layout.addWidget(title)
            
            # Help content
            help_text = QTextEdit()
            help_text.setReadOnly(True)
            help_content = """<html>
<h2>Admin Dashboard Features</h2>

<h3>Dashboard Tab</h3>
<ul>
<li><b>Statistics Cards:</b> View total users, classrooms, bookings, and pending approvals</li>
<li><b>Quick Actions:</b> Add users, classrooms, schedules, view bookings, and generate reports</li>
</ul>

<h3>Users Tab</h3>
<ul>
<li><b>View Users:</b> See all registered users with their details</li>
<li><b>Add User:</b> Create new user accounts (Admin/Teacher/Student)</li>
<li><b>Edit User:</b> Update user information, department, and status</li>
<li><b>Delete User:</b> Remove users from the system</li>
</ul>

<h3>Classrooms Tab</h3>
<ul>
<li><b>View Classrooms:</b> See all available classrooms</li>
<li><b>Add Classroom:</b> Register new classrooms with capacity and details</li>
<li><b>Edit Classroom:</b> Update room information, capacity, and status</li>
<li><b>Delete Classroom:</b> Remove classrooms from the system</li>
</ul>

<h3>Bookings Tab</h3>
<ul>
<li><b>View Bookings:</b> See all booking requests with status filters</li>
<li><b>Edit Booking:</b> Modify booking details and status</li>
<li><b>Delete Booking:</b> Cancel bookings</li>
<li><b>Approve/Reject:</b> Manage booking approval status</li>
</ul>

<h3>Schedules Tab</h3>
<ul>
<li><b>View Schedules:</b> See all class schedules</li>
<li><b>Add Schedule:</b> Create new class schedules</li>
<li><b>Edit Schedule:</b> Update schedule timings and details</li>
<li><b>Delete Schedule:</b> Remove schedules</li>
</ul>

<h3>Reports Tab</h3>
<ul>
<li><b>Resource Usage Report:</b> View classroom utilization statistics</li>
<li><b>Booking Statistics:</b> See booking trends and status breakdown</li>
<li><b>Teacher Schedule Report:</b> Generate teacher-wise schedule reports</li>
<li><b>Export Data:</b> Export classrooms, teachers, and schedules to CSV</li>
</ul>

<h3>Menu Options</h3>
<ul>
<li><b>File → Backup Database:</b> Create database backup</li>
<li><b>File → Settings:</b> View system configuration and statistics</li>
<li><b>File → Logout:</b> Exit admin dashboard</li>
<li><b>Edit → Refresh Data:</b> Reload all data from database</li>
<li><b>Help → About:</b> View application information</li>
</ul>

<h3>Support</h3>
<p><b>Email:</b> hajrasarwar11@gmail.com<br>
<b>Phone:</b> 03273456789</p>
</html>"""
            help_text.setHtml(help_content)
            layout.addWidget(help_text)
            
            # Close button
            close_btn = QPushButton("Close")
            close_btn.setMinimumHeight(40)
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"Help error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open help:\n{str(e)}")
    
    def logout(self):
        """Logout user"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
