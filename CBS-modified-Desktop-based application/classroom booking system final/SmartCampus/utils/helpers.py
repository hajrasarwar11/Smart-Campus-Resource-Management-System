"""
Helper Utilities Module
"""

import hashlib
import re
from datetime import datetime, timedelta
import json
import os

class DateTimeHelper:
    """Helper functions for date/time operations"""
    
    @staticmethod
    def is_future_date(date_str):
        """Check if date is in the future"""
        from datetime import datetime
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return date >= datetime.now().date()
        except ValueError:
            return False
    
    @staticmethod
    def format_date(date_obj):
        """Format date object to string"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime('%Y-%m-%d')
    
    @staticmethod
    def format_time(time_str):
        """Format time string"""
        try:
            time_obj = datetime.strptime(time_str, '%H:%M')
            return time_obj.strftime('%H:%M')
        except ValueError:
            return time_str
    
    @staticmethod
    def get_week_days():
        """Get week days list"""
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    @staticmethod
    def date_range(start_date, end_date):
        """Generate date range"""
        from datetime import datetime, timedelta
        current = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        while current <= end:
            yield current.strftime('%Y-%m-%d')
            current += timedelta(days=1)


class StringHelper:
    """Helper functions for string operations"""
    
    @staticmethod
    def truncate(text, length=50):
        """Truncate text to specified length"""
        if len(text) > length:
            return text[:length-3] + '...'
        return text
    
    @staticmethod
    def camel_to_snake(name):
        """Convert camelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(name):
        """Convert snake_case to camelCase"""
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def capitalize_words(text):
        """Capitalize each word"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def slugify(text):
        """Convert text to slug format"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')


class NumberHelper:
    """Helper functions for number operations"""
    
    @staticmethod
    def format_number(number, decimals=2):
        """Format number with decimals"""
        return f"{number:.{decimals}f}"
    
    @staticmethod
    def percentage(part, whole):
        """Calculate percentage"""
        if whole == 0:
            return 0
        return (part / whole) * 100
    
    @staticmethod
    def round_to_nearest(number, nearest=5):
        """Round to nearest value"""
        return round(number / nearest) * nearest


class ListHelper:
    """Helper functions for list operations"""
    
    @staticmethod
    def chunk_list(lst, chunk_size):
        """Split list into chunks"""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    @staticmethod
    def unique(lst):
        """Get unique items from list"""
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def flatten(nested_list):
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(ListHelper.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def group_by(lst, key_func):
        """Group list items by key function"""
        groups = {}
        for item in lst:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups


class FileHelper:
    """Helper functions for file operations"""
    
    @staticmethod
    def ensure_directory(directory):
        """Create directory if it doesn't exist"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    
    @staticmethod
    def get_file_size(filepath):
        """Get file size in human readable format"""
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    @staticmethod
    def read_json(filepath):
        """Read JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    @staticmethod
    def write_json(filepath, data):
        """Write JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing JSON: {e}")
            return False


class ValidationHelper:
    """Additional validation helpers"""
    
    @staticmethod
    def is_valid_id(value):
        """Check if value is valid ID (positive integer)"""
        try:
            return int(value) > 0
        except ValueError:
            return False
    
    @staticmethod
    def is_alphanumeric(value):
        """Check if string is alphanumeric"""
        return value.isalnum()
    
    @staticmethod
    def is_numeric(value):
        """Check if string is numeric"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_url(value):
        """Check if string is valid URL"""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(value) is not None


class CryptographyHelper:
    """Helper functions for encryption/hashing"""
    
    @staticmethod
    def sha256(text):
        """Generate SHA256 hash"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def sha1(text):
        """Generate SHA1 hash"""
        return hashlib.sha1(text.encode()).hexdigest()
    
    @staticmethod
    def md5(text):
        """Generate MD5 hash"""
        return hashlib.md5(text.encode()).hexdigest()


class NotificationHelper:
    """Helper for notifications and alerts"""
    
    @staticmethod
    def format_notification(title, message, notification_type='info'):
        """Format notification"""
        types = {
            'success': '✓',
            'error': '✗',
            'warning': '⚠',
            'info': 'ℹ'
        }
        icon = types.get(notification_type, 'ℹ')
        return f"{icon} {title}\n{message}"


class LoggerHelper:
    """Helper for logging"""
    
    @staticmethod
    def log_action(user_id, action, details='', log_file='activity.log'):
        """Log user action"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] User: {user_id} | Action: {action} | Details: {details}\n"
        
        try:
            with open(log_file, 'a') as f:
                f.write(log_entry)
            return True
        except Exception as e:
            print(f"Error writing log: {e}")
            return False


class CacheHelper:
    """Simple in-memory cache helper"""
    
    _cache = {}
    
    @classmethod
    def set(cls, key, value, ttl=None):
        """Set cache value"""
        cls._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl) if ttl else None
        }
    
    @classmethod
    def get(cls, key):
        """Get cache value"""
        if key in cls._cache:
            cache_item = cls._cache[key]
            if cache_item['expires_at'] is None or cache_item['expires_at'] > datetime.now():
                return cache_item['value']
            else:
                del cls._cache[key]
        return None
    
    @classmethod
    def delete(cls, key):
        """Delete cache value"""
        if key in cls._cache:
            del cls._cache[key]
    
    @classmethod
    def clear(cls):
        """Clear all cache"""
        cls._cache.clear()
