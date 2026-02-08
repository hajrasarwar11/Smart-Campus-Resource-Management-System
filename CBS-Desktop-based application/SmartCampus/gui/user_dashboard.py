"""
User Dashboard Module (Student/Teacher)
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox, QLineEdit, QDateEdit, QTimeEdit, QTextEdit,
                             QSpinBox, QMessageBox, QTabWidget, QHeaderView, QMenu, QMenuBar)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor
from models.user import User
from models.classroom import Classroom
from models.booking import Booking
from models.schedule import Schedule
from gui.styles import MODERN_STYLESHEET
from gui.dialogs_edit import EditBookingDialog
from utils.validation import FormValidator, Validator
from utils.email_notification import EmailNotificationService
from database.db_setup import DatabaseManager
from datetime import datetime, timedelta
from config import TIME_SLOTS

class UserDashboard(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.db = DatabaseManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize user dashboard"""
        self.setWindowTitle(f"Smart Campus - {self.current_user.fullname}")
        self.setGeometry(0, 0, 1400, 900)
        self.setStyleSheet(MODERN_STYLESHEET)
        
        # Menu bar
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
        
        # Dashboard tab
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        
        # Bookings tab
        self.tabs.addTab(self.create_bookings_tab(), "My Bookings")
        
        # Available rooms tab
        self.tabs.addTab(self.create_available_rooms_tab(), "Available Rooms")
        
        # Schedules tab (for teachers)
        if self.current_user.role == 2:
            self.tabs.addTab(self.create_schedules_tab(), "My Schedules")
        
        # Profile tab
        self.tabs.addTab(self.create_profile_tab(), "Profile")
        
        main_layout.addWidget(self.tabs)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Refresh", self.refresh_data)
        file_menu.addAction("Export Bookings", self.export_bookings)
        file_menu.addSeparator()
        file_menu.addAction("Logout", self.logout)
        file_menu.addAction("Exit", self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("Contact Support", self.contact_support)
    
    def create_header(self):
        """Create header widget"""
        header = QWidget()
        header.setStyleSheet("background-color: #2563EB; padding: 15px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel(f"Welcome, {self.current_user.fullname}")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        dept_label = QLabel(f"Department: {self.current_user.department}")
        dept_label.setFont(QFont("Segoe UI", 10))
        dept_label.setStyleSheet("color: #FFFFFF;")
        header_layout.addWidget(dept_label)
        
        return header
    
    def create_dashboard_tab(self):
        """Create dashboard overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # For Students - Show Class Schedule
        if self.current_user.role == 3:  # Student
            # Title
            title = QLabel("My Class Schedule - Fall 2025")
            title.setFont(QFont("Segoe UI", 16, QFont.Bold))
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # Semester info
            info_layout = QHBoxLayout()
            info_layout.addStretch()
            
            semester_label = QLabel(f"Semester: {self.current_user.department} - 5th Semester, Section A")
            semester_label.setFont(QFont("Segoe UI", 11))
            info_layout.addWidget(semester_label)
            info_layout.addStretch()
            layout.addLayout(info_layout)
            
            # Day selector
            day_layout = QHBoxLayout()
            day_label = QLabel("Select Day:")
            day_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            day_layout.addWidget(day_label)
            
            self.day_selector = QComboBox()
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            self.day_selector.addItems(days)
            
            # Set today's day
            from datetime import datetime
            today = datetime.now().strftime("%A")
            if today in days:
                self.day_selector.setCurrentText(today)
            
            self.day_selector.currentIndexChanged.connect(self.refresh_schedule_for_day)
            self.day_selector.setMinimumHeight(35)
            day_layout.addWidget(self.day_selector)
            day_layout.addStretch()
            
            layout.addLayout(day_layout)
            
            # Schedule table
            self.schedule_table = QTableWidget()
            self.schedule_table.setColumnCount(6)
            self.schedule_table.setHorizontalHeaderLabels(["Time", "Course", "Teacher", "Room", "Building", "Duration"])
            self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.schedule_table.setAlternatingRowColors(True)
            self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.refresh_schedule_for_day()
            
            layout.addWidget(self.schedule_table)
            
            # Quick action for booking
            booking_label = QLabel("Need to book a room?")
            booking_label.setFont(QFont("Segoe UI", 10))
            booking_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(booking_label)
            
            book_btn = QPushButton("Book a Room")
            book_btn.setMinimumHeight(45)
            book_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
            layout.addWidget(book_btn)
        
        else:  # For Teachers - keep existing stats
            # Quick stats
            stats_layout = QHBoxLayout()
            
            my_bookings = len(Booking.get_user_bookings(self.current_user.id))
            approved = len(Booking.get_user_bookings(self.current_user.id, status=1))
            pending = len(Booking.get_user_bookings(self.current_user.id, status=2))
            
            stats = [
                ("Total Bookings", my_bookings, "#0EA5E9"),
                ("Approved", approved, "#059669"),
                ("Pending", pending, "#F59E0B"),
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
                ("Book a Room", lambda: self.tabs.setCurrentIndex(2)),
                ("View My Bookings", lambda: self.tabs.setCurrentIndex(1)),
                ("View Profile", lambda: self.tabs.setCurrentIndex(3 if self.current_user.role == 2 else 4)),
            ]
            
            for action_name, callback in actions:
                btn = QPushButton(action_name)
                btn.setMinimumHeight(40)
                btn.clicked.connect(callback)
                actions_layout.addWidget(btn)
            
            layout.addLayout(actions_layout)
            
            # Recent bookings
            recent_label = QLabel("Recent Bookings")
            recent_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            layout.addWidget(recent_label)
            
            self.recent_bookings_table = QTableWidget()
            self.recent_bookings_table.setColumnCount(5)
            self.recent_bookings_table.setHorizontalHeaderLabels(["Room", "Date", "Start", "End", "Status"])
            self.recent_bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.recent_bookings_table.setMaximumHeight(200)
            self.refresh_recent_bookings()
            
            layout.addWidget(self.recent_bookings_table)
            layout.addStretch()
        
        return widget
    
    def create_bookings_tab(self):
        """Create bookings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("My Bookings")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        book_btn = QPushButton("+ New Booking")
        book_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        header_layout.addWidget(book_btn)
        
        layout.addLayout(header_layout)
        
        # Bookings table
        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(10)
        self.bookings_table.setHorizontalHeaderLabels(["ID", "Room", "Course", "Date", "Start", "End", "Status", "View", "Edit", "Cancel"])
        self.bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bookings_table.setAlternatingRowColors(True)
        self.refresh_bookings_table()
        
        layout.addWidget(self.bookings_table)
        
        return widget
    
    def create_available_rooms_tab(self):
        """Create available rooms search tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Filter section
        filter_label = QLabel("Search Available Rooms")
        filter_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(filter_label)
        
        filter_layout = QHBoxLayout()
        
        # Room type
        filter_layout.addWidget(QLabel("Room Type:"))
        self.room_type_combo = QComboBox()
        self.room_type_combo.addItems(["All", "Theory", "Lab", "Seminar", "Conference"])
        filter_layout.addWidget(self.room_type_combo)
        
        # Date
        filter_layout.addWidget(QLabel("Date:"))
        self.search_date = QDateEdit()
        self.search_date.setDate(QDate.currentDate())
        self.search_date.setCalendarPopup(True)
        filter_layout.addWidget(self.search_date)
        
        # Start time
        filter_layout.addWidget(QLabel("From:"))
        self.search_start_time = QComboBox()
        self.search_start_time.addItems(TIME_SLOTS)
        filter_layout.addWidget(self.search_start_time)
        
        # End time
        filter_layout.addWidget(QLabel("To:"))
        self.search_end_time = QComboBox()
        self.search_end_time.addItems(TIME_SLOTS)
        filter_layout.addWidget(self.search_end_time)
        
        # Search button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_available_rooms)
        filter_layout.addWidget(search_btn)
        
        layout.addLayout(filter_layout)
        
        # Available rooms table
        self.available_rooms_table = QTableWidget()
        self.available_rooms_table.setColumnCount(6)
        self.available_rooms_table.setHorizontalHeaderLabels(["Room #", "Type", "Capacity", "Building", "Floor", "Action"])
        self.available_rooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.available_rooms_table.setAlternatingRowColors(True)
        self.search_available_rooms()
        
        layout.addWidget(self.available_rooms_table)
        
        return widget
    
    def create_schedules_tab(self):
        """Create schedules tab (for teachers)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("My Schedules")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add Schedule")
        add_btn.clicked.connect(self.add_schedule)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Schedules table
        self.schedules_table = QTableWidget()
        self.schedules_table.setColumnCount(6)
        self.schedules_table.setHorizontalHeaderLabels(["Course", "Room", "Day", "Start", "End", "Semester"])
        self.schedules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedules_table.setAlternatingRowColors(True)
        self.refresh_schedules_table()
        
        layout.addWidget(self.schedules_table)
        
        return widget
    
    def create_profile_tab(self):
        """Create profile tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("My Profile")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Profile info
        info_layout = QHBoxLayout()
        
        profile_frame = QWidget()
        profile_frame.setStyleSheet("""
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 20px;
        """)
        profile_layout = QVBoxLayout(profile_frame)
        
        profile_data = [
            ("Username", self.current_user.username),
            ("Full Name", self.current_user.fullname),
            ("Email", self.current_user.email),
            ("Phone", self.current_user.phone or "Not provided"),
            ("Department", self.current_user.department),
            ("Role", "Teacher" if self.current_user.role == 2 else "Student"),
        ]
        
        for label, value in profile_data:
            row_layout = QHBoxLayout()
            label_widget = QLabel(f"{label}:")
            label_widget.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label_widget.setMinimumWidth(120)
            value_widget = QLabel(value)
            value_widget.setFont(QFont("Segoe UI", 10))
            row_layout.addWidget(label_widget)
            row_layout.addWidget(value_widget)
            row_layout.addStretch()
            profile_layout.addLayout(row_layout)
        
        info_layout.addWidget(profile_frame)
        layout.addLayout(info_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Edit Profile")
        edit_btn.clicked.connect(self.edit_profile)
        buttons_layout.addWidget(edit_btn)
        
        password_btn = QPushButton("Change Password")
        password_btn.clicked.connect(self.change_password)
        buttons_layout.addWidget(password_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        return widget
    
    def create_stat_card(self, title, value, color):
        """Create stat card"""
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {color};
            border-radius: 8px;
            padding: 20px;
            color: white;
        """)
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: rgba(255,255,255,0.8);")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        card_layout.addWidget(value_label)
        
        return card
    
    # Data loading methods
    def refresh_recent_bookings(self):
        """Refresh recent bookings"""
        bookings = Booking.get_user_bookings(self.current_user.id)[:5]
        self.recent_bookings_table.setRowCount(len(bookings))
        
        for row, booking in enumerate(bookings):
            classroom = Classroom.get_classroom_by_id(booking.classroom_id)
            
            self.recent_bookings_table.setItem(row, 0, QTableWidgetItem(classroom.room_number if classroom else "Unknown"))
            self.recent_bookings_table.setItem(row, 1, QTableWidgetItem(str(booking.booking_date)))
            self.recent_bookings_table.setItem(row, 2, QTableWidgetItem(booking.start_time))
            self.recent_bookings_table.setItem(row, 3, QTableWidgetItem(booking.end_time))
            
            status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
            self.recent_bookings_table.setItem(row, 4, QTableWidgetItem(status_map.get(booking.status, "Unknown")))
    
    def refresh_schedule_for_day(self):
        """Refresh schedule table for selected day"""
        if not hasattr(self, 'schedule_table') or not hasattr(self, 'day_selector'):
            return
        
        selected_day = self.day_selector.currentText()
        
        # Get all schedules for Fall 2025, Semester 5
        db = DatabaseManager()
        query = '''
            SELECT s.*, u.fullname as teacher_name, c.room_number, c.building
            FROM schedules s
            LEFT JOIN users u ON s.teacher_id = u.id
            LEFT JOIN classrooms c ON s.classroom_id = c.id
            WHERE s.day_of_week = ? AND s.semester = 'Fall 2025'
            ORDER BY s.start_time
        '''
        results = db.execute_query(query, (selected_day,))
        
        if results:
            self.schedule_table.setRowCount(len(results))
            
            for row, schedule_data in enumerate(results):
                start_time = schedule_data[5]  # start_time
                end_time = schedule_data[6]    # end_time
                course_name = schedule_data[3] # course_name
                teacher_name = schedule_data[10] # teacher_name
                room_number = schedule_data[11]  # room_number
                building = schedule_data[12] if schedule_data[12] else "Main"
                
                # Calculate duration
                from datetime import datetime
                try:
                    start = datetime.strptime(start_time, "%H:%M")
                    end = datetime.strptime(end_time, "%H:%M")
                    duration_mins = int((end - start).total_seconds() / 60)
                    duration = f"{duration_mins} mins"
                except:
                    duration = "N/A"
                
                # Set table items
                self.schedule_table.setItem(row, 0, QTableWidgetItem(f"{start_time} - {end_time}"))
                self.schedule_table.setItem(row, 1, QTableWidgetItem(course_name or "N/A"))
                self.schedule_table.setItem(row, 2, QTableWidgetItem(teacher_name or "N/A"))
                self.schedule_table.setItem(row, 3, QTableWidgetItem(room_number or "N/A"))
                self.schedule_table.setItem(row, 4, QTableWidgetItem(building))
                self.schedule_table.setItem(row, 5, QTableWidgetItem(duration))
                
                # Color code by time of day
                time_hour = int(start_time.split(':')[0])
                if time_hour < 12:
                    color = QColor(240, 253, 244)  # Light green for morning
                elif time_hour < 15:
                    color = QColor(254, 249, 195)  # Light yellow for afternoon
                else:
                    color = QColor(239, 246, 255)  # Light blue for evening
                
                for col in range(6):
                    item = self.schedule_table.item(row, col)
                    if item:
                        item.setBackground(color)
        else:
            self.schedule_table.setRowCount(1)
            no_class = QTableWidgetItem("No classes scheduled for this day")
            no_class.setForeground(QColor(128, 128, 128))
            self.schedule_table.setItem(0, 0, no_class)
            self.schedule_table.setSpan(0, 0, 1, 6)
    
    def refresh_bookings_table(self):
        """Refresh bookings table"""
        bookings = Booking.get_user_bookings(self.current_user.id)
        self.bookings_table.setRowCount(len(bookings))
        
        for row, booking in enumerate(bookings):
            classroom = Classroom.get_classroom_by_id(booking.classroom_id)
            
            self.bookings_table.setItem(row, 0, QTableWidgetItem(str(booking.id)))
            self.bookings_table.setItem(row, 1, QTableWidgetItem(classroom.room_number if classroom else "Unknown"))
            self.bookings_table.setItem(row, 2, QTableWidgetItem(booking.course_name))
            self.bookings_table.setItem(row, 3, QTableWidgetItem(str(booking.booking_date)))
            self.bookings_table.setItem(row, 4, QTableWidgetItem(booking.start_time))
            self.bookings_table.setItem(row, 5, QTableWidgetItem(booking.end_time))
            
            status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
            status_text = status_map.get(booking.status, "Unknown")
            self.bookings_table.setItem(row, 6, QTableWidgetItem(status_text))
            
            # View button
            view_btn = QPushButton("View")
            view_btn.clicked.connect(lambda checked, b=booking: self.view_booking(b))
            view_btn.setMaximumWidth(80)
            self.bookings_table.setCellWidget(row, 7, view_btn)
            
            # Edit button (only for pending bookings)
            if booking.status == 2:  # Pending
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, b=booking: self.edit_booking(b))
                edit_btn.setMaximumWidth(80)
                self.bookings_table.setCellWidget(row, 8, edit_btn)
            else:
                self.bookings_table.setCellWidget(row, 8, QWidget())
            
            # Cancel/Action button
            if booking.status == 2:  # Pending
                cancel_btn = QPushButton("Cancel")
                cancel_btn.clicked.connect(lambda checked, b=booking: self.cancel_booking(b))
                cancel_btn.setMaximumWidth(80)
                cancel_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
                self.bookings_table.setCellWidget(row, 9, cancel_btn)
            else:
                self.bookings_table.setCellWidget(row, 9, QWidget())
    
    def search_available_rooms(self):
        """Search available rooms"""
        room_type = self.room_type_combo.currentText()
        if room_type == "All":
            classrooms = Classroom.get_all_classrooms()
        else:
            classrooms = Classroom.get_all_classrooms(room_type=room_type)
        
        self.available_rooms_table.setRowCount(len(classrooms))
        
        for row, classroom in enumerate(classrooms):
            self.available_rooms_table.setItem(row, 0, QTableWidgetItem(classroom.room_number))
            self.available_rooms_table.setItem(row, 1, QTableWidgetItem(classroom.room_type))
            self.available_rooms_table.setItem(row, 2, QTableWidgetItem(str(classroom.capacity)))
            self.available_rooms_table.setItem(row, 3, QTableWidgetItem(classroom.building))
            self.available_rooms_table.setItem(row, 4, QTableWidgetItem(str(classroom.floor)))
            
            book_btn = QPushButton("Book")
            book_btn.clicked.connect(lambda checked, c=classroom: self.book_room(c))
            self.available_rooms_table.setCellWidget(row, 5, book_btn)
    
    def refresh_schedules_table(self):
        """Refresh schedules table"""
        schedules = Schedule.get_teacher_schedules(self.current_user.id)
        self.schedules_table.setRowCount(len(schedules))
        
        for row, schedule in enumerate(schedules):
            classroom = Classroom.get_classroom_by_id(schedule.classroom_id)
            
            self.schedules_table.setItem(row, 0, QTableWidgetItem(schedule.course_name))
            self.schedules_table.setItem(row, 1, QTableWidgetItem(classroom.room_number if classroom else "Unknown"))
            self.schedules_table.setItem(row, 2, QTableWidgetItem(schedule.day_of_week))
            self.schedules_table.setItem(row, 3, QTableWidgetItem(schedule.start_time))
            self.schedules_table.setItem(row, 4, QTableWidgetItem(schedule.end_time))
            self.schedules_table.setItem(row, 5, QTableWidgetItem(schedule.semester or "N/A"))
    
    # Action methods
    def book_room(self, classroom):
        """Book a room"""
        dialog = BookingDialog(self, classroom, self.current_user)
        if dialog.exec_():
            self.refresh_bookings_table()
            self.refresh_recent_bookings()
    
    def cancel_booking(self, booking):
        """Cancel a booking"""
        reply = QMessageBox.question(self, "Cancel Booking", 
                                    "Are you sure you want to cancel this booking?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            reason, ok = self.get_reason_dialog("Cancellation Reason")
            if ok and reason:
                booking.cancel(self.current_user.id, reason)
                QMessageBox.information(self, "Success", "Booking cancelled!")
                self.refresh_bookings_table()
                self.refresh_recent_bookings()
    
    def view_booking(self, booking):
        """View booking details"""
        classroom = Classroom.get_classroom_by_id(booking.classroom_id)
        
        status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
        message = f"""
        Booking Details:
        
        ID: {booking.id}
        Room: {classroom.room_number if classroom else 'Unknown'}
        Course: {booking.course_name}
        Date: {booking.booking_date}
        Time: {booking.start_time} - {booking.end_time}
        Status: {status_map.get(booking.status, 'Unknown')}
        Description: {booking.description}
        """
        
        QMessageBox.information(self, "Booking Details", message)
    
    def edit_booking(self, booking):
        """Edit booking"""
        try:
            dialog = EditBookingDialog(booking, self)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_bookings_table()
                QMessageBox.information(self, "Success", "Booking updated successfully!")
        except Exception as e:
            print(f"Edit booking error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to edit booking:\n{str(e)}")
    
    def add_schedule(self):
        """Add schedule (for teachers)"""
        QMessageBox.information(self, "Add Schedule", "Schedule creation dialog would appear here.")
    
    def edit_profile(self):
        """Edit user profile"""
        try:
            # Create dialog for editing profile
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Profile")
            dialog.setGeometry(100, 100, 500, 400)
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Edit Your Profile")
            title.setFont(QFont("Segoe UI", 14, True))
            layout.addWidget(title)
            
            # Full Name
            layout.addWidget(QLabel("Full Name:"))
            fullname_input = QLineEdit()
            fullname_input.setText(self.current_user.fullname)
            fullname_input.setMinimumHeight(35)
            layout.addWidget(fullname_input)
            
            # Email
            layout.addWidget(QLabel("Email:"))
            email_input = QLineEdit()
            email_input.setText(self.current_user.email)
            email_input.setMinimumHeight(35)
            layout.addWidget(email_input)
            
            # Phone
            layout.addWidget(QLabel("Phone:"))
            phone_input = QLineEdit()
            phone_input.setText(self.current_user.phone if self.current_user.phone else "")
            phone_input.setMinimumHeight(35)
            layout.addWidget(phone_input)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_btn = QPushButton("Save")
            save_btn.setMinimumHeight(40)
            save_btn.clicked.connect(lambda: self.save_profile(
                fullname_input.text().strip(),
                email_input.text().strip(),
                phone_input.text().strip(),
                dialog
            ))
            button_layout.addWidget(save_btn)
            
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setMinimumHeight(40)
            cancel_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"Edit profile error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open edit dialog:\n{str(e)}")
    
    def save_profile(self, fullname, email, phone, dialog):
        """Save profile changes"""
        try:
            if not fullname or not email:
                QMessageBox.warning(self, "Validation Error", "Full name and email are required!")
                return
            
            from database.db_setup import DatabaseManager
            db = DatabaseManager()
            query = '''
                UPDATE users 
                SET fullname = ?, email = ?, phone = ?
                WHERE id = ?
            '''
            db.execute_update(query, (fullname, email, phone, self.current_user.id))
            
            # Update current user object
            self.current_user.fullname = fullname
            self.current_user.email = email
            self.current_user.phone = phone
            
            QMessageBox.information(self, "Success", "Profile updated successfully!")
            dialog.accept()
            self.refresh_profile_display()
        except Exception as e:
            print(f"Save profile error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save profile:\n{str(e)}")
    
    def refresh_profile_display(self):
        """Refresh the profile display on the Profile tab"""
        try:
            # Find and update the profile fields if they exist
            profile_tab = None
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == "Profile":
                    profile_tab = self.tabs.widget(i)
                    break
            
            if profile_tab:
                # Refresh the profile tab by recreating it
                profile_idx = self.tabs.indexOf(profile_tab)
                self.tabs.removeTab(profile_idx)
                new_profile_tab = self.create_profile_tab()
                self.tabs.insertTab(profile_idx, new_profile_tab, "Profile")
        except Exception as e:
            print(f"Refresh profile display error: {e}")
    
    def change_password(self):
        """Change password"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Change Password")
            dialog.setGeometry(100, 100, 450, 280)
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("Change Your Password")
            title.setFont(QFont("Segoe UI", 14, True))
            layout.addWidget(title)
            
            # Current Password
            layout.addWidget(QLabel("Current Password:"))
            current_pwd = QLineEdit()
            current_pwd.setEchoMode(QLineEdit.Password)
            current_pwd.setMinimumHeight(35)
            layout.addWidget(current_pwd)
            
            # New Password
            layout.addWidget(QLabel("New Password:"))
            new_pwd = QLineEdit()
            new_pwd.setEchoMode(QLineEdit.Password)
            new_pwd.setMinimumHeight(35)
            layout.addWidget(new_pwd)
            
            # Confirm Password
            layout.addWidget(QLabel("Confirm Password:"))
            confirm_pwd = QLineEdit()
            confirm_pwd.setEchoMode(QLineEdit.Password)
            confirm_pwd.setMinimumHeight(35)
            layout.addWidget(confirm_pwd)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            save_btn = QPushButton("Change Password")
            save_btn.setMinimumHeight(40)
            save_btn.clicked.connect(lambda: self.save_password(
                current_pwd.text(),
                new_pwd.text(),
                confirm_pwd.text(),
                dialog
            ))
            button_layout.addWidget(save_btn)
            
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setMinimumHeight(40)
            cancel_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            print(f"Change password error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to open change password dialog:\n{str(e)}")
    
    def save_password(self, current_pwd, new_pwd, confirm_pwd, dialog):
        """Save new password"""
        try:
            if not all([current_pwd, new_pwd, confirm_pwd]):
                QMessageBox.warning(self, "Validation Error", "All password fields are required!")
                return
            
            if new_pwd != confirm_pwd:
                QMessageBox.warning(self, "Validation Error", "New passwords do not match!")
                return
            
            if len(new_pwd) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters!")
                return
            
            # Verify current password
            from models.user import User
            hashed_current = User.hash_password(current_pwd)
            
            from database.db_setup import DatabaseManager
            db = DatabaseManager()
            result = db.execute_query(
                "SELECT password FROM users WHERE id = ?",
                (self.current_user.id,)
            )
            
            if not result or result[0][0] != hashed_current:
                QMessageBox.warning(self, "Error", "Current password is incorrect!")
                return
            
            # Update password
            hashed_new = User.hash_password(new_pwd)
            db.execute_update(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed_new, self.current_user.id)
            )
            
            QMessageBox.information(self, "Success", "Password changed successfully!")
            dialog.accept()
        except Exception as e:
            print(f"Save password error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to change password:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh all data"""
        self.refresh_bookings_table()
        self.refresh_recent_bookings()
        if self.current_user.role == 2:
            self.refresh_schedules_table()
        self.search_available_rooms()
        QMessageBox.information(self, "Success", "Data refreshed!")
    
    def export_bookings(self):
        """Export bookings to CSV file"""
        try:
            import csv
            import os
            from datetime import datetime
            
            # Get all bookings for current user
            bookings = Booking.get_user_bookings(self.current_user.id)
            
            if not bookings:
                QMessageBox.warning(self, "Export", "No bookings to export!")
                return
            
            # Create reports directory if it doesn't exist
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_path, "reports_output")
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"my_bookings_{timestamp}.csv"
            filepath = os.path.join(reports_dir, filename)
            
            # Write to CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Room', 'Course', 'Date', 'Start Time', 'End Time', 'Status'])
                
                status_map = {0: "Cancelled", 1: "Approved", 2: "Pending", 3: "Rejected"}
                for booking in bookings:
                    classroom = Classroom.get_classroom_by_id(booking.classroom_id)
                    room = classroom.room_number if classroom else "Unknown"
                    status = status_map.get(booking.status, "Unknown")
                    
                    writer.writerow([
                        booking.id,
                        room,
                        booking.course_name,
                        booking.booking_date,
                        booking.start_time,
                        booking.end_time,
                        status
                    ])
            
            QMessageBox.information(self, "Export", f"Bookings exported successfully!\n\nFile saved to:\n{filepath}")
        except Exception as e:
            print(f"Export error: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to export bookings:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Smart Campus Resource Management System
        Version 1.0.0
        
        © 2026 Smart Campus
        All rights reserved.
        """
        QMessageBox.information(self, "About", about_text)
    
    def contact_support(self):
        """Contact support"""
        QMessageBox.information(self, "Contact Support", 
                              "Email: hajrasarwar11@gmail.com\nPhone: 03273456789")
    
    def logout(self):
        """Logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
    
    @staticmethod
    def get_reason_dialog(title):
        """Get reason from user"""
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(None, title, "Reason:")
        return text, ok


class BookingDialog(QDialog):
    def __init__(self, parent, classroom, user):
        super().__init__(parent)
        self.classroom = classroom
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        """Initialize booking dialog"""
        self.setWindowTitle(f"Book Room: {self.classroom.room_number}")
        self.setGeometry(100, 100, 500, 400)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Room info
        layout.addWidget(QLabel(f"Room: {self.classroom.room_number} ({self.classroom.room_type})"))
        layout.addWidget(QLabel(f"Capacity: {self.classroom.capacity} persons"))
        
        # Course name
        layout.addWidget(QLabel("Course Name:"))
        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Enter course name")
        layout.addWidget(self.course_input)
        
        # Date
        layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate().addDays(1))
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)
        
        # Time
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("From:"))
        self.start_time = QComboBox()
        self.start_time.addItems(TIME_SLOTS)
        time_layout.addWidget(self.start_time)
        
        time_layout.addWidget(QLabel("To:"))
        self.end_time = QComboBox()
        self.end_time.addItems(TIME_SLOTS)
        time_layout.addWidget(self.end_time)
        layout.addLayout(time_layout)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter purpose of booking")
        self.desc_input.setMaximumHeight(100)
        layout.addWidget(self.desc_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        book_btn = QPushButton("Book Now")
        book_btn.clicked.connect(self.handle_booking)
        button_layout.addWidget(book_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def handle_booking(self):
        """Handle room booking"""
        course = self.course_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        
        if not course:
            QMessageBox.warning(self, "Error", "Please enter course name")
            return
        
        booking_date = self.date_input.date().toString("yyyy-MM-dd")
        start_time = self.start_time.currentText()
        end_time = self.end_time.currentText()
        
        # Check conflict
        if Booking.check_conflict(self.classroom.id, booking_date, start_time, end_time):
            QMessageBox.warning(self, "Conflict", "This time slot is already booked!")
            return
        
        # Create booking
        booking = Booking(
            user_id=self.user.id,
            classroom_id=self.classroom.id,
            course_name=course,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            description=description,
            status=2  # Pending
        )
        
        if booking.create(created_by=self.user.id):
            # Send admin notification email
            try:
                classroom = Classroom.get_classroom_by_id(self.classroom.id)
                EmailNotificationService.send_admin_notification_new_booking(booking, self.user, classroom)
            except Exception as e:
                print(f"Failed to send admin notification: {e}")
            
            QMessageBox.information(self, "Success", "Booking request submitted! Waiting for approval.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to create booking. Please try again.")
