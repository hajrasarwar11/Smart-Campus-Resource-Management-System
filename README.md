# Smart Campus Resource Management System

A comprehensive desktop application built with Python and PyQt5 to manage university resources including classrooms, equipment, and teacher schedules.

## Features

### Core Functionality
- **Multi-role Authentication**: Admin, Teacher, and Student accounts with secure login/signup
- **Classroom Management**: View, add, and manage available classrooms and labs
- **Room Booking**: Students and teachers can search, book, and manage room reservations
- **Conflict Detection**: Automatic detection of scheduling conflicts
- **Schedule Management**: Create and manage class schedules with automatic validation
- **Equipment Inventory**: Track and manage lab equipment and resources
- **Reports & Analytics**: Generate comprehensive reports on resource usage and utilization

### Advanced Features
- **Modern UI Design**: Professional, elegant, and intuitive interface
- **Real-time Updates**: Live data refresh and notifications
- **Data Persistence**: SQLite database for reliable data storage
- **Booking Approval Workflow**: Admin approval for pending bookings
- **Search & Filter**: Quick search for available slots and resources
- **Export Functionality**: Export reports and booking data
- **User Profile Management**: Edit profile, change password, view booking history

## Project Structure

```
SmartCampus/
├── main.py                      # Application entry point
├── config.py                    # Configuration and constants
│
├── database/
│   └── db_setup.py             # Database initialization and management
│
├── models/
│   ├── user.py                 # User model (authentication, profiles)
│   ├── classroom.py            # Classroom model
│   ├── booking.py              # Booking model and logic
│   └── schedule.py             # Schedule model
│
├── gui/
│   ├── styles.py               # Modern stylesheet
│   ├── login_window.py         # Login/authentication UI
│   ├── signup_window.py        # Registration UI
│   ├── admin_dashboard.py      # Admin interface
│   └── user_dashboard.py       # Student/Teacher interface
│
├── utils/
│   └── validation.py           # Input validation utilities
│
├── reports/
│   └── usage_report.py         # Report generation and charts
│
└── assets/
    └── (icons and resources)
```

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone or extract the project**
```bash
cd SmartCampus
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Demo Student/Teacher Accounts:**
- Username: `2023-BSE-022`
- Password: `password123`

⚠️ **Important**: Change default credentials in production!

## Usage Guide

### Admin Dashboard
1. Login with admin credentials
2. Access comprehensive dashboard with:
   - User management (add, edit, deactivate users)
   - Classroom management (add, edit, view classrooms)
   - Booking management (approve, reject, cancel bookings)
   - Schedule management (create and manage timetables)
   - Reports and analytics

### Student/Teacher Dashboard
1. Login with your credentials
2. Features available:
   - View available classrooms
   - Search for time slots
   - Book rooms for classes/events
   - View your bookings
   - Track booking status
   - View profile and edit information
   - (Teachers only) Manage class schedules

## Key Features in Detail

### Booking System
- Search for available rooms by type, date, and time
- Submit booking requests that require admin approval
- View booking status (Approved, Pending, Rejected, Cancelled)
- Cancel pending bookings
- Automatic conflict detection

### Schedule Management
- Create recurring schedules for courses
- Detect scheduling conflicts automatically
- View teacher and classroom schedules
- Manage semester-wise schedules

### Reports Module
- Resource utilization report
- Booking statistics and trends
- Peak hour analysis
- Underutilized rooms identification
- Export reports to text/CSV formats

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.x |
| **GUI Framework** | PyQt5 |
| **Database** | SQLite |
| **Data Visualization** | Matplotlib |
| **Authentication** | MD5 Hashing |

## Database Schema

### Main Tables
- **users**: User accounts and profiles
- **departments**: Department information
- **classrooms**: Room details and specifications
- **equipment**: Equipment inventory
- **bookings**: Room reservation records
- **schedules**: Class schedules and timetables
- **reports**: Generated reports
- **logs**: Activity logs

## API Functions

### User Management
```python
User.login(username, password)  # Authenticate user
User.register()                  # Create new account
User.get_all_users()            # Get all users (admin)
User.update_profile()           # Update user information
User.change_password()          # Change password
```

### Booking Management
```python
Booking.create()                # Create new booking
Booking.get_user_bookings()     # Get user's bookings
Booking.approve()               # Approve booking (admin)
Booking.reject()                # Reject booking (admin)
Booking.cancel()                # Cancel booking
Booking.check_conflict()        # Check scheduling conflicts
```

### Classroom Management
```python
Classroom.create()              # Add new classroom
Classroom.get_all_classrooms()  # Get all rooms
Classroom.get_available_classrooms()  # Search available rooms
```

## Validation

The system includes comprehensive validation for:
- Username and email uniqueness
- Password strength requirements
- Email format validation
- Date and time format validation
- Room capacity constraints
- Booking time slot conflicts

## Error Handling

- Input validation with user-friendly error messages
- Database transaction handling
- Exception handling for file operations
- Graceful error dialogs

## Future Enhancements

- [ ] Email notifications for booking approvals
- [ ] QR code generation for room identification
- [ ] Mobile application
- [ ] Integration with calendar applications
- [ ] Advanced reporting with AI predictions
- [ ] Video conferencing integration
- [ ] Resource request system
- [ ] Attendance tracking

## Security Considerations

- Passwords hashed using MD5 (upgrade to bcrypt in production)
- SQL injection prevention through parameterized queries
- Role-based access control
- Session management (30-minute timeout)
- Activity logging

## Support & Contact

For issues, suggestions, or support:
- Email: support@smartcampus.edu
- Documentation: See inline code comments

## License

© 2026 Smart Campus. All rights reserved.

## Contributors

- Development Team
- Faculty Advisors
- Student Testers

## Changelog

### Version 1.0.0 (2026-01-08)
- Initial release
- Complete admin dashboard
- User authentication and management
- Room booking system
- Schedule management
- Reports module
- Modern PyQt5 interface

## FAQ

**Q: How do I reset the admin password?**
A: Delete the database file (smartcampus.db) and restart the application to reset to default credentials.

**Q: Can multiple users book the same room at the same time?**
A: No, the system automatically detects and prevents booking conflicts.

**Q: Is there a backup feature?**
A: Yes, use File > Backup Database in the admin dashboard.

**Q: How long are sessions active?**
A: Sessions are active for 30 minutes of inactivity by default.

---

**Version**: 1.0.0  
**Last Updated**: January 8, 2026  
**Status**: Production Ready
