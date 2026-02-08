# QUICK REFERENCE GUIDE

## 🚀 Quick Start (5 Minutes)

### 1. Install
```bash
cd SmartCampus
pip install -r requirements.txt
```

### 2. Run
```bash
python main.py
```

### 3. Login
- **Username**: admin
- **Password**: admin123

---

## 📱 Default Roles

| Role | Access | Permissions |
|------|--------|-------------|
| **Admin** | Full | Manage everything |
| **Teacher** | Limited | Book rooms, create schedules |
| **Student** | Limited | Book rooms, view availability |

---

## 🔑 Key Features

### Authentication
```python
User.login(username, password)
User.register()
```

### Classroom Management
```python
Classroom.create()
Classroom.get_all_classrooms()
Classroom.get_available_classrooms()
```

### Booking System
```python
Booking.create()
Booking.approve()
Booking.reject()
Booking.cancel()
Booking.check_conflict()
```

### Schedules
```python
Schedule.create()
Schedule.get_teacher_schedules()
Schedule.check_conflict()
```

---

## 🎨 UI Navigation

### Admin Dashboard
1. **Dashboard** - Statistics overview
2. **Users** - User management
3. **Classrooms** - Room management
4. **Bookings** - Approval workflow
5. **Schedules** - Timetable management
6. **Reports** - Analytics & reports

### User Dashboard
1. **Dashboard** - Overview & quick actions
2. **My Bookings** - Booking history
3. **Available Rooms** - Search & book
4. **My Schedules** (Teachers) - Class schedule
5. **Profile** - User information

---

## 🛠️ Common Tasks

### Add a User (Admin)
1. Go to Users tab
2. Click "+ Add User"
3. Fill form
4. Click Create

### Book a Room (Student/Teacher)
1. Go to Available Rooms
2. Filter by date/time
3. Click "Book"
4. Enter details
5. Submit

### Approve Booking (Admin)
1. Go to Bookings tab
2. Find pending booking
3. Click "View"
4. Approve or Reject

### Create Schedule (Teacher)
1. Go to My Schedules
2. Click "+ Add Schedule"
3. Fill details
4. Submit

---

## 📊 Database Tables

| Table | Purpose |
|-------|---------|
| users | User accounts |
| departments | Organization structure |
| classrooms | Room information |
| equipment | Resource inventory |
| bookings | Room reservations |
| schedules | Class timetables |
| reports | Generated reports |
| logs | Activity tracking |

---

## 🔐 Credentials

**Default Admin:**
- Username: `admin`
- Password: `admin123`

⚠️ Change in production!

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `config.py` | Settings & constants |
| `smartcampus.db` | Database (auto-created) |
| `requirements.txt` | Dependencies |
| `README.md` | Full documentation |
| `USER_MANUAL.md` | User guide |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Submit form |
| Escape | Close dialog |
| Tab | Navigate fields |
| Ctrl+Q | Quit application |

---

## 🎨 Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Blue | #2563EB |
| Success | Green | #059669 |
| Danger | Red | #DC2626 |
| Warning | Amber | #F59E0B |
| Info | Sky Blue | #0EA5E9 |

---

## 📞 Support Commands

### Check Python Version
```bash
python --version
```

### List Installed Packages
```bash
pip list
```

### Reset Database
```bash
# Delete smartcampus.db and restart
```

### View Logs
```bash
# Check logs directory for errors
```

---

## 🧪 Test Accounts

Create test accounts:
1. Click "Sign Up" on login
2. Fill registration form
3. Set role as needed
4. Submit

---

## 💡 Tips & Tricks

1. **Search Efficiently**
   - Filter by room type first
   - Check multiple dates
   - Use specific time ranges

2. **Avoid Conflicts**
   - System prevents overlaps
   - Check calendar before booking
   - Plan ahead for recurring events

3. **Manage Bookings**
   - Cancel pending bookings anytime
   - Track status regularly
   - Contact admin if rejected

4. **Admin Tasks**
   - Regular database backups
   - Monitor pending bookings daily
   - Review underutilized rooms
   - Generate reports weekly

---

## 🐛 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run: `pip install -r requirements.txt` |
| Database locked | Delete `.db-journal` file |
| Won't start | Install Python 3.7+ |
| UI elements missing | Check screen resolution |
| Login fails | Reset admin password |

---

## 📚 Documentation Quick Links

- **README.md** - Full project documentation
- **USER_MANUAL.md** - Complete user guide
- **INSTALLATION.md** - Setup instructions
- **DEPLOYMENT.md** - Production deployment
- **PROJECT_SUMMARY.md** - Completion report
- **FILE_STRUCTURE.md** - File organization

---

## 🔄 Workflow Examples

### Student Workflow
```
1. Login
2. Browse Available Rooms
3. Select date/time
4. Book Classroom
5. Wait for Approval
6. View Booking Status
```

### Admin Workflow
```
1. Login
2. Review Dashboard
3. Check Pending Bookings
4. Approve/Reject
5. Manage Users
6. Generate Reports
```

### Teacher Workflow
```
1. Login
2. Create/View Schedule
3. Book Additional Rooms
4. Check Availability
5. View Profile
```

---

## 📊 Useful Statistics

- **Total Users**: Displayed on dashboard
- **Total Bookings**: Displayed on dashboard
- **Pending Approvals**: Shown in admin dashboard
- **Room Utilization**: In reports tab
- **Peak Hours**: In reports tab

---

## 🎯 Best Practices

1. ✅ Change default passwords
2. ✅ Backup database regularly
3. ✅ Review pending bookings daily
4. ✅ Monitor system logs
5. ✅ Update user information
6. ✅ Archive old records
7. ✅ Keep documentation updated

---

## 📦 Dependencies

```
PyQt5          # GUI Framework
matplotlib     # Charting
numpy          # Numerics
python-dateutil # Dates
```

Install: `pip install -r requirements.txt`

---

## 🆘 Get Help

1. Check **README.md**
2. Review **USER_MANUAL.md**
3. See **INSTALLATION.md**
4. Read inline code comments
5. Contact support

---

## ✨ Features at a Glance

✅ Multi-role authentication
✅ Room reservation system
✅ Automatic conflict detection
✅ Schedule management
✅ Report generation
✅ Professional UI
✅ Secure database
✅ Easy installation
✅ Comprehensive documentation
✅ Production-ready

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: January 8, 2026

---

## 🚦 Getting Started Checklist

- [ ] Install Python 3.7+
- [ ] Extract SmartCampus folder
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run application: `python main.py`
- [ ] Login with admin credentials
- [ ] Change admin password
- [ ] Add your institution details
- [ ] Create user accounts
- [ ] Start using the system

---

**Congratulations! You're ready to use Smart Campus!** 🎉
