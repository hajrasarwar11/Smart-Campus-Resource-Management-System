"""
Booking Model Module
"""

from datetime import datetime
from database.db_setup import DatabaseManager

class Booking:
    def __init__(self, user_id=None, classroom_id=None, course_name=None,
                 booking_date=None, start_time=None, end_time=None,
                 description=None, status=2):
        self.id = None
        self.user_id = user_id
        self.classroom_id = classroom_id
        self.course_name = course_name
        self.booking_date = booking_date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.status = status  # 0=Cancelled, 1=Approved, 2=Pending, 3=Rejected
        self.created_by = None
        self.cancelled_by = None
        self.created_at = None
        self.db = DatabaseManager()
    
    def create(self, created_by=None):
        """Create a new booking"""
        try:
            query = '''
                INSERT INTO bookings 
                (user_id, classroom_id, course_name, booking_date, 
                 start_time, end_time, description, status, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.id = self.db.execute_update(query, (
                self.user_id, self.classroom_id, self.course_name,
                self.booking_date, self.start_time, self.end_time,
                self.description, self.status, created_by
            ))
            return self.id is not None
        except Exception as e:
            print(f"Create booking error: {e}")
            return False
    
    @staticmethod
    def get_booking_by_id(booking_id):
        """Get booking by ID"""
        try:
            db = DatabaseManager()
            query = 'SELECT * FROM bookings WHERE id = ?'
            results = db.execute_query(query, (booking_id,))
            
            if results:
                row = results[0]
                booking = Booking(
                    user_id=row[1],
                    classroom_id=row[2],
                    course_name=row[3],
                    booking_date=row[4],
                    start_time=row[5],
                    end_time=row[6],
                    description=row[8],
                    status=row[7]
                )
                booking.id = row[0]
                booking.created_by = row[9]
                booking.cancelled_by = row[10]
                booking.created_at = row[12]
                return booking
            return None
        except Exception as e:
            print(f"Get booking error: {e}")
            return None
    
    @staticmethod
    def get_user_bookings(user_id, status=None):
        """Get all bookings for a user"""
        try:
            db = DatabaseManager()
            if status is not None:
                query = '''
                    SELECT * FROM bookings 
                    WHERE user_id = ? AND status = ?
                    ORDER BY booking_date DESC, start_time DESC
                '''
                results = db.execute_query(query, (user_id, status))
            else:
                query = '''
                    SELECT * FROM bookings 
                    WHERE user_id = ?
                    ORDER BY booking_date DESC, start_time DESC
                '''
                results = db.execute_query(query, (user_id,))
            
            bookings = []
            if results:
                for row in results:
                    booking = Booking(
                        user_id=row[1],
                        classroom_id=row[2],
                        course_name=row[3],
                        booking_date=row[4],
                        start_time=row[5],
                        end_time=row[6],
                        description=row[8],
                        status=row[7]
                    )
                    booking.id = row[0]
                    booking.created_by = row[9]
                    booking.created_at = row[12]
                    bookings.append(booking)
            return bookings
        except Exception as e:
            print(f"Get user bookings error: {e}")
            return []
    
    @staticmethod
    def get_all_bookings(status=None):
        """Get all bookings in the system"""
        try:
            db = DatabaseManager()
            if status is not None:
                query = '''
                    SELECT * FROM bookings 
                    WHERE status = ?
                    ORDER BY booking_date DESC
                '''
                results = db.execute_query(query, (status,))
            else:
                query = 'SELECT * FROM bookings ORDER BY booking_date DESC'
                results = db.execute_query(query)
            
            bookings = []
            if results:
                for row in results:
                    booking = Booking(
                        user_id=row[1],
                        classroom_id=row[2],
                        course_name=row[3],
                        booking_date=row[4],
                        start_time=row[5],
                        end_time=row[6],
                        description=row[8],
                        status=row[7]
                    )
                    booking.id = row[0]
                    booking.created_by = row[9]
                    booking.created_at = row[12]
                    bookings.append(booking)
            return bookings
        except Exception as e:
            print(f"Get all bookings error: {e}")
            return []
    
    def approve(self, approved_by):
        """Approve a booking"""
        try:
            query = 'UPDATE bookings SET status = 1, updated_at = ? WHERE id = ?'
            self.db.execute_update(query, (datetime.now(), self.id))
            self.status = 1
            return True
        except Exception as e:
            print(f"Approve booking error: {e}")
            return False
    
    def reject(self, rejected_by, reason):
        """Reject a booking"""
        try:
            query = '''
                UPDATE bookings 
                SET status = 3, reason = ?, updated_at = ?
                WHERE id = ?
            '''
            self.db.execute_update(query, (reason, datetime.now(), self.id))
            self.status = 3
            return True
        except Exception as e:
            print(f"Reject booking error: {e}")
            return False
    
    def cancel(self, cancelled_by, reason):
        """Cancel a booking"""
        try:
            query = '''
                UPDATE bookings 
                SET status = 0, cancelled_by = ?, reason = ?, updated_at = ?
                WHERE id = ?
            '''
            self.db.execute_update(query, (cancelled_by, reason, datetime.now(), self.id))
            self.status = 0
            return True
        except Exception as e:
            print(f"Cancel booking error: {e}")
            return False
    
    @staticmethod
    def check_conflict(classroom_id, booking_date, start_time, end_time, booking_id=None):
        """Check for booking conflicts"""
        try:
            db = DatabaseManager()
            if booking_id:
                query = '''
                    SELECT COUNT(*) as count FROM bookings
                    WHERE classroom_id = ? AND booking_date = ?
                    AND status IN (1, 2) AND id != ?
                    AND (
                        (start_time <= ? AND end_time > ?)
                        OR (start_time < ? AND end_time >= ?)
                        OR (start_time >= ? AND end_time <= ?)
                    )
                '''
                results = db.execute_query(query, (
                    classroom_id, booking_date, booking_id,
                    start_time, start_time, end_time, end_time, start_time, end_time
                ))
            else:
                query = '''
                    SELECT COUNT(*) as count FROM bookings
                    WHERE classroom_id = ? AND booking_date = ?
                    AND status IN (1, 2)
                    AND (
                        (start_time <= ? AND end_time > ?)
                        OR (start_time < ? AND end_time >= ?)
                        OR (start_time >= ? AND end_time <= ?)
                    )
                '''
                results = db.execute_query(query, (
                    classroom_id, booking_date,
                    start_time, start_time, end_time, end_time, start_time, end_time
                ))
            
            return results[0][0] > 0 if results else False
        except Exception as e:
            print(f"Check conflict error: {e}")
            return False
    
    def __repr__(self):
        return f"<Booking(id={self.id}, user={self.user_id}, room={self.classroom_id})>"
