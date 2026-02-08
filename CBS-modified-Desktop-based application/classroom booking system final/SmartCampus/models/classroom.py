"""
Classroom Model Module
"""

from datetime import datetime
from database.db_setup import DatabaseManager

class Classroom:
    def __init__(self, room_number=None, room_type=None, capacity=None, 
                 building=None, floor=None, description=None, status=1):
        self.id = None
        self.room_number = room_number
        self.room_type = room_type
        self.capacity = capacity
        self.building = building
        self.floor = floor
        self.description = description
        self.status = status
        self.db = DatabaseManager()
    
    def create(self):
        """Create a new classroom"""
        try:
            query = '''
                INSERT INTO classrooms 
                (room_number, room_type, capacity, building, floor, description, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            self.id = self.db.execute_update(query, (
                self.room_number, self.room_type, self.capacity,
                self.building, self.floor, self.description, self.status
            ))
            return self.id is not None
        except Exception as e:
            print(f"Create classroom error: {e}")
            return False
    
    @staticmethod
    def get_classroom_by_id(classroom_id):
        """Get classroom by ID"""
        try:
            db = DatabaseManager()
            query = 'SELECT * FROM classrooms WHERE id = ?'
            results = db.execute_query(query, (classroom_id,))
            
            if results:
                row = results[0]
                classroom = Classroom(
                    room_number=row[1],
                    room_type=row[2],
                    capacity=row[3],
                    building=row[4],
                    floor=row[5],
                    description=row[6],
                    status=row[7]
                )
                classroom.id = row[0]
                return classroom
            return None
        except Exception as e:
            print(f"Get classroom error: {e}")
            return None
    
    @staticmethod
    def get_all_classrooms(room_type=None, status=1):
        """Get all classrooms or filtered by type"""
        try:
            db = DatabaseManager()
            if room_type:
                query = '''
                    SELECT * FROM classrooms 
                    WHERE room_type = ? AND status = ?
                    ORDER BY room_number
                '''
                results = db.execute_query(query, (room_type, status))
            else:
                query = '''
                    SELECT * FROM classrooms 
                    WHERE status = ?
                    ORDER BY building, room_number
                '''
                results = db.execute_query(query, (status,))
            
            classrooms = []
            if results:
                for row in results:
                    classroom = Classroom(
                        room_number=row[1],
                        room_type=row[2],
                        capacity=row[3],
                        building=row[4],
                        floor=row[5],
                        description=row[6],
                        status=row[7]
                    )
                    classroom.id = row[0]
                    classrooms.append(classroom)
            return classrooms
        except Exception as e:
            print(f"Get all classrooms error: {e}")
            return []
    
    def update(self):
        """Update classroom details"""
        try:
            query = '''
                UPDATE classrooms 
                SET room_number = ?, room_type = ?, capacity = ?, 
                    building = ?, floor = ?, description = ?
                WHERE id = ?
            '''
            self.db.execute_update(query, (
                self.room_number, self.room_type, self.capacity,
                self.building, self.floor, self.description, self.id
            ))
            return True
        except Exception as e:
            print(f"Update classroom error: {e}")
            return False
    
    def deactivate(self):
        """Deactivate classroom"""
        try:
            query = 'UPDATE classrooms SET status = 0 WHERE id = ?'
            self.db.execute_update(query, (self.id,))
            self.status = 0
            return True
        except Exception as e:
            print(f"Deactivate classroom error: {e}")
            return False
    
    @staticmethod
    def get_available_classrooms(room_type, booking_date, start_time, end_time):
        """Get available classrooms for a specific time slot"""
        try:
            db = DatabaseManager()
            query = '''
                SELECT DISTINCT c.* FROM classrooms c
                WHERE c.room_type = ? AND c.status = 1
                AND c.id NOT IN (
                    SELECT classroom_id FROM bookings
                    WHERE booking_date = ? 
                    AND status IN (1, 2)
                    AND (
                        (start_time <= ? AND end_time > ?)
                        OR (start_time < ? AND end_time >= ?)
                        OR (start_time >= ? AND end_time <= ?)
                    )
                )
                ORDER BY c.room_number
            '''
            results = db.execute_query(query, (
                room_type, booking_date, start_time, start_time,
                end_time, end_time, start_time, end_time
            ))
            
            classrooms = []
            if results:
                for row in results:
                    classroom = Classroom(
                        room_number=row[1],
                        room_type=row[2],
                        capacity=row[3],
                        building=row[4],
                        floor=row[5],
                        description=row[6],
                        status=row[7]
                    )
                    classroom.id = row[0]
                    classrooms.append(classroom)
            return classrooms
        except Exception as e:
            print(f"Get available classrooms error: {e}")
            return []
    
    def __repr__(self):
        return f"<Classroom(id={self.id}, room={self.room_number}, type={self.room_type})>"
