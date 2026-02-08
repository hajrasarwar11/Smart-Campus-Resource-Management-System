# START HERE - Getting Started Guide

## 📌 Welcome to Smart Campus Resource Management System!

This guide will help you get up and running in just a few minutes.

---

## ⚡ QUICK START (5 MINUTES)

### Step 1: Install Python (if not already installed)
Download from: https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked
- Verify: Open terminal and type `python --version`

### Step 2: Navigate to Project Folder
```bash
cd d:\XAMPP\Files\htdocs\Project\classroom booking system final\SmartCampus
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

### Step 5: Login
The login window will appear. Use:
- **Username**: admin
- **Password**: admin123

✅ **You're in!** The admin dashboard should now be visible.

---

## 📚 Documentation Guide

Read these in order:

1. **QUICK_REFERENCE.md** ← Start here for features overview
2. **USER_MANUAL.md** ← How to use each feature
3. **README.md** ← Complete project documentation
4. **INSTALLATION.md** ← If you have installation issues

---

## 🎯 First Time Setup (10 MINUTES)

Once logged in as admin:

1. **Change Your Password**
   - Go to Profile tab
   - Click "Change Password"
   - Enter new secure password

2. **Review System**
   - Click "Dashboard" tab
   - View statistics and overview
   - Click quick action buttons

3. **Explore Features**
   - Check "Users" tab
   - Review "Classrooms" tab
   - Look at "Bookings" tab

---

## 🎓 Common First Tasks

### Task 1: Add a Classroom
1. Click "Classrooms" tab
2. Click "+ Add Classroom"
3. Fill in:
   - Room Number (e.g., "101")
   - Type (e.g., "Theory")
   - Capacity (e.g., "50")
   - Building (e.g., "Main")
   - Floor (e.g., "1")
4. Click "Create"

### Task 2: Create a User Account
1. Click "Users" tab
2. Click "+ Add User"
3. Fill in all fields
4. Click "Create User"

### Task 3: Test a Booking (as Admin)
1. Click "Bookings" tab
2. See sample bookings
3. Approve or reject

---

## 🔧 Troubleshooting

### Problem: "Python not found"
**Solution**: 
- Install Python from https://www.python.org/
- Make sure "Add to PATH" is checked
- Restart terminal

### Problem: "ModuleNotFoundError: No module named 'PyQt5'"
**Solution**:
```bash
pip install -r requirements.txt
```

### Problem: "Database error"
**Solution**:
- Delete `smartcampus.db` file if it exists
- Restart the application
- Database will be recreated automatically

### Problem: "Application won't start"
**Solution**:
1. Check Python version: `python --version`
2. Ensure Python 3.7 or higher
3. Reinstall dependencies

---

## 📖 Key Features Overview

### 👥 User Roles

**Admin**
- Manage all users
- Add/edit classrooms
- Approve/reject bookings
- Generate reports
- System settings

**Teacher**
- Book classrooms
- Create schedules
- View available rooms
- Track bookings

**Student**
- Search for rooms
- Book classrooms
- View my bookings
- Check availability

---

## 🎨 User Interface Overview

### Main Menu
- **File** → Settings, Backup, Logout, Exit
- **Edit** → Refresh data
- **Help** → About, Documentation

### Tabs
- **Dashboard** → Overview with statistics
- **Users** → Manage user accounts
- **Classrooms** → Manage rooms
- **Bookings** → Manage reservations
- **Schedules** → Manage timetables
- **Reports** → View analytics

---

## 🔐 Security Notes

⚠️ **Important**: Change the default admin password immediately!

**Default Credentials** (for development only):
- Username: admin
- Password: admin123

---

## 📂 Project Structure

```
SmartCampus/
├── main.py              ← Run this file
├── config.py            ← Settings
├── requirements.txt     ← Dependencies
├── database/            ← Database management
├── models/              ← Business logic
├── gui/                 ← User interface
├── utils/               ← Utilities
├── reports/             ← Report generation
└── [documentation files]
```

---

## 💾 Database

The application uses SQLite (local database):
- **File**: `smartcampus.db` (created automatically)
- **Tables**: 8 (users, classrooms, bookings, schedules, etc.)
- **Location**: Same folder as application

**To Reset**: Delete `smartcampus.db` and restart

---

## 🚀 What To Do Next

### If you're just exploring:
1. ✅ Read QUICK_REFERENCE.md
2. ✅ Explore all tabs in dashboard
3. ✅ Try adding a classroom
4. ✅ Check out reports

### If you're setting up for your institution:
1. ✅ Change admin password
2. ✅ Add all classrooms
3. ✅ Create user accounts for teachers
4. ✅ Create accounts for students
5. ✅ Configure settings
6. ✅ Start using system

### If you're deploying to production:
1. ✅ Change all default credentials
2. ✅ Read DEPLOYMENT.md
3. ✅ Set up regular backups
4. ✅ Configure security settings
5. ✅ Train users

---

## 📞 Help & Support

**Quick Questions?**
- Check QUICK_REFERENCE.md

**How do I use a feature?**
- Check USER_MANUAL.md

**Installation issues?**
- Check INSTALLATION.md

**Deployment help?**
- Check DEPLOYMENT.md

**Full documentation?**
- Read README.md

---

## ✨ Feature Highlights

✅ **Multi-user authentication** - Secure login system  
✅ **Room booking** - Search and reserve classrooms  
✅ **Conflict detection** - Prevents double-booking  
✅ **Admin approval** - Workflow for booking management  
✅ **Scheduling** - Create and manage timetables  
✅ **Reports** - Analytics and utilization reports  
✅ **Modern UI** - Professional, elegant interface  
✅ **Secure database** - SQLite with backup  

---

## 🎯 System Requirements Check

Before running, verify:
- ✅ Windows 7+ OR Mac OS 10.12+ OR Linux
- ✅ Python 3.7 or higher installed
- ✅ Minimum 512 MB RAM
- ✅ 200 MB disk space available
- ✅ 1024x768 or higher screen resolution

---

## 💡 Pro Tips

1. **Search Smarter**: Filter by room type, date, and time
2. **Avoid Conflicts**: System prevents double-bookings
3. **Save Time**: Use quick action buttons on dashboard
4. **Stay Organized**: Use department and building filters
5. **Track Status**: Check booking status regularly
6. **Generate Reports**: Use reporting tab for analytics

---

## 🎓 Learning Path

### For First-Time Users (30 minutes)
1. Read QUICK_REFERENCE.md
2. Follow "First Time Setup"
3. Try common tasks
4. Explore dashboard

### For Regular Users (1 hour)
1. Read USER_MANUAL.md
2. Learn all features
3. Practice bookings
4. Review reports

### For Administrators (2-3 hours)
1. Read complete README.md
2. Study USER_MANUAL.md
3. Review DEPLOYMENT.md
4. Practice user management

---

## 🔄 Daily Operations

### Admin Daily Tasks
- [ ] Review pending bookings
- [ ] Approve/reject as needed
- [ ] Check for conflicts
- [ ] Monitor system health

### Teacher Daily Tasks
- [ ] Check available classrooms
- [ ] Book rooms if needed
- [ ] Review schedule
- [ ] Check notifications

### Student Daily Tasks
- [ ] View available rooms
- [ ] Book study spaces
- [ ] Check booking status
- [ ] View schedules

---

## 🌟 What Makes This Special

✨ **Professional Design** - Modern, elegant interface  
✨ **Complete Solution** - Everything you need included  
✨ **Well Documented** - 7 comprehensive guides  
✨ **Production Ready** - Secure and tested  
✨ **Easy to Use** - Intuitive and clear  
✨ **Customizable** - Easy to modify and extend  

---

## 📋 Checklist to Get Started

- [ ] Install Python
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run application: `python main.py`
- [ ] Login as admin
- [ ] Change admin password
- [ ] Add first classroom
- [ ] Create first user
- [ ] Explore features
- [ ] Read documentation
- [ ] Start using system

---

## 🎉 You're All Set!

The Smart Campus Resource Management System is ready to use.

**Next Step**: Open `main.py` and start the application!

---

## 📚 Documentation Index

| Document | Purpose | Read Time |
|----------|---------|-----------|
| QUICK_REFERENCE.md | Feature overview | 5 min |
| USER_MANUAL.md | Complete user guide | 20 min |
| README.md | Full documentation | 30 min |
| INSTALLATION.md | Setup help | 10 min |
| DEPLOYMENT.md | Production setup | 15 min |
| FILE_STRUCTURE.md | Project organization | 5 min |
| PROJECT_SUMMARY.md | Completion report | 10 min |

---

**Version**: 1.0.0  
**Status**: Ready to Use ✅  
**Last Updated**: January 8, 2026  

**Enjoy using Smart Campus!** 🎓
