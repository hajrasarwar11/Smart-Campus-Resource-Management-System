# Smart Campus - Complete File Listing

## Project Directory Structure

```
d:\XAMPP\Files\htdocs\Project\classroom booking system final\SmartCampus\
│
├── 📄 main.py                          [Application Entry Point]
│   └── Launches the PyQt5 application with login dialog
│
├── 📄 config.py                        [Configuration Settings]
│   └── All app settings, colors, fonts, constants
│
├── 📄 requirements.txt                 [Dependencies]
│   └── PyQt5, matplotlib, numpy, python-dateutil
│
├── 📚 Documentation Files
│   ├── 📄 README.md                    [Project Overview]
│   │   └── Features, installation, usage, API docs
│   │
│   ├── 📄 USER_MANUAL.md               [User Guide]
│   │   └── Admin, student, teacher guides with examples
│   │
│   ├── 📄 INSTALLATION.md              [Setup Instructions]
│   │   └── Step-by-step installation for Windows/Mac/Linux
│   │
│   ├── 📄 DEPLOYMENT.md                [Deployment Guide]
│   │   └── Production deployment, Docker, executables
│   │
│   └── 📄 PROJECT_SUMMARY.md           [Completion Report]
│       └── All features completed, checklist, statistics
│
├── 📁 database/
│   ├── 📄 __init__.py
│   └── 📄 db_setup.py                  [Database Manager]
│       ├── SQLite database initialization
│       ├── 8 tables with relationships
│       ├── Default data seeding
│       ├── Backup functionality
│       └── Connection management
│
├── 📁 models/
│   ├── 📄 __init__.py
│   ├── 📄 user.py                      [User Model]
│   │   ├── Authentication (login/register)
│   │   ├── Password management
│   │   ├── Profile operations
│   │   ├── Role-based access
│   │   └── User CRUD operations
│   │
│   ├── 📄 classroom.py                 [Classroom Model]
│   │   ├── Add/edit/delete classrooms
│   │   ├── Availability checking
│   │   ├── Conflict detection
│   │   └── Equipment management
│   │
│   ├── 📄 booking.py                   [Booking Model]
│   │   ├── Create bookings
│   │   ├── Approve/reject workflow
│   │   ├── Cancellation
│   │   ├── Conflict detection
│   │   └── Status tracking
│   │
│   └── 📄 schedule.py                  [Schedule Model]
│       ├── Create schedules
│       ├── Manage recurring schedules
│       ├── Conflict detection
│       ├── Teacher schedules
│       └── Classroom schedules
│
├── 📁 gui/
│   ├── 📄 __init__.py
│   ├── 📄 styles.py                    [Modern Stylesheet]
│   │   ├── Color scheme (#2563EB blue)
│   │   ├── Button styles
│   │   ├── Form styling
│   │   ├── Table styling
│   │   ├── Menu styling
│   │   └── Responsive design
│   │
│   ├── 📄 login_window.py              [Login Interface]
│   │   ├── Professional login form
│   │   ├── Sign-up link
│   │   ├── Input validation
│   │   ├── Remember me checkbox
│   │   └── Error handling
│   │
│   ├── 📄 signup_window.py             [Registration Dialog]
│   │   ├── User registration form
│   │   ├── Field validation
│   │   ├── Email uniqueness check
│   │   ├── Username uniqueness check
│   │   ├── Department selection
│   │   └── Role selection
│   │
│   ├── 📄 admin_dashboard.py           [Admin Interface]
│   │   ├── Dashboard with statistics
│   │   ├── User management tab
│   │   ├── Classroom management tab
│   │   ├── Booking management tab
│   │   ├── Schedule management tab
│   │   ├── Reports tab
│   │   ├── Menu bar
│   │   ├── Data tables
│   │   ├── Quick action buttons
│   │   └── Stat cards
│   │
│   └── 📄 user_dashboard.py            [Student/Teacher Interface]
│       ├── Dashboard overview
│       ├── My Bookings tab
│       ├── Available Rooms tab
│       ├── My Schedules tab (teachers)
│       ├── Profile tab
│       ├── Booking dialog
│       ├── Search functionality
│       ├── Status tracking
│       └── Menu bar
│
├── 📁 utils/
│   ├── 📄 __init__.py
│   ├── 📄 validation.py                [Validation Module]
│   │   ├── Username validation
│   │   ├── Email validation
│   │   ├── Password strength
│   │   ├── Phone validation
│   │   ├── Date/time validation
│   │   ├── Room capacity validation
│   │   ├── Time range validation
│   │   ├── FormValidator class
│   │   ├── Input sanitization
│   │   └── Comprehensive form validation
│   │
│   └── 📄 helpers.py                   [Helper Utilities]
│       ├── DateTimeHelper
│       │   └── Date/time operations
│       ├── StringHelper
│       │   └── String manipulation
│       ├── NumberHelper
│       │   └── Number formatting
│       ├── ListHelper
│       │   └── List operations
│       ├── FileHelper
│       │   └── File operations
│       ├── ValidationHelper
│       │   └── Additional validation
│       ├── CryptographyHelper
│       │   └── Hashing functions
│       ├── NotificationHelper
│       │   └── Notification formatting
│       ├── LoggerHelper
│       │   └── Activity logging
│       └── CacheHelper
│           └── In-memory caching
│
├── 📁 reports/
│   ├── 📄 __init__.py
│   └── 📄 usage_report.py              [Report Generator]
│       ├── Booking statistics
│       ├── Resource usage analysis
│       ├── Peak hours identification
│       ├── Underutilized rooms report
│       ├── Text file export
│       ├── Matplotlib charts
│       ├── PDF export
│       └── CSV export
│
├── 📁 assets/
│   └── (Directory for icons and resources)
│
├── 📄 __init__.py
│
└── 📄 smartcampus.db                   [SQLite Database]
    (Created automatically on first run)
```

## File Count Summary

- **Python Files**: 18
- **Documentation Files**: 5
- **Configuration Files**: 1
- **Data Files**: 1 (database, created at runtime)
- **Total**: 25 files

## Code Statistics

### Models Layer
- `user.py`: ~200 lines (User model with auth)
- `classroom.py`: ~150 lines (Classroom management)
- `booking.py`: ~200 lines (Booking system)
- `schedule.py`: ~200 lines (Schedule management)
- **Total**: ~750 lines

### GUI Layer
- `styles.py`: ~300 lines (Modern stylesheet)
- `login_window.py`: ~150 lines (Login UI)
- `signup_window.py`: ~150 lines (Registration UI)
- `admin_dashboard.py`: ~600 lines (Admin interface)
- `user_dashboard.py`: ~700 lines (User interface)
- **Total**: ~1,900 lines

### Utilities Layer
- `validation.py`: ~300 lines (Validation module)
- `helpers.py`: ~400 lines (Helper functions)
- **Total**: ~700 lines

### Database Layer
- `db_setup.py`: ~250 lines (Database management)
- **Total**: ~250 lines

### Core Files
- `config.py`: ~150 lines (Configuration)
- `main.py`: ~50 lines (Entry point)
- **Total**: ~200 lines

### Reports
- `usage_report.py`: ~200 lines (Report generation)
- **Total**: ~200 lines

### Grand Total: ~3,800+ lines of code

## Database Tables

1. **users** - User accounts and authentication
   - id, username, fullname, email, password, phone, role, status, department, created_at

2. **departments** - Institution departments
   - id, name, code, description, created_at

3. **classrooms** - Room information
   - id, room_number, room_type, capacity, building, floor, description, status

4. **equipment** - Resource inventory
   - id, name, equipment_type, quantity, classroom_id, description, status

5. **bookings** - Room reservations
   - id, user_id, classroom_id, course_name, booking_date, start_time, end_time, status, description, created_by, cancelled_by, reason

6. **schedules** - Class timetables
   - id, teacher_id, classroom_id, course_name, day_of_week, start_time, end_time, semester, status

7. **reports** - Generated reports
   - id, title, report_type, generated_by, content, file_path, created_at

8. **logs** - Activity logs
   - id, user_id, action, details, ip_address, created_at

## Key Features Implemented

### Authentication & Security
✅ User registration with validation
✅ Secure login system
✅ Password hashing
✅ Role-based access control
✅ Session management
✅ Input sanitization

### Room Management
✅ Add/edit/delete classrooms
✅ Equipment tracking
✅ Capacity management
✅ Availability checking
✅ Facility status tracking

### Booking System
✅ Search available rooms
✅ Request bookings
✅ Admin approval workflow
✅ Booking cancellation
✅ Conflict detection
✅ Status tracking

### Schedule Management
✅ Create class schedules
✅ Manage recurring schedules
✅ Automatic conflict detection
✅ Teacher schedule view
✅ Classroom schedule view

### Reporting
✅ Resource utilization report
✅ Booking statistics
✅ Peak hour analysis
✅ Underutilized rooms report
✅ Data export (CSV/PDF)
✅ Chart visualization

### UI/UX
✅ Modern, professional design
✅ Color-coded status indicators
✅ Responsive layout
✅ Intuitive navigation
✅ Quick action buttons
✅ Data tables with filtering

## Installation Requirements

- Python 3.7 or higher
- pip (Python package manager)
- ~200 MB disk space
- 512 MB RAM minimum
- Display: 1024x768 minimum

## Running the Application

```bash
# Navigate to project directory
cd SmartCampus

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Default Credentials

- **Username**: admin
- **Password**: admin123

⚠️ Change immediately in production!

## Support & Documentation

- **README.md** - Complete project documentation
- **USER_MANUAL.md** - Detailed user guide
- **INSTALLATION.md** - Installation instructions
- **DEPLOYMENT.md** - Deployment guide
- **Inline comments** - Code documentation

---

**Total Project Size**: ~500-600 MB (with virtual environment)
**Executable Size**: ~150-200 MB (packaged as .exe)
**Database Size**: ~100 KB (grows with usage)

**Version**: 1.0.0
**Status**: Production Ready ✅
**Last Updated**: January 8, 2026
