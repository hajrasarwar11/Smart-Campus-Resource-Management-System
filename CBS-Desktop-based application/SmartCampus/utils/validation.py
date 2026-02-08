"""
Validation Utilities
"""

import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_username(username):
        """Validate username"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            return False, "Username can only contain letters, numbers, dash and underscore"
        return True, "Valid"
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "Valid"
        return False, "Invalid email address"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        return True, "Valid"
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        phone = re.sub(r'[^\d+]', '', phone)
        if len(phone) < 10:
            return False, "Phone number must be at least 10 digits"
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_str):
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Valid"
        except ValueError:
            return False, "Invalid date format (use YYYY-MM-DD)"
    
    @staticmethod
    def validate_time(time_str):
        """Validate time format (HH:MM)"""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True, "Valid"
        except ValueError:
            return False, "Invalid time format (use HH:MM)"
    
    @staticmethod
    def validate_time_range(start_time, end_time):
        """Validate that end_time is after start_time"""
        try:
            start = datetime.strptime(start_time, '%H:%M')
            end = datetime.strptime(end_time, '%H:%M')
            if end > start:
                return True, "Valid"
            return False, "End time must be after start time"
        except ValueError:
            return False, "Invalid time format"
    
    @staticmethod
    def validate_room_number(room_number):
        """Validate room number"""
        if not room_number or len(room_number) < 2:
            return False, "Room number is required"
        if not re.match("^[a-zA-Z0-9-]+$", room_number):
            return False, "Invalid room number format"
        return True, "Valid"
    
    @staticmethod
    def validate_capacity(capacity):
        """Validate room capacity"""
        try:
            cap = int(capacity)
            if 5 <= cap <= 500:
                return True, "Valid"
            return False, "Capacity must be between 5 and 500"
        except ValueError:
            return False, "Capacity must be a number"
    
    @staticmethod
    def validate_fullname(fullname):
        """Validate full name"""
        if not fullname or len(fullname) < 3:
            return False, "Name must be at least 3 characters long"
        if not re.match(r"^[a-zA-Z\s.'-]+$", fullname):
            return False, "Name contains invalid characters"
        return True, "Valid"
    
    @staticmethod
    def validate_form_data(data_dict):
        """Validate multiple form fields"""
        errors = {}
        
        for field, value in data_dict.items():
            if not value:
                errors[field] = f"{field} is required"
        
        return len(errors) == 0, errors
    
    @staticmethod
    def is_future_date(date_str):
        """Check if date is in the future"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return date >= datetime.now().date()
        except ValueError:
            return False
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize user input to prevent SQL injection"""
        if not isinstance(text, str):
            return text
        # Remove dangerous characters
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/"]
        for char in dangerous_chars:
            text = text.replace(char, "")
        return text.strip()


class FormValidator:
    """Comprehensive form validation"""
    
    def __init__(self):
        self.errors = {}
    
    def add_error(self, field, message):
        """Add validation error"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def is_valid(self):
        """Check if form is valid"""
        return len(self.errors) == 0
    
    def get_errors(self):
        """Get all errors"""
        return self.errors
    
    def validate_login_form(self, username, password):
        """Validate login form"""
        self.errors = {}
        
        if not username:
            self.add_error('username', 'Username is required')
        if not password:
            self.add_error('password', 'Password is required')
        
        return self.is_valid()
    
    def validate_registration_form(self, data):
        """Validate registration form"""
        self.errors = {}
        
        valid, msg = Validator.validate_username(data.get('username', ''))
        if not valid:
            self.add_error('username', msg)
        
        valid, msg = Validator.validate_email(data.get('email', ''))
        if not valid:
            self.add_error('email', msg)
        
        valid, msg = Validator.validate_password(data.get('password', ''))
        if not valid:
            self.add_error('password', msg)
        
        valid, msg = Validator.validate_fullname(data.get('fullname', ''))
        if not valid:
            self.add_error('fullname', msg)
        
        return self.is_valid()
    
    def validate_booking_form(self, data):
        """Validate booking form"""
        self.errors = {}
        
        if not data.get('course_name'):
            self.add_error('course_name', 'Course name is required')
        
        valid, msg = Validator.validate_date(data.get('booking_date', ''))
        if not valid:
            self.add_error('booking_date', msg)
        
        valid, msg = Validator.validate_time(data.get('start_time', ''))
        if not valid:
            self.add_error('start_time', msg)
        
        valid, msg = Validator.validate_time(data.get('end_time', ''))
        if not valid:
            self.add_error('end_time', msg)
        
        if data.get('start_time') and data.get('end_time'):
            valid, msg = Validator.validate_time_range(data.get('start_time'), data.get('end_time'))
            if not valid:
                self.add_error('time_range', msg)
        
        return self.is_valid()
