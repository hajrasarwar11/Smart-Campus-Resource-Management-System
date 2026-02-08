# Configuration file for Smart Campus Resource Management System

import os
from datetime import datetime

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'smartcampus.db')
DB_NAME = 'smartcampus'

# University Configuration
UNIVERSITY_NAME = "Fatima Jinnah Women University"
SESSION = "2023-2027"
SEMESTER = 5
SECTION = "A"

# Application Settings
APP_NAME = "Smart Campus Resource Management System"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

# User Roles
USER_ROLES = {
    1: 'Admin',
    2: 'Teacher',
    3: 'Student'
}

# User Status
USER_STATUS = {
    0: 'Inactive',
    1: 'Active',
    2: 'Pending'
}

# Booking Status
BOOKING_STATUS = {
    0: 'Cancelled',
    1: 'Approved',
    2: 'Pending',
    3: 'Rejected'
}

# Room Types
ROOM_TYPES = ['Theory', 'Lab', 'Seminar', 'Conference']

# Equipment Types
EQUIPMENT_TYPES = [
    'Projector',
    'Computer',
    'Whiteboard',
    'Smart Board',
    'Microscope',
    'Oscilloscope',
    'Lab Kit'
]

# Time Slots
TIME_SLOTS = [
    '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', 
    '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'
]

# Department Codes
DEPARTMENTS = [
    'CSE', 'BBA', 'EEE', 'CIVIL', 'ARCH', 'ADMIN'
]

# Color Scheme (Modern Professional)
COLORS = {
    'primary': '#2563EB',        # Blue
    'secondary': '#1E40AF',      # Dark Blue
    'success': '#059669',        # Green
    'danger': '#DC2626',         # Red
    'warning': '#F59E0B',        # Amber
    'info': '#0EA5E9',           # Sky Blue
    'light': '#F3F4F6',          # Light Gray
    'dark': '#1F2937',           # Dark Gray
    'white': '#FFFFFF',
    'border': '#E5E7EB',
    'hover': '#1D4ED8'
}

# Font Configuration
FONTS = {
    'title': ('Segoe UI', 14, 'bold'),
    'heading': ('Segoe UI', 12, 'bold'),
    'label': ('Segoe UI', 10),
    'input': ('Segoe UI', 10),
    'small': ('Segoe UI', 9)
}

# Pagination
ITEMS_PER_PAGE = 10

# Session Timeout (minutes)
SESSION_TIMEOUT = 30

# Logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')
LOG_LEVEL = 'INFO'

# Email Configuration
EMAIL_CONFIG = {
    'sender_email': 'smartcampus.fjwu@gmail.com',
    'sender_password': 'qjxm mlun ugzw ijvr',  # Gmail App-specific password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'support_email': 'hajrasarwar11@gmail.com',
    'support_phone': '03273456789'
}

# Default Admin Credentials (Change in production!)
DEFAULT_ADMIN = {
    'username': 'admin',
    'password': 'admin123',
    'email': 'admin@smartcampus.edu'
}
