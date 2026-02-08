"""
Database Setup and Management Module
"""

import sqlite3
import os
from datetime import datetime
import hashlib
from config import DB_PATH, COLORS

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    fullname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    phone TEXT,
                    role INTEGER DEFAULT 3,
                    status INTEGER DEFAULT 1,
                    department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Departments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Classrooms table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classrooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_number TEXT UNIQUE NOT NULL,
                    room_type TEXT NOT NULL,
                    capacity INTEGER,
                    building TEXT,
                    floor INTEGER,
                    description TEXT,
                    status INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Equipment table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    equipment_type TEXT NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    classroom_id INTEGER,
                    description TEXT,
                    status INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
                )
            ''')
            
            # Bookings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    classroom_id INTEGER NOT NULL,
                    course_name TEXT,
                    booking_date DATE NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    status INTEGER DEFAULT 2,
                    description TEXT,
                    created_by INTEGER,
                    cancelled_by INTEGER,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
                    FOREIGN KEY (created_by) REFERENCES users(id),
                    FOREIGN KEY (cancelled_by) REFERENCES users(id)
                )
            ''')
            
            # Schedules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER NOT NULL,
                    classroom_id INTEGER NOT NULL,
                    course_name TEXT NOT NULL,
                    day_of_week TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    semester TEXT,
                    status INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES users(id),
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
                )
            ''')
            
            # Reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    report_type TEXT,
                    generated_by INTEGER,
                    content TEXT,
                    file_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (generated_by) REFERENCES users(id)
                )
            ''')
            
            # Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            self.insert_default_data(conn)
            conn.close()
    
    def insert_default_data(self, conn):
        """Insert default data if tables are empty"""
        cursor = conn.cursor()
        
        # Check if users table is empty
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            # Insert default admin
            admin_password = hashlib.md5('admin123'.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, fullname, email, password, role, status, department)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', 'System Administrator', 'admin@smartcampus.edu', admin_password, 1, 1, 'ADMIN'))
        
        # Check if departments table is empty
        cursor.execute('SELECT COUNT(*) FROM departments')
        if cursor.fetchone()[0] == 0:
            departments = [
                ('Computer Science', 'CSE', 'Department of Computer Science and Engineering'),
                ('Business Administration', 'BBA', 'Department of Business Administration'),
                ('Electrical Engineering', 'EEE', 'Department of Electrical and Electronics Engineering'),
                ('Civil Engineering', 'CIVIL', 'Department of Civil Engineering'),
                ('Architecture', 'ARCH', 'Department of Architecture'),
                ('Administration', 'ADMIN', 'Administration Department'),
            ]
            cursor.executemany('''
                INSERT INTO departments (name, code, description)
                VALUES (?, ?, ?)
            ''', departments)
        
        # Check if classrooms table is empty
        cursor.execute('SELECT COUNT(*) FROM classrooms')
        if cursor.fetchone()[0] == 0:
            classrooms = [
                ('101', 'Theory', 50, 'Main Building', 1, 'Standard Classroom'),
                ('102', 'Theory', 50, 'Main Building', 1, 'Standard Classroom'),
                ('201', 'Lab', 30, 'Main Building', 2, 'Computer Lab'),
                ('202', 'Lab', 25, 'Main Building', 2, 'Physics Lab'),
                ('301', 'Seminar', 40, 'Annex Building', 3, 'Seminar Hall'),
                ('A01', 'Conference', 20, 'Admin Building', 1, 'Conference Room'),
            ]
            cursor.executemany('''
                INSERT INTO classrooms (room_number, room_type, capacity, building, floor, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', classrooms)
        
        conn.commit()
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return None
    
    def execute_update(self, query, params=()):
        """Execute an update/insert/delete query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database update error: {e}")
            return None
    
    def backup_database(self):
        """Create a backup of the database"""
        import shutil
        backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'smartcampus_backup_{timestamp}.db')
        shutil.copy2(self.db_path, backup_path)
        return backup_path


# Initialize database
db_manager = DatabaseManager()
