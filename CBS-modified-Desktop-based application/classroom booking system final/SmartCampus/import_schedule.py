"""
Import Schedule Data for FJWU Department of Software Engineering
Semester Fall 2025 - 5th Semester Section A
"""

from database.db_setup import DatabaseManager
from models.user import User
from models.classroom import Classroom
from models.schedule import Schedule
import sys
import io

# Fix for Unicode printing on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def import_classrooms():
    """Import all classroom data"""
    classrooms_data = [
        {'room_number': 'S-2', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 40},
        {'room_number': 'S-3', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 40},
        {'room_number': 'S-5', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 40},
        {'room_number': 'S-6', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 40},
        {'room_number': 'S-7', 'room_type': 'Lab', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 30},
        {'room_number': 'S-8', 'room_type': 'Lab', 'building': 'Software Engineering Block', 'floor': 1, 'capacity': 30},
        {'room_number': 'S-27b', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 2, 'capacity': 40},
        {'room_number': 'S-37b', 'room_type': 'Theory', 'building': 'Software Engineering Block', 'floor': 3, 'capacity': 40},
        {'room_number': 'C-8', 'room_type': 'Lab', 'building': 'Computer Science Block', 'floor': 1, 'capacity': 30},
    ]
    
    db = DatabaseManager()
    for classroom in classrooms_data:
        try:
            # Check if classroom already exists
            result = db.execute_query('SELECT id FROM classrooms WHERE room_number = ?', (classroom['room_number'],))
            if not result:
                new_classroom = Classroom(
                    room_number=classroom['room_number'],
                    room_type=classroom['room_type'],
                    building=classroom['building'],
                    floor=classroom['floor'],
                    capacity=classroom['capacity']
                )
                new_classroom.create()
                print(f"✓ Added classroom: {classroom['room_number']}")
        except Exception as e:
            print(f"✗ Error adding classroom {classroom['room_number']}: {e}")

def import_teachers():
    """Import all teacher data"""
    teachers_data = [
        {'username': 'dr_sobia', 'fullname': 'Dr. Sobia Khalid', 'email': 'sobia.khalid@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111111', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_irum', 'fullname': 'Dr. Irum Matloob', 'email': 'irum.matloob@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111112', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_sidra', 'fullname': 'Dr. Sidra Ejaz', 'email': 'sidra.ejaz@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111113', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_mehreen', 'fullname': 'Dr. Mehreen Sirshar', 'email': 'mehreen.sirshar@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111114', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_aliya', 'fullname': 'Dr. Aliya Ashraf Khan', 'email': 'aliya.khan@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111115', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_bushra', 'fullname': 'Dr. Bushra Bashir', 'email': 'bushra.bashir@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111116', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_saria', 'fullname': 'Dr. Saria Safdar', 'email': 'saria.safdar@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111117', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_mukhtar', 'fullname': 'Dr. Mukhtiar Bano', 'email': 'mukhtar.bano@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111118', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'engr_shahzad', 'fullname': 'Engr. Muhammad Shahzad', 'email': 'shahzad@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111119', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'engr_rehan', 'fullname': 'Engr. Rehan Ahmed', 'email': 'rehan.ahmed@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111120', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'engr_ahsen', 'fullname': 'Engr. Ahsen Ilyas', 'email': 'ahsen.ilyas@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111121', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'dr_aamir', 'fullname': 'Dr. Aamir Arsalan', 'email': 'aamir.arsalan@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111122', 'role': 2, 'department': 'Software Engineering'},
        {'username': 'engr_waqas', 'fullname': 'Engr. Waqas Salim', 'email': 'waqas.salim@fjwu.edu.pk', 'password': 'password123', 'phone': '0300-1111123', 'role': 2, 'department': 'Software Engineering'},
    ]
    
    db = DatabaseManager()
    for teacher in teachers_data:
        try:
            # Check if teacher already exists
            result = db.execute_query('SELECT id FROM users WHERE username = ?', (teacher['username'],))
            if not result:
                new_teacher = User(
                    username=teacher['username'],
                    fullname=teacher['fullname'],
                    email=teacher['email'],
                    password=teacher['password'],
                    phone=teacher['phone'],
                    role=teacher['role'],
                    department=teacher['department']
                )
                new_teacher.register()
                print(f"✓ Added teacher: {teacher['fullname']}")
        except Exception as e:
            print(f"✗ Error adding teacher {teacher['fullname']}: {e}")

def get_teacher_id(fullname):
    """Get teacher ID by full name"""
    db = DatabaseManager()
    result = db.execute_query('SELECT id FROM users WHERE fullname = ? AND role = 2', (fullname,))
    return result[0][0] if result else None

def get_classroom_id(room_number):
    """Get classroom ID by room number"""
    db = DatabaseManager()
    result = db.execute_query('SELECT id FROM classrooms WHERE room_number = ?', (room_number,))
    return result[0][0] if result else None

def import_schedules():
    """Import all schedule data from the timetables"""
    schedules_data = [
        # Monday
        {'teacher': 'Dr. Sobia Khalid', 'classroom': 'S-2', 'course': 'DS-703 Machine Learning MSDS-I', 'day': 'Monday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Irum Matloob', 'classroom': 'S-2', 'course': 'DS-703 Machine Learning MSDS-I', 'day': 'Monday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Sobia Khalid', 'classroom': 'S-3', 'course': 'SE-613 Data Structures and Algorithm BSE-IIIB', 'day': 'Monday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Sobia Khalid', 'classroom': 'S-3', 'course': 'SE-613 Data Structures and Algorithm BSE-IIIA', 'day': 'Monday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Engr. Muhammad Shahzad', 'classroom': 'S-3', 'course': 'SE-615Lab Operating Systems Lab BSE-IIIB', 'day': 'Monday', 'start': '01:00', 'end': '02:30'},
        {'teacher': 'Dr. Aliya Ashraf Khan', 'classroom': 'S-7', 'course': 'NS-637 Exploring Quantitative Skills BSE-IA', 'day': 'Monday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-6', 'course': 'SE-615 Operating Systems BSE-IIIB', 'day': 'Monday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-7', 'course': 'SE-615 Operating Systems BSE-IIIB', 'day': 'Monday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-7', 'course': 'SE-618 Introduction to Info & Communication Technologies BSE-IA', 'day': 'Monday', 'start': '01:00', 'end': '02:30'},
        
        # Tuesday
        {'teacher': 'Dr. Bushra Bashir', 'classroom': 'S-3', 'course': 'SE-611 Programming Fundamentals BSE-IA', 'day': 'Tuesday', 'start': '08:00', 'end': '09:30'},
        {'teacher': 'Dr. Mukhtiar Bano', 'classroom': 'S-3', 'course': 'BSE-620 Formal Methods in Software Engineering BSE-VIIA', 'day': 'Tuesday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Engr. Ahsen Ilyas', 'classroom': 'S-2', 'course': 'SE-618LAB Introduction to Info & Communication Technologies Lab BSE-IB', 'day': 'Tuesday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Engr. Ahsen Ilyas', 'classroom': 'S-2', 'course': 'NS-616Lab Applied Physics Lab BSE-IB', 'day': 'Tuesday', 'start': '01:00', 'end': '02:30'},
        {'teacher': 'Dr. Bushra Bashir', 'classroom': 'S-8', 'course': 'SE-611 Programming Fundamentals BSE-IA', 'day': 'Tuesday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Sidra Ejaz', 'classroom': 'S-8', 'course': 'SE-618 Introduction to Info & Communication Technologies BSE-IB', 'day': 'Tuesday', 'start': '11:30', 'end': '01:00'},
        
        # Wednesday
        {'teacher': 'Dr. Aamir Arsalan', 'classroom': 'S-2', 'course': 'DS-701 Tools and Techniques of Data Science MSDS-I', 'day': 'Wednesday', 'start': '08:00', 'end': '09:30'},
        {'teacher': 'Dr. Aamir Arsalan', 'classroom': 'S-2', 'course': 'DS-701 Tools and Techniques of Data Science MSDS-I', 'day': 'Wednesday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Sobia Khalid', 'classroom': 'S-2', 'course': 'DS-757 Data Science Programming MSDS-I', 'day': 'Wednesday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Mukhtiar Bano', 'classroom': 'S-3', 'course': 'BSE-620 Formal Methods in Software Engineering BSE-VIIB', 'day': 'Wednesday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Sidra Ejaz', 'classroom': 'S-3', 'course': 'SE-666 Designing and Analysis of Algorithms BSE-VB', 'day': 'Wednesday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-6', 'course': 'DS-713 Deep Learning MSDS-III', 'day': 'Wednesday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Aliya Ashraf Khan', 'classroom': 'S-6', 'course': 'DS-754 AI for Healthcare MSDS-III', 'day': 'Wednesday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-7', 'course': 'SE-613Lab Data Structures and Algorithm Lab BSE-IIIA', 'day': 'Wednesday', 'start': '11:30', 'end': '01:00'},
        
        # Thursday
        {'teacher': 'Dr. Saria Safdar', 'classroom': 'S-6', 'course': 'Dr. Saria Safdar', 'day': 'Thursday', 'start': '08:00', 'end': '09:30'},
        {'teacher': 'Dr. Mehreen Sirshar', 'classroom': 'S-6', 'course': 'DS-713 Deep Learning MSDS-III', 'day': 'Thursday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Aliya Ashraf Khan', 'classroom': 'S-6', 'course': 'DS-754 AI for Healthcare MSDS-III', 'day': 'Thursday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Engr. Rehan Ahmed', 'classroom': 'S-7', 'course': 'SE-613Lab Data Structures and Algorithm Lab BSE-IIIB', 'day': 'Thursday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Bushra Bashir', 'classroom': 'S-3', 'course': 'SE-658Lab Software Construction & Development Lab BSE-VB', 'day': 'Thursday', 'start': '11:30', 'end': '01:00'},
        
        # Friday
        {'teacher': 'Dr. Irum Matloob', 'classroom': 'S-2', 'course': 'Dr. Irum Matloob', 'day': 'Friday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Mukhtiar Bano', 'classroom': 'S-3', 'course': 'SE-658 Software Construction & Development BSE-VA', 'day': 'Friday', 'start': '09:30', 'end': '11:00'},
        {'teacher': 'Dr. Mukhtiar Bano', 'classroom': 'S-3', 'course': 'SE-658 Software Construction & Development BSE-VB', 'day': 'Friday', 'start': '01:00', 'end': '02:30'},
        {'teacher': 'Engr. Waqas Salim', 'classroom': 'S-6', 'course': 'SE-665 Cloud Computing BSE-VA', 'day': 'Friday', 'start': '08:00', 'end': '10:00'},
        {'teacher': 'Dr. Irum Matloob', 'classroom': 'S-6', 'course': 'SE-CD-631 Artificial Intelligence BSE-VA', 'day': 'Friday', 'start': '10:00', 'end': '11:30'},
        {'teacher': 'Dr. Bushra Bashir', 'classroom': 'S-7', 'course': 'SE-611Lab Programming Fundamentals Lab BSE-IA', 'day': 'Friday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Bushra Bashir', 'classroom': 'S-8', 'course': 'BSE-702 Internet of Things (IoT) BSE-VIIA', 'day': 'Friday', 'start': '11:30', 'end': '01:00'},
        {'teacher': 'Dr. Aliya Ashraf Khan', 'classroom': 'S-8', 'course': 'NS-637 Exploring Quantitative Skills BSE-IA', 'day': 'Friday', 'start': '11:30', 'end': '01:00'},
    ]
    
    db = DatabaseManager()
    added_count = 0
    skipped_count = 0
    
    for schedule in schedules_data:
        try:
            teacher_id = get_teacher_id(schedule['teacher'])
            classroom_id = get_classroom_id(schedule['classroom'])
            
            if teacher_id and classroom_id:
                # Check if schedule already exists
                result = db.execute_query(
                    'SELECT id FROM schedules WHERE teacher_id = ? AND classroom_id = ? AND course_name = ? AND day_of_week = ?',
                    (teacher_id, classroom_id, schedule['course'], schedule['day'])
                )
                
                if not result:
                    new_schedule = Schedule(
                        teacher_id=teacher_id,
                        classroom_id=classroom_id,
                        course_name=schedule['course'],
                        day_of_week=schedule['day'],
                        start_time=schedule['start'],
                        end_time=schedule['end'],
                        semester='Fall 2025'
                    )
                    if new_schedule.create():
                        added_count += 1
                        print(f"✓ Added schedule: {schedule['course']} - {schedule['day']} {schedule['start']}-{schedule['end']} in {schedule['classroom']}")
                else:
                    skipped_count += 1
            else:
                print(f"✗ Skipped schedule: Teacher '{schedule['teacher']}' or Classroom '{schedule['classroom']}' not found")
                skipped_count += 1
        except Exception as e:
            print(f"✗ Error adding schedule: {e}")
    
    print(f"\n✓ Total schedules added: {added_count}")
    print(f"⊘ Total schedules skipped: {skipped_count}")

def main():
    """Main import function"""
    print("=" * 60)
    print("FJWU Schedule Data Import - Semester Fall 2025")
    print("=" * 60)
    
    print("\n[1/3] Importing classrooms...")
    import_classrooms()
    
    print("\n[2/3] Importing teachers...")
    import_teachers()
    
    print("\n[3/3] Importing schedules...")
    import_schedules()
    
    print("\n" + "=" * 60)
    print("Import completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
