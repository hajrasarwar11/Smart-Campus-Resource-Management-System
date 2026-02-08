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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

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
                padding: 14px 24px;
                margin-right: 3px;
                font-size: 12px;
            }
        """)
        
        # Dashboard tab
        self.tabs.addTab(self.create_dashboard_tab(), "📊 Dashboard")
        
        # Users management tab
        self.tabs.addTab(self.create_users_tab(), "👥 Users")
        
        # Classrooms tab
        self.tabs.addTab(self.create_classrooms_tab(), "🏫 Classrooms")
        
        # Bookings tab
        self.tabs.addTab(self.create_bookings_tab(), "📅 Bookings")
        
        # Schedules tab
        self.tabs.addTab(self.create_schedules_tab(), "🗓️ Schedules")
        
        # Reports tab
        self.tabs.addTab(self.create_reports_tab(), "📈 Reports")
        
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
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #06B6D4, stop:1 #0891B2);
            padding: 20px;
        """)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("🎓 ADMIN DASHBOARD")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; letter-spacing: 1px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        user_label = QLabel(f"👤 {self.current_user.fullname}")
        user_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        user_label.setStyleSheet("color: #FFFFFF;")
        header_layout.addWidget(user_label)
        
        return header
    
    def create_dashboard_tab(self):
        """Create dashboard overview tab"""
        # Create scrollable widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome message
        welcome_box = QWidget()
        welcome_box.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #06B6D4, stop:1 #10B981);
            border-radius: 12px;
            padding: 20px;
        """)
        welcome_layout = QVBoxLayout(welcome_box)
        
        welcome_title = QLabel(f"👋 Welcome back, {self.current_user.fullname}!")
        welcome_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcome_title.setStyleSheet("color: #FFFFFF;")
        welcome_layout.addWidget(welcome_title)
        
        welcome_subtitle = QLabel(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
        welcome_subtitle.setFont(QFont("Segoe UI", 12))
        welcome_subtitle.setStyleSheet("color: rgba(255,255,255,0.9);")
        welcome_layout.addWidget(welcome_subtitle)
        
        layout.addWidget(welcome_box)
        
        # Stats
        stats_layout = QHBoxLayout()
        
        stats = [
            ("Total Users", self.count_users(), "#06B6D4"),
            ("Total Classrooms", self.count_classrooms(), "#10B981"),
            ("Total Bookings", self.count_bookings(), "#F59E0B"),
            ("Pending Approvals", self.count_pending_bookings(), "#EF4444"),
        ]
        
        for title, count, color in stats:
            stat_widget = self.create_stat_card(title, count, color)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        # Analytics Section
        analytics_row = QHBoxLayout()
        
        # Recent Activity Panel
        recent_activity = self.create_recent_activity_panel()
        analytics_row.addWidget(recent_activity, 40)
        
        # System Status Panel
        system_status = self.create_system_status_panel()
        analytics_row.addWidget(system_status, 30)
        
        # Quick Stats Panel
        quick_stats = self.create_quick_stats_panel()
        analytics_row.addWidget(quick_stats, 30)
        
        layout.addLayout(analytics_row)
        
        # Charts Section
        charts_label = QLabel("📊 ANALYTICS OVERVIEW")
        charts_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        charts_label.setStyleSheet("color: #06B6D4; margin-top: 10px;")
        layout.addWidget(charts_label)
        
        charts_row = QHBoxLayout()
        
        # Booking trends chart
        bookings_chart = self.create_bookings_chart_panel()
        charts_row.addWidget(bookings_chart)
        
        # Classroom utilization chart
        utilization_chart = self.create_utilization_chart_panel()
        charts_row.addWidget(utilization_chart)
        
        layout.addLayout(charts_row)
        
        # Weekly Trend Line Chart
        trend_label = QLabel("📈 WEEKLY BOOKING TRENDS")
        trend_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        trend_label.setStyleSheet("color: #06B6D4; margin-top: 10px;")
        layout.addWidget(trend_label)
        
        weekly_trend = self.create_weekly_trend_chart()
        layout.addWidget(weekly_trend)
        
        # Upcoming Events
        upcoming_label = QLabel("📅 UPCOMING EVENTS")
        upcoming_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        upcoming_label.setStyleSheet("color: #06B6D4; margin-top: 10px;")
        layout.addWidget(upcoming_label)
        
        upcoming_events = self.create_upcoming_events_panel()
        layout.addWidget(upcoming_events)
        
        layout.addStretch()
        
        scroll_area.setWidget(widget)
        return scroll_area
    
    def create_stat_card(self, title, value, color):
        """Create a stat card widget"""
        card = QWidget()
        card.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 {color}, stop:1 #0F172A);
            border: 2px solid {color};
            border-radius: 12px;
            padding: 25px;
        """)
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title.upper())
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #94A3B8; letter-spacing: 1px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 38, QFont.Bold))
        value_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(value_label)
        
        return card
    
    def create_recent_activity_panel(self):
        """Create recent activity panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("🔔 RECENT ACTIVITY")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Get recent bookings
        recent_bookings = Booking.get_recent_bookings(limit=5)
        
        if recent_bookings:
            for booking in recent_bookings:
                # Load user and classroom
                from models.user import User
                from models.classroom import Classroom
                user = User.get_user_by_id(booking.user_id)
                classroom = Classroom.get_classroom_by_id(booking.classroom_id)
                
                if not user or not classroom:
                    continue
                
                activity_item = QWidget()
                activity_layout = QHBoxLayout(activity_item)
                activity_layout.setContentsMargins(0, 5, 0, 5)
                
                status_colors = {
                    'Pending': '#F59E0B',
                    'Approved': '#10B981',
                    'Rejected': '#EF4444'
                }
                
                # Map status numbers to text
                status_map = {0: 'Cancelled', 1: 'Approved', 2: 'Pending', 3: 'Rejected'}
                status_text = status_map.get(booking.status, 'Unknown')
                color = status_colors.get(status_text, '#64748B')
                
                icon = QLabel("●")
                icon.setStyleSheet(f"color: {color}; font-size: 16px;")
                icon.setFixedWidth(20)
                activity_layout.addWidget(icon)
                
                text = QLabel(f"{user.fullname} - {classroom.room_number}")
                text.setFont(QFont("Segoe UI", 9))
                text.setStyleSheet("color: #E2E8F0;")
                activity_layout.addWidget(text)
                
                status_label = QLabel(status_text)
                status_label.setFont(QFont("Segoe UI", 8, QFont.Bold))
                status_label.setStyleSheet(f"color: {color};")
                activity_layout.addWidget(status_label)
                
                layout.addWidget(activity_item)
        else:
            no_activity = QLabel("No recent activity")
            no_activity.setStyleSheet("color: #64748B;")
            layout.addWidget(no_activity)
        
        layout.addStretch()
        return panel
    
    def create_system_status_panel(self):
        """Create system status panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("⚡ SYSTEM STATUS")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Database status
        db_status = QWidget()
        db_layout = QHBoxLayout(db_status)
        db_layout.setContentsMargins(0, 5, 0, 5)
        
        db_icon = QLabel("✓")
        db_icon.setStyleSheet("color: #10B981; font-size: 18px; font-weight: bold;")
        db_icon.setFixedWidth(30)
        db_layout.addWidget(db_icon)
        
        db_label = QLabel("Database Connected")
        db_label.setFont(QFont("Segoe UI", 10))
        db_label.setStyleSheet("color: #E2E8F0;")
        db_layout.addWidget(db_label)
        
        layout.addWidget(db_status)
        
        # Users online
        online_status = QWidget()
        online_layout = QHBoxLayout(online_status)
        online_layout.setContentsMargins(0, 5, 0, 5)
        
        online_icon = QLabel("👥")
        online_icon.setFixedWidth(30)
        online_layout.addWidget(online_icon)
        
        online_label = QLabel(f"{self.count_users()} Total Users")
        online_label.setFont(QFont("Segoe UI", 10))
        online_label.setStyleSheet("color: #E2E8F0;")
        online_layout.addWidget(online_label)
        
        layout.addWidget(online_status)
        
        # Storage
        storage_status = QWidget()
        storage_layout = QHBoxLayout(storage_status)
        storage_layout.setContentsMargins(0, 5, 0, 5)
        
        storage_icon = QLabel("💾")
        storage_icon.setFixedWidth(30)
        storage_layout.addWidget(storage_icon)
        
        storage_label = QLabel(f"{self.count_bookings()} Total Records")
        storage_label.setFont(QFont("Segoe UI", 10))
        storage_label.setStyleSheet("color: #E2E8F0;")
        storage_layout.addWidget(storage_label)
        
        layout.addWidget(storage_status)
        
        # Last backup
        backup_status = QWidget()
        backup_layout = QHBoxLayout(backup_status)
        backup_layout.setContentsMargins(0, 5, 0, 5)
        
        backup_icon = QLabel("🔄")
        backup_icon.setFixedWidth(30)
        backup_layout.addWidget(backup_icon)
        
        backup_label = QLabel("Auto-save Active")
        backup_label.setFont(QFont("Segoe UI", 10))
        backup_label.setStyleSheet("color: #E2E8F0;")
        backup_layout.addWidget(backup_label)
        
        layout.addWidget(backup_status)
        
        layout.addStretch()
        return panel
    
    def create_quick_stats_panel(self):
        """Create quick statistics panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("📈 QUICK STATS")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Today's bookings
        today_bookings = len([b for b in Booking.get_all_bookings() 
                             if b.booking_date == datetime.now().strftime('%Y-%m-%d')])
        
        stat1 = self.create_mini_stat("Today's Bookings", today_bookings, "#06B6D4")
        layout.addWidget(stat1)
        
        # Approval rate
        all_bookings = Booking.get_all_bookings()
        if all_bookings:
            approved_count = len([b for b in all_bookings if b.status == 1])  # status 1 = Approved
            approval_rate = int((approved_count / len(all_bookings)) * 100)
        else:
            approval_rate = 0
            
        stat2 = self.create_mini_stat("Approval Rate", f"{approval_rate}%", "#10B981")
        layout.addWidget(stat2)
        
        # Available classrooms
        total_rooms = self.count_classrooms()
        stat3 = self.create_mini_stat("Total Rooms", total_rooms, "#F59E0B")
        layout.addWidget(stat3)
        
        # Pending count
        pending = self.count_pending_bookings()
        stat4 = self.create_mini_stat("Needs Review", pending, "#EF4444")
        layout.addWidget(stat4)
        
        layout.addStretch()
        return panel
    
    def create_mini_stat(self, label, value, color):
        """Create a mini stat widget"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            background-color: #0F172A;
            border-left: 3px solid {color};
            border-radius: 6px;
            padding: 10px;
            margin: 5px 0;
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Segoe UI", 9))
        label_widget.setStyleSheet("color: #94A3B8;")
        layout.addWidget(label_widget)
        
        layout.addStretch()
        
        value_widget = QLabel(str(value))
        value_widget.setFont(QFont("Segoe UI", 14, QFont.Bold))
        value_widget.setStyleSheet(f"color: {color};")
        layout.addWidget(value_widget)
        
        return widget
    
    def create_bookings_chart_panel(self):
        """Create booking status bar chart"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 15px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("📊 BOOKING STATUS ANALYSIS")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Get booking status data
        bookings = Booking.get_all_bookings()
        status_map = {0: 'Cancelled', 1: 'Approved', 2: 'Pending', 3: 'Rejected'}
        status_counts = {'Approved': 0, 'Pending': 0, 'Rejected': 0, 'Cancelled': 0}
        
        for booking in bookings:
            status_text = status_map.get(booking.status, 'Unknown')
            if status_text in status_counts:
                status_counts[status_text] += 1
        
        # Create matplotlib chart
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        
        fig = Figure(figsize=(5.5, 3.5), dpi=100, facecolor='#1E293B')
        ax = fig.add_subplot(111)
        
        statuses = ['Approved', 'Pending', 'Rejected', 'Cancelled']
        counts = [status_counts[s] for s in statuses]
        colors = ['#10B981', '#F59E0B', '#EF4444', '#64748B']
        
        bars = ax.bar(statuses, counts, color=colors, edgecolor='#0F172A', linewidth=2.5, width=0.5)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(count)}',
                   ha='center', va='bottom', color='#FFFFFF', fontweight='bold', fontsize=13)
        
        ax.set_facecolor('#0F172A')
        ax.set_ylabel('Number of Bookings', color='#E2E8F0', fontsize=11, fontweight='bold')
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#94A3B8', labelsize=10, width=1.5, length=4)
        ax.grid(True, alpha=0.15, color='#475569', axis='y', linestyle='-', linewidth=0.5)
        ax.set_ylim(0, max(counts) * 1.15 if counts else 5)
        
        fig.tight_layout()
        
        canvas = FigureCanvasQTAgg(fig)
        canvas.setMinimumHeight(280)
        layout.addWidget(canvas, 1)
        
        return panel
    
    def create_utilization_chart_panel(self):
        """Create classroom utilization bar chart"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 15px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("🏫 TOP CLASSROOMS BY USAGE")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Get classroom booking counts
        from models.classroom import Classroom
        classrooms = Classroom.get_all_classrooms()
        bookings = Booking.get_all_bookings()
        
        classroom_counts = {}
        for classroom in classrooms:
            count = len([b for b in bookings if b.classroom_id == classroom.id])
            if classroom.room_number:
                classroom_counts[classroom.room_number] = count
        
        # Get top 6
        sorted_rooms = sorted(classroom_counts.items(), key=lambda x: x[1], reverse=True)[:6]
        
        # Create matplotlib chart
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        
        fig = Figure(figsize=(5.5, 3.5), dpi=100, facecolor='#1E293B')
        ax = fig.add_subplot(111)
        
        if sorted_rooms:
            rooms = [item[0] for item in sorted_rooms]
            counts = [item[1] for item in sorted_rooms]
            
            colors = ['#06B6D4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
            
            bars = ax.barh(rooms, counts, color=colors[:len(rooms)], edgecolor='#0F172A', linewidth=2)
            
            # Add value labels
            for bar, count in zip(bars, counts):
                width = bar.get_width()
                ax.text(width + 0.15, bar.get_y() + bar.get_height()/2.,
                       f'{int(count)}',
                       ha='left', va='center', color='#FFFFFF', fontweight='bold', fontsize=11)
        
        ax.set_facecolor('#0F172A')
        ax.set_xlabel('Number of Bookings', color='#E2E8F0', fontsize=11, fontweight='bold')
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#94A3B8', labelsize=10, width=1.5, length=4)
        ax.grid(True, alpha=0.15, color='#475569', axis='x', linestyle='-', linewidth=0.5)
        
        fig.tight_layout()
        
        canvas = FigureCanvasQTAgg(fig)
        canvas.setMinimumHeight(280)
        layout.addWidget(canvas, 1)
        
        return panel
    
    def create_weekly_trend_chart(self):
        """Create weekly booking trend line chart"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 15px;
        """)
        layout = QVBoxLayout(panel)
        
        title = QLabel("📈 WEEKLY BOOKING TRENDS")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #06B6D4; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Get bookings for last 7 days
        from datetime import timedelta
        bookings = Booking.get_all_bookings()
        
        # Create date range for last 7 days
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        date_labels = [(today - timedelta(days=i)).strftime('Sun' if (today - timedelta(days=i)).weekday() == 6 else 'Mon' if (today - timedelta(days=i)).weekday() == 0 else '%a') for i in range(6, -1, -1)]
        
        # Count bookings per day
        daily_counts = {date: 0 for date in dates}
        for booking in bookings:
            if booking.booking_date in daily_counts:
                daily_counts[booking.booking_date] += 1
        
        counts = [daily_counts[date] for date in dates]
        
        # Create matplotlib line chart
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        
        fig = Figure(figsize=(12, 3.5), dpi=100, facecolor='#1E293B')
        ax = fig.add_subplot(111)
        
        # Plot line with markers
        ax.plot(range(len(date_labels)), counts, color='#06B6D4', linewidth=3.5, marker='o', 
               markersize=10, markerfacecolor='#10B981', markeredgecolor='#06B6D4', 
               markeredgewidth=2.5, label='Bookings')
        
        # Fill area under curve
        ax.fill_between(range(len(date_labels)), counts, alpha=0.25, color='#06B6D4')
        
        # Add value labels on points
        for i, count in enumerate(counts):
            ax.text(i, count + 0.25, str(int(count)), ha='center', va='bottom', 
                   color='#FFFFFF', fontweight='bold', fontsize=11)
        
        # Styling
        ax.set_facecolor('#0F172A')
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#94A3B8', labelsize=10, width=1.5, length=4)
        ax.set_ylabel('Number of Bookings', color='#E2E8F0', fontsize=11, fontweight='bold')
        ax.set_xlabel('Day of Week', color='#E2E8F0', fontsize=11, fontweight='bold')
        ax.set_xticks(range(len(date_labels)))
        ax.set_xticklabels(date_labels, color='#94A3B8')
        ax.grid(True, alpha=0.15, color='#475569', linestyle='-', linewidth=0.5)
        ax.set_ylim(0, max(counts) * 1.2 if counts else 5)
        ax.legend(loc='upper left', facecolor='#0F172A', edgecolor='#334155', labelcolor='#E2E8F0', fontsize=10)
        
        fig.tight_layout()
        
        canvas = FigureCanvasQTAgg(fig)
        canvas.setMinimumHeight(300)
        canvas.setStyleSheet("background-color: #1E293B; border: none;")
        layout.addWidget(canvas, 1)
        
        return panel
    
    def create_upcoming_events_panel(self):
        """Create upcoming events panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 20px;
        """)
        layout = QHBoxLayout(panel)
        
        # Get upcoming bookings (today and future)
        today = datetime.now().strftime('%Y-%m-%d')
        all_bookings = Booking.get_all_bookings()
        upcoming = [b for b in all_bookings if b.booking_date >= today and b.status == 1]  # status 1 = Approved
        upcoming.sort(key=lambda x: (x.booking_date, x.start_time))
        
        if upcoming[:4]:  # Show first 4
            for booking in upcoming[:4]:
                # Load user and classroom
                from models.user import User
                from models.classroom import Classroom
                user = User.get_user_by_id(booking.user_id)
                classroom = Classroom.get_classroom_by_id(booking.classroom_id)
                
                if not user or not classroom:
                    continue
                
                event_card = QWidget()
                event_card.setStyleSheet("""
                    background-color: #0F172A;
                    border: 2px solid #334155;
                    border-radius: 8px;
                    padding: 15px;
                """)
                event_layout = QVBoxLayout(event_card)
                
                room_label = QLabel(f"🏫 {classroom.room_number}")
                room_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
                room_label.setStyleSheet("color: #06B6D4;")
                event_layout.addWidget(room_label)
                
                user_label = QLabel(f"👤 {user.fullname}")
                user_label.setFont(QFont("Segoe UI", 9))
                user_label.setStyleSheet("color: #E2E8F0;")
                event_layout.addWidget(user_label)
                
                date_label = QLabel(f"📅 {booking.booking_date}")
                date_label.setFont(QFont("Segoe UI", 9))
                date_label.setStyleSheet("color: #94A3B8;")
                event_layout.addWidget(date_label)
                
                time_label = QLabel(f"⏰ {booking.start_time} - {booking.end_time}")
                time_label.setFont(QFont("Segoe UI", 9))
                time_label.setStyleSheet("color: #94A3B8;")
                event_layout.addWidget(time_label)
                
                layout.addWidget(event_card)
        else:
            no_events = QLabel("📭 No upcoming events")
            no_events.setFont(QFont("Segoe UI", 12))
            no_events.setStyleSheet("color: #64748B;")
            no_events.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_events)
        
        return panel
    
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: #0F172A; border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 Reports & Analytics Center")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #06B6D4;")
        scroll_layout.addWidget(title)
        
        # Report buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        reports = [
            ("Resource Usage Report", self.report_resource_usage),
            ("Booking Statistics", self.report_booking_stats),
            ("Teacher Schedule Report", self.report_teacher_schedule),
            ("Export All Data", self.export_data),
        ]
        
        for report_name, callback in reports:
            btn = QPushButton(report_name)
            btn.setMinimumHeight(50)
            btn.setMinimumWidth(120)
            btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0891B2);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0E7490);
                }
            """)
            btn.clicked.connect(callback)
            buttons_layout.addWidget(btn)
        
        scroll_layout.addLayout(buttons_layout)
        
        # Statistics cards row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # Get data for stats
        total_bookings = len(Booking.get_all_bookings())
        total_classrooms = len(Classroom.get_all_classrooms())
        total_users = len(User.get_all_users())
        total_schedules = len(Schedule.get_all_schedules())
        
        stats = [
            ("📅 Total Bookings", str(total_bookings), "#06B6D4"),
            ("🏫 Classrooms", str(total_classrooms), "#10B981"),
            ("👥 Users", str(total_users), "#F59E0B"),
            ("🗓️ Schedules", str(total_schedules), "#EF4444"),
        ]
        
        for label, value, color in stats:
            card = self.create_stat_card_reports(label, value, color)
            stats_layout.addWidget(card)
        
        scroll_layout.addLayout(stats_layout)
        
        # Charts row
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Booking status distribution chart
        booking_chart = self.create_booking_status_chart_reports()
        charts_layout.addWidget(booking_chart)
        
        # Classroom type distribution chart
        classroom_chart = self.create_classroom_distribution_chart()
        charts_layout.addWidget(classroom_chart)
        
        scroll_layout.addLayout(charts_layout)
        
        # Report summary section
        summary_title = QLabel("📋 Report Summary")
        summary_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        summary_title.setStyleSheet("color: #06B6D4; margin-top: 10px;")
        scroll_layout.addWidget(summary_title)
        
        # Summary cards layout
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # Recent bookings summary
        recent_bookings = Booking.get_all_bookings()[-5:] if Booking.get_all_bookings() else []
        
        bookings_card = QWidget()
        bookings_card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        bookings_layout = QVBoxLayout(bookings_card)
        
        bookings_title = QLabel("🔔 Recent Bookings")
        bookings_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        bookings_title.setStyleSheet("color: #06B6D4;")
        bookings_layout.addWidget(bookings_title)
        
        if recent_bookings:
            for booking in recent_bookings[-3:]:
                status_map = {0: 'Cancelled', 1: 'Approved', 2: 'Pending', 3: 'Rejected'}
                status_text = status_map.get(booking.status, 'Unknown')
                status_colors = {
                    'Approved': '#10B981',
                    'Pending': '#F59E0B',
                    'Rejected': '#EF4444',
                    'Cancelled': '#64748B'
                }
                color = status_colors.get(status_text, '#64748B')
                
                entry = QLabel(f"• {booking.booking_date} - {status_text}")
                entry.setStyleSheet(f"color: {color}; font-size: 10px;")
                bookings_layout.addWidget(entry)
        else:
            empty = QLabel("No recent bookings")
            empty.setStyleSheet("color: #94A3B8;")
            bookings_layout.addWidget(empty)
        
        bookings_layout.addStretch()
        summary_layout.addWidget(bookings_card)
        
        # Peak hours summary
        peak_card = QWidget()
        peak_card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        peak_layout = QVBoxLayout(peak_card)
        
        peak_title = QLabel("⏰ System Stats")
        peak_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        peak_title.setStyleSheet("color: #06B6D4;")
        peak_layout.addWidget(peak_title)
        
        approved_count = len([b for b in Booking.get_all_bookings() if b.status == 1])
        pending_count = len([b for b in Booking.get_all_bookings() if b.status == 2])
        approval_rate = (approved_count / total_bookings * 100) if total_bookings > 0 else 0
        
        stats_text = [
            f"✓ Approved: {approved_count}",
            f"⏳ Pending: {pending_count}",
            f"📊 Approval Rate: {approval_rate:.1f}%",
            f"🔄 System Status: Online",
        ]
        
        for stat in stats_text:
            stat_label = QLabel(stat)
            stat_label.setStyleSheet("color: #E2E8F0; font-size: 10px;")
            peak_layout.addWidget(stat_label)
        
        peak_layout.addStretch()
        summary_layout.addWidget(peak_card)
        
        # Room utilization summary
        util_card = QWidget()
        util_card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        util_layout = QVBoxLayout(util_card)
        
        util_title = QLabel("🏢 Utilization")
        util_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        util_title.setStyleSheet("color: #06B6D4;")
        util_layout.addWidget(util_title)
        
        if total_classrooms > 0 and total_bookings > 0:
            utilization = (total_bookings / total_classrooms)
            util_label = QLabel(f"Avg Bookings/Room: {utilization:.1f}")
            util_label.setStyleSheet("color: #10B981; font-size: 10px; font-weight: bold;")
            util_layout.addWidget(util_label)
        
        peak_percentage = (len([b for b in Booking.get_all_bookings() if b.status == 1]) / total_bookings * 100) if total_bookings > 0 else 0
        peak_label = QLabel(f"Approval Rate: {peak_percentage:.1f}%")
        peak_label.setStyleSheet("color: #06B6D4; font-size: 10px;")
        util_layout.addWidget(peak_label)
        
        capacity_sum = sum([c.capacity for c in Classroom.get_all_classrooms()])
        capacity_label = QLabel(f"Total Capacity: {capacity_sum}")
        capacity_label.setStyleSheet("color: #F59E0B; font-size: 10px;")
        util_layout.addWidget(capacity_label)
        
        util_layout.addStretch()
        summary_layout.addWidget(util_card)
        
        scroll_layout.addLayout(summary_layout)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
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
            edit_btn.setStyleSheet("background-color: #06B6D4; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.users_table.setCellWidget(row, 6, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, u=user: self.delete_user(u))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
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
            edit_btn.setStyleSheet("background-color: #06B6D4; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.classrooms_table.setCellWidget(row, 6, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, c=classroom: self.delete_classroom(c))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.classrooms_table.setCellWidget(row, 7, delete_btn)
            
            # QR Code button
            qr_btn = QPushButton("QR Code")
            qr_btn.clicked.connect(lambda checked, c=classroom: self.generate_classroom_qr(c))
            qr_btn.setMaximumWidth(80)
            qr_btn.setStyleSheet("background-color: #8B5CF6; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
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
            view_btn.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.bookings_table.setCellWidget(row, 7, view_btn)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, b=booking: self.edit_booking(b))
            edit_btn.setMaximumWidth(80)
            edit_btn.setStyleSheet("background-color: #06B6D4; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.bookings_table.setCellWidget(row, 8, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, b=booking: self.delete_booking(b))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
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
            edit_btn.setStyleSheet("background-color: #06B6D4; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
            self.schedules_table.setCellWidget(row, 7, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, s=schedule: self.delete_schedule(s))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; border: none; padding: 5px; border-radius: 4px;")
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
            
            # Apply dark theme styling
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #1E293B;
                }
                QLabel {
                    color: #E2E8F0;
                    font-size: 11px;
                }
                QLineEdit, QTextEdit {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    border: 2px solid #334155;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus, QTextEdit:focus {
                    border: 2px solid #06B6D4;
                }
                QPushButton {
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 11px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #0891B2);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0891B2, stop:1 #0E7490);
                }
            """)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("System Configuration")
            title.setFont(QFont("Segoe UI", 14, QFont.Bold))
            title.setStyleSheet("color: #06B6D4; font-size: 14px; margin-bottom: 10px;")
            layout.addWidget(title)
            
            # Database Settings Section
            db_group = QLabel("Database Settings")
            db_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
            db_group.setStyleSheet("color: #06B6D4;")
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
            uni_group.setStyleSheet("color: #06B6D4;")
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
            stats_group.setStyleSheet("color: #06B6D4;")
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
    
    def create_stat_card_reports(self, title, value, color):
        """Create stat card for reports tab"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border-left: 5px solid {color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        card.setMinimumHeight(120)
        card.setMinimumWidth(180)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        return card
    
    def create_booking_status_chart_reports(self):
        """Create booking status pie chart for reports tab"""
        container = QWidget()
        container.setMinimumHeight(320)
        container.setStyleSheet("background: #0F172A; border-radius: 8px; border: 1px solid #334155;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Add title
        chart_title = QLabel("📊 Booking Status Distribution")
        chart_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        chart_title.setStyleSheet("color: #06B6D4;")
        layout.addWidget(chart_title)
        
        try:
            # Get booking data
            bookings = Booking.get_all_bookings()
            status_map = {0: 'Cancelled', 1: 'Approved', 2: 'Pending', 3: 'Rejected'}
            status_counts = {status: 0 for status in status_map.values()}
            
            for booking in bookings:
                status_text = status_map.get(booking.status, 'Unknown')
                status_counts[status_text] += 1
            
            # Create figure
            fig = plt.Figure(figsize=(5, 3), dpi=100, facecolor='#0F172A')
            ax = fig.add_subplot(111)
            
            labels = list(status_counts.keys())
            sizes = list(status_counts.values())
            colors = ['#EF4444', '#10B981', '#F59E0B', '#64748B']
            
            if sum(sizes) > 0:
                # Create pie chart with legend instead of direct labels
                wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%',
                                                    startangle=90,
                                                    textprops={'color': 'white', 'fontsize': 11, 'weight': 'bold'},
                                                    pctdistance=0.8)
                
                # Style percentage text
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(11)
                
                # Add legend
                ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                         fontsize=10, frameon=False, labelcolor='#E2E8F0')
            else:
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center', color='#94A3B8', fontsize=12)
            
            ax.set_title('', color='#06B6D4', fontsize=11, fontweight='bold')
            
            canvas = FigureCanvasQTAgg(fig)
            layout.addWidget(canvas)
            
        except Exception as e:
            error_label = QLabel(f"Chart Error: {str(e)}")
            error_label.setStyleSheet("color: #EF4444;")
            layout.addWidget(error_label)
        
        return container
    
    def create_classroom_distribution_chart(self):
        """Create classroom type distribution chart for reports tab"""
        container = QWidget()
        container.setMinimumHeight(320)
        container.setStyleSheet("background: #0F172A; border-radius: 8px; border: 1px solid #334155;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Add title
        chart_title = QLabel("🏫 Classroom Types Distribution")
        chart_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        chart_title.setStyleSheet("color: #06B6D4;")
        layout.addWidget(chart_title)
        
        try:
            # Get classroom data
            classrooms = Classroom.get_all_classrooms()
            room_types = {}
            
            for classroom in classrooms:
                room_type = classroom.room_type
                room_types[room_type] = room_types.get(room_type, 0) + 1
            
            # Create figure
            fig = plt.Figure(figsize=(5, 3), dpi=100, facecolor='#0F172A')
            ax = fig.add_subplot(111)
            
            if room_types:
                labels = list(room_types.keys())
                sizes = list(room_types.values())
                colors = ['#06B6D4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
                
                bars = ax.bar(labels, sizes, color=colors[:len(labels)], edgecolor='#334155', linewidth=1.5)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}',
                           ha='center', va='bottom', color='#E2E8F0', fontsize=11, fontweight='bold')
                
                ax.set_ylabel('Count', color='#E2E8F0', fontsize=10, fontweight='bold')
                ax.set_xlabel('')
                ax.tick_params(axis='both', colors='#E2E8F0', labelsize=10)
                ax.spines['left'].set_color('#334155')
                ax.spines['bottom'].set_color('#334155')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.grid(axis='y', color='#1E293B', linestyle='--', alpha=0.5)
            else:
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center', color='#94A3B8', fontsize=12)
            
            ax.set_title('', color='#06B6D4', fontsize=11, fontweight='bold')
            
            canvas = FigureCanvasQTAgg(fig)
            layout.addWidget(canvas)
            
        except Exception as e:
            error_label = QLabel(f"Chart Error: {str(e)}")
            error_label.setStyleSheet("color: #EF4444;")
            layout.addWidget(error_label)
        
        return container
    
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
