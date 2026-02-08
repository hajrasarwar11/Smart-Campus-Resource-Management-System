"""
Schedule Model Module
"""

from datetime import datetime
from database.db_setup import DatabaseManager

class Schedule:
    def __init__(self, teacher_id=None, classroom_id=None, course_name=None,
                 day_of_week=None, start_time=None, end_time=None,
                 semester=None, status=1):
        self.id = None
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id
        self.course_name = course_name
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.semester = semester
        self.status = status
        self.created_at = None
        self.db = DatabaseManager()
    
    def create(self):
        """Create a new schedule"""
        try:
            query = '''
                INSERT INTO schedules 
                (teacher_id, classroom_id, course_name, day_of_week,
                 start_time, end_time, semester, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.id = self.db.execute_update(query, (
                self.teacher_id, self.classroom_id, self.course_name,
                self.day_of_week, self.start_time, self.end_time,
                self.semester, self.status
            ))
            return self.id is not None
        except Exception as e:
            print(f"Create schedule error: {e}")
            return False
    
    @staticmethod
    def get_schedule_by_id(schedule_id):
        """Get schedule by ID"""
        try:
            db = DatabaseManager()
            query = 'SELECT * FROM schedules WHERE id = ?'
            results = db.execute_query(query, (schedule_id,))
            
            if results:
                row = results[0]
                schedule = Schedule(
                    teacher_id=row[1],
                    classroom_id=row[2],
                    course_name=row[3],
                    day_of_week=row[4],
                    start_time=row[5],
                    end_time=row[6],
                    semester=row[7],
                    status=row[8]
                )
                schedule.id = row[0]
                schedule.created_at = row[9]
                return schedule
            return None
        except Exception as e:
            print(f"Get schedule error: {e}")
            return None
    
    @staticmethod
    def get_teacher_schedules(teacher_id):
        """Get all schedules for a teacher"""
        try:
            db = DatabaseManager()
            query = '''
                SELECT * FROM schedules 
                WHERE teacher_id = ? AND status = 1
                ORDER BY day_of_week, start_time
            '''
            results = db.execute_query(query, (teacher_id,))
            
            schedules = []
            if results:
                for row in results:
                    schedule = Schedule(
                        teacher_id=row[1],
                        classroom_id=row[2],
                        course_name=row[3],
                        day_of_week=row[4],
                        start_time=row[5],
                        end_time=row[6],
                        semester=row[7],
                        status=row[8]
                    )
                    schedule.id = row[0]
                    schedules.append(schedule)
            return schedules
        except Exception as e:
            print(f"Get teacher schedules error: {e}")
            return []
    
    @staticmethod
    def get_classroom_schedules(classroom_id):
        """Get all schedules for a classroom"""
        try:
            db = DatabaseManager()
            query = '''
                SELECT * FROM schedules 
                WHERE classroom_id = ? AND status = 1
                ORDER BY day_of_week, start_time
            '''
            results = db.execute_query(query, (classroom_id,))
            
            schedules = []
            if results:
                for row in results:
                    schedule = Schedule(
                        teacher_id=row[1],
                        classroom_id=row[2],
                        course_name=row[3],
                        day_of_week=row[4],
                        start_time=row[5],
                        end_time=row[6],
                        semester=row[7],
                        status=row[8]
                    )
                    schedule.id = row[0]
                    schedules.append(schedule)
            return schedules
        except Exception as e:
            print(f"Get classroom schedules error: {e}")
            return []
    
    @staticmethod
    def get_all_schedules():
        """Get all schedules"""
        try:
            db = DatabaseManager()
            query = 'SELECT * FROM schedules WHERE status = 1 ORDER BY day_of_week, start_time'
            results = db.execute_query(query)
            
            schedules = []
            if results:
                for row in results:
                    schedule = Schedule(
                        teacher_id=row[1],
                        classroom_id=row[2],
                        course_name=row[3],
                        day_of_week=row[4],
                        start_time=row[5],
                        end_time=row[6],
                        semester=row[7],
                        status=row[8]
                    )
                    schedule.id = row[0]
                    schedules.append(schedule)
            return schedules
        except Exception as e:
            print(f"Get all schedules error: {e}")
            return []
    
    def update(self):
        """Update schedule"""
        try:
            query = '''
                UPDATE schedules 
                SET teacher_id = ?, classroom_id = ?, course_name = ?,
                    day_of_week = ?, start_time = ?, end_time = ?, semester = ?
                WHERE id = ?
            '''
            self.db.execute_update(query, (
                self.teacher_id, self.classroom_id, self.course_name,
                self.day_of_week, self.start_time, self.end_time,
                self.semester, self.id
            ))
            return True
        except Exception as e:
            print(f"Update schedule error: {e}")
            return False
    
    def delete(self):
        """Delete/deactivate schedule"""
        try:
            query = 'UPDATE schedules SET status = 0 WHERE id = ?'
            self.db.execute_update(query, (self.id,))
            self.status = 0
            return True
        except Exception as e:
            print(f"Delete schedule error: {e}")
            return False
    
    @staticmethod
    def check_conflict(teacher_id, classroom_id, day_of_week, start_time, end_time, schedule_id=None):
        """Check for schedule conflicts"""
        try:
            db = DatabaseManager()
            if schedule_id:
                query = '''
                    SELECT COUNT(*) as count FROM schedules
                    WHERE (teacher_id = ? OR classroom_id = ?)
                    AND day_of_week = ? AND status = 1 AND id != ?
                    AND (
                        (start_time <= ? AND end_time > ?)
                        OR (start_time < ? AND end_time >= ?)
                        OR (start_time >= ? AND end_time <= ?)
                    )
                '''
                results = db.execute_query(query, (
                    teacher_id, classroom_id, day_of_week, schedule_id,
                    start_time, start_time, end_time, end_time, start_time, end_time
                ))
            else:
                query = '''
                    SELECT COUNT(*) as count FROM schedules
                    WHERE (teacher_id = ? OR classroom_id = ?)
                    AND day_of_week = ? AND status = 1
                    AND (
                        (start_time <= ? AND end_time > ?)
                        OR (start_time < ? AND end_time >= ?)
                        OR (start_time >= ? AND end_time <= ?)
                    )
                '''
                results = db.execute_query(query, (
                    teacher_id, classroom_id, day_of_week,
                    start_time, start_time, end_time, end_time, start_time, end_time
                ))
            
            return results[0][0] > 0 if results else False
        except Exception as e:
            print(f"Check conflict error: {e}")
            return False
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, teacher={self.teacher_id}, course={self.course_name})>"
