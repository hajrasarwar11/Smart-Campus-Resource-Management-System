# Smart Campus - User Manual & Documentation

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Features Guide](#features-guide)
4. [Admin Guide](#admin-guide)
5. [Student Guide](#student-guide)
6. [Teacher Guide](#teacher-guide)
7. [FAQ](#faq)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Logging In
1. Launch the application: `python main.py`
2. Enter your username/email and password
3. Click "Login"

**First Time Users:**
- Use "Sign Up" to create a new account
- Fill in all required fields
- Verify email and confirm password
- Account will be created instantly

### Navigation
- Use the menu bar for major functions
- Tabs at the top to switch between sections
- Buttons for specific actions
- Right-click for context menus

## User Roles

### Admin
**Responsibilities:**
- User management
- Classroom and equipment management
- Booking approvals
- Report generation
- System maintenance

**Access:**
- Complete system control
- View all users, bookings, schedules
- Generate comprehensive reports

### Teacher
**Responsibilities:**
- Create and manage class schedules
- Book classrooms for lectures
- View resource availability

**Access:**
- Book rooms and equipment
- Manage personal schedule
- View class bookings
- Generate personal reports

### Student
**Responsibilities:**
- Book study rooms
- Reserve equipment
- Check classroom availability

**Access:**
- Book classrooms
- View available resources
- Track personal bookings
- View schedules

## Features Guide

### Dashboard Overview
The dashboard provides at-a-glance information:
- Statistics (total users, classrooms, bookings, pending approvals)
- Quick action buttons
- Recent activity
- Key metrics

### User Management (Admin)

**Adding a User:**
1. Click "Users" tab
2. Click "+ Add User"
3. Fill in required information:
   - Full name
   - Username (unique)
   - Email (unique)
   - Phone number
   - Department
   - Role (Admin, Teacher, Student)
4. Click "Create User"
5. System generates temporary password
6. Share credentials securely

**Editing a User:**
1. Find user in table
2. Click on row
3. Modify information
4. Click "Save"

**Deactivating a User:**
1. Select user
2. Click "Deactivate"
3. Confirm action

### Classroom Management (Admin)

**Adding a Classroom:**
1. Go to "Classrooms" tab
2. Click "+ Add Classroom"
3. Enter details:
   - Room number (e.g., 101, A-201)
   - Type (Theory, Lab, Seminar, Conference)
   - Capacity (number of students)
   - Building name
   - Floor number
   - Description
4. Click "Create"

**Managing Equipment:**
1. Select classroom
2. Click "Equipment"
3. Add/remove equipment items
4. Specify quantity and condition
5. Save changes

### Booking System

**Searching for Available Rooms:**
1. Go to "Available Rooms" tab
2. Filter by:
   - Room type
   - Date (select future date)
   - Time slot (from and to)
3. View matching classrooms
4. Check capacity and facilities

**Making a Booking:**
1. Click "Book" on desired room
2. Enter booking details:
   - Course/Event name
   - Purpose/Description
3. Verify date and time
4. Submit request
5. Status becomes "Pending" (awaiting approval)

**Tracking Bookings:**
1. Go to "My Bookings"
2. View all your bookings
3. Status indicators:
   - ✓ Approved (confirmed)
   - ⏱ Pending (waiting for approval)
   - ✗ Rejected (request denied)
   - ⊘ Cancelled (you cancelled)
4. Click "View" for details

**Cancelling a Booking:**
1. Go to "My Bookings"
2. Find pending booking
3. Click "Cancel"
4. Provide cancellation reason
5. Confirm cancellation

### Schedule Management

**Viewing Schedules:**
1. Go to "Schedules" tab
2. View all available schedules
3. Filter by:
   - Teacher name
   - Classroom
   - Day of week

**Creating Schedule (Teachers):**
1. Go to "My Schedules"
2. Click "+ Add Schedule"
3. Enter:
   - Course name
   - Classroom
   - Day of week
   - Start time
   - End time
   - Semester
4. System checks for conflicts
5. Click "Create"

**Managing Schedule:**
1. View current schedule
2. Edit or delete entries
3. System updates automatically

### Reports & Analytics

**Generating Reports:**
1. Go to "Reports" tab
2. Select report type:
   - **Resource Usage**: Utilization by classroom
   - **Booking Statistics**: Booking trends
   - **Peak Hours**: Busiest times
   - **Underutilized Rooms**: Low-usage classrooms

3. Reports display:
   - Charts and graphs
   - Data tables
   - Summary statistics
4. Export to file (PDF/CSV)

**Exporting Data:**
1. Go to report
2. Click "Export"
3. Choose format (PDF, CSV, Excel)
4. Specify date range
5. Download file

## Admin Guide

### System Administration

**Backup Database:**
1. File > Backup Database
2. Choose backup location
3. Confirm backup completion
4. Backup file created with timestamp

**User Management:**
- Create accounts for teachers and students
- Assign appropriate roles
- Monitor account status
- Deactivate inactive accounts
- Generate user reports

**Classroom Configuration:**
- Add and configure classrooms
- Manage equipment inventory
- Set capacity limits
- Track facility status
- Assign to departments

**Booking Workflow:**
1. Review pending bookings
2. Check for conflicts
3. Approve valid requests
4. Reject unsuitable requests
5. Provide feedback to users

**Reporting:**
- Resource utilization analysis
- Booking statistics
- Peak hour identification
- Facility recommendations
- Cost analysis (if integrated)

### Approval Workflow

**Pending Bookings:**
1. Click "Bookings" tab
2. Filter by "Pending"
3. Review booking details
4. Check for conflicts
5. **Approve:** Confirms booking (user notified)
6. **Reject:** Denies booking (provide reason)
7. **Hold:** For later review

### Settings
File > Settings to configure:
- Institution name
- Notification preferences
- Report formats
- Email settings (if configured)

## Student Guide

### Finding and Booking Rooms

**Step 1: Search**
- Go to "Available Rooms"
- Set date (tomorrow or later)
- Select time slot
- Choose room type
- View results

**Step 2: Book**
- Click "Book" button
- Enter course/event name
- Add description if needed
- Review details
- Click "Submit"

**Step 3: Wait for Approval**
- Go to "My Bookings"
- Check status: Pending
- Admin reviews and approves
- You'll see status update

**Step 4: Confirmed**
- Status: Approved
- Booking is confirmed
- Use the room at scheduled time

### Managing Bookings
- View all bookings in one place
- See approval status
- Cancel pending bookings
- View booking history

### Checking Schedules
- View classroom timetables
- Check teacher schedules
- See room availability
- Plan study sessions accordingly

## Teacher Guide

### Managing Classes

**Create Schedule:**
1. Go to "My Schedules"
2. Click "+ Add Schedule"
3. Enter course details
4. Assign classroom
5. Set days and times
6. Confirm no conflicts
7. Submit schedule

**View Schedule:**
- See all your courses
- Check assigned rooms
- View day/time
- See enrolled students (if integrated)

**Book Additional Rooms:**
- Same as student process
- Request additional classrooms
- For labs, seminars, tutorials
- Wait for admin approval

### Reports & Analysis
- View your class bookings
- See student attendance (if integrated)
- Generate class reports
- Export attendance records

## FAQ

### Booking Questions

**Q: How long does approval take?**
A: Usually within 24 hours. During busy times, up to 48 hours.

**Q: Can I book a room for multiple dates?**
A: Book once per date. Repeat bookings for recurring classes.

**Q: What if my booking is rejected?**
A: Check the reason in the booking details. Modify request or choose different time.

**Q: Can I change my booking?**
A: Cancel the current booking and create a new one with desired details.

### Schedule Questions

**Q: Why does the system show a conflict?**
A: You or the classroom already has something scheduled at that time.

**Q: Can two teachers share a classroom?**
A: Only at different times. The system prevents overlapping schedules.

**Q: How do I view the master timetable?**
A: Admin dashboard shows all schedules. User dashboard shows your schedule.

### Account Questions

**Q: Forgot password - what do I do?**
A: Contact admin to reset password. No self-service reset in this version.

**Q: Can I change my role?**
A: No, only admin can change roles. Contact administrator.

**Q: How do I delete my account?**
A: Contact admin. Account data may be required for records.

### Technical Questions

**Q: What browsers are supported?**
A: This is a desktop application, not browser-based.

**Q: Can I access from my phone?**
A: Currently desktop only. Mobile version planned for future.

**Q: Where is my data stored?**
A: In local SQLite database (smartcampus.db) in the application folder.

## Troubleshooting

### Application Won't Start

**Error: "Python not found"**
- Install Python 3.7 or higher
- Add Python to system PATH
- Restart computer

**Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Error: "Database locked"**
- Close other instances of the application
- Delete `.db-journal` file if exists
- Restart application

### Login Issues

**Issue: "Invalid username or password"**
- Check capslock
- Ensure username is correct
- Ask admin to reset password if forgotten
- Verify account is active

**Issue: "Account deactivated"**
- Contact admin to reactivate
- Only admin can activate accounts

### Booking Issues

**Issue: "No available rooms found"**
- Try different time slot
- Extend time range
- Check different day
- Select different room type

**Issue: "Booking time conflict"**
- System prevents overlapping bookings
- Choose different time
- Check classroom schedule

**Issue: "Booking stuck on pending"**
- Normal: admin must approve
- If > 48 hours: contact admin
- Cancel and resubmit if needed

### Display Issues

**Issue: "UI elements not visible"**
- Check screen resolution (minimum 1024x768)
- Restart application
- Reinstall PyQt5:
  ```bash
  pip install --upgrade PyQt5
  ```

**Issue: "Text too small/large"**
- Currently no zoom feature
- Adjust system display settings
- Change font size in system settings

## Getting Help

### Support Channels
- Email: support@smartcampus.edu
- Phone: +1-XXX-XXX-XXXX
- In-app Help menu
- Documentation (this file)

### Reporting Bugs
1. Note the error message
2. Describe what you were doing
3. Include screenshots if possible
4. Contact support with details

### Feature Requests
- Submit through support email
- Include use case
- Explain benefit
- Help us prioritize improvements

---

**Last Updated**: January 8, 2026  
**Version**: 1.0.0

For the latest documentation, visit the README.md file.
