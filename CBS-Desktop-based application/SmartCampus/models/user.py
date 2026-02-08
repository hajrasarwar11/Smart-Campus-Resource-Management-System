"""
User Model Module
"""

import hashlib
from datetime import datetime
from database.db_setup import DatabaseManager

class User:
    def __init__(self, username=None, fullname=None, email=None, password=None, 
                 phone=None, role=3, status=1, department=None):
        self.id = None
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role  # 1=Admin, 2=Teacher, 3=Student
        self.status = status
        self.department = department
        self.created_at = None
        self.db = DatabaseManager()
    
    @staticmethod
    def hash_password(password):
        """Hash password using MD5"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def register(self):
        """Register a new user"""
        try:
            hashed_password = self.hash_password(self.password)
            query = '''
                INSERT INTO users (username, fullname, email, password, phone, role, status, department)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.id = self.db.execute_update(query, (
                self.username, self.fullname, self.email, hashed_password,
                self.phone, self.role, self.status, self.department
            ))
            return self.id is not None
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    @staticmethod
    def login(username, password):
        """Authenticate user"""
        try:
            db = DatabaseManager()
            hashed_password = User.hash_password(password)
            query = '''
                SELECT * FROM users 
                WHERE username = ? AND password = ? AND status = 1
            '''
            results = db.execute_query(query, (username, hashed_password))
            
            if results:
                user_data = results[0]
                user = User(
                    username=user_data[1],
                    fullname=user_data[2],
                    email=user_data[3],
                    phone=user_data[5],
                    role=user_data[6],
                    status=user_data[7],
                    department=user_data[8]
                )
                user.id = user_data[0]
                user.created_at = user_data[10]
                return user
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            db = DatabaseManager()
            query = 'SELECT * FROM users WHERE id = ?'
            results = db.execute_query(query, (user_id,))
            
            if results:
                user_data = results[0]
                user = User(
                    username=user_data[1],
                    fullname=user_data[2],
                    email=user_data[3],
                    phone=user_data[5],
                    role=user_data[6],
                    status=user_data[7],
                    department=user_data[8]
                )
                user.id = user_data[0]
                return user
            return None
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    @staticmethod
    def get_all_users(role=None):
        """Get all users or users by role"""
        try:
            db = DatabaseManager()
            if role:
                query = 'SELECT * FROM users WHERE role = ? ORDER BY fullname'
                results = db.execute_query(query, (role,))
            else:
                query = 'SELECT * FROM users ORDER BY fullname'
                results = db.execute_query(query)
            
            users = []
            if results:
                for row in results:
                    user = User(
                        username=row[1],
                        fullname=row[2],
                        email=row[3],
                        phone=row[5],
                        role=row[6],
                        status=row[7],
                        department=row[8]
                    )
                    user.id = row[0]
                    users.append(user)
            return users
        except Exception as e:
            print(f"Get all users error: {e}")
            return []
    
    def update_profile(self):
        """Update user profile"""
        try:
            query = '''
                UPDATE users 
                SET fullname = ?, email = ?, phone = ?, department = ?, updated_at = ?
                WHERE id = ?
            '''
            self.db.execute_update(query, (
                self.fullname, self.email, self.phone, self.department,
                datetime.now(), self.id
            ))
            return True
        except Exception as e:
            print(f"Update profile error: {e}")
            return False
    
    def change_password(self, old_password, new_password):
        """Change user password"""
        try:
            old_hashed = self.hash_password(old_password)
            new_hashed = self.hash_password(new_password)
            
            # Verify old password
            query = 'SELECT password FROM users WHERE id = ?'
            results = self.db.execute_query(query, (self.id,))
            
            if results and results[0][0] == old_hashed:
                update_query = 'UPDATE users SET password = ? WHERE id = ?'
                self.db.execute_update(update_query, (new_hashed, self.id))
                return True
            return False
        except Exception as e:
            print(f"Change password error: {e}")
            return False
    
    def deactivate(self):
        """Deactivate user account"""
        try:
            query = 'UPDATE users SET status = 0 WHERE id = ?'
            self.db.execute_update(query, (self.id,))
            self.status = 0
            return True
        except Exception as e:
            print(f"Deactivate error: {e}")
            return False
    
    @staticmethod
    def username_exists(username):
        """Check if username already exists"""
        try:
            db = DatabaseManager()
            query = 'SELECT id FROM users WHERE username = ?'
            results = db.execute_query(query, (username,))
            return len(results) > 0
        except Exception as e:
            print(f"Username check error: {e}")
            return False
    
    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        try:
            db = DatabaseManager()
            query = 'SELECT id FROM users WHERE email = ?'
            results = db.execute_query(query, (email,))
            return len(results) > 0
        except Exception as e:
            print(f"Email check error: {e}")
            return False
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
