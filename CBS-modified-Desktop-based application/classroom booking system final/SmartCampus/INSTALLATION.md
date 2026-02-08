# Smart Campus Resource Management System - Installation Guide

## Prerequisites
- Windows, macOS, or Linux
- Python 3.7 or higher
- pip (Python package manager)

## Step-by-Step Installation

### 1. Install Python
Download and install Python from: https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation
- Verify installation: `python --version`

### 2. Extract Project Files
Extract the SmartCampus folder to your desired location.

### 3. Open Terminal/Command Prompt
Navigate to the SmartCampus folder:
```bash
cd path/to/SmartCampus
```

### 4. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```

Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take a few minutes).

### 6. Run the Application
```bash
python main.py
```

The application window should open automatically.

## First Time Setup

### Default Admin Login
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately after first login!

### Initial Configuration
1. Go to File > Settings (if available)
2. Configure your institution details
3. Add departments
4. Add classrooms
5. Invite users

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PyQt5'"
**Solution**: Install dependencies again
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete `smartcampus.db` file and restart the application

### Issue: Port already in use
**Solution**: The application doesn't require external ports; this shouldn't occur

### Issue: Python not recognized
**Solution**: Ensure Python is added to PATH:
- Windows: Reinstall Python with "Add to PATH" checked
- macOS/Linux: Use `python3` instead of `python`

### Issue: Permission denied
**Solution**: Run with administrator privileges (Windows) or use `sudo` (macOS/Linux)

## File Structure After Setup

```
SmartCampus/
├── main.py
├── config.py
├── requirements.txt
├── smartcampus.db          # (Created automatically)
├── database/
│   ├── __init__.py
│   └── db_setup.py
├── models/
│   ├── user.py
│   ├── classroom.py
│   ├── booking.py
│   └── schedule.py
├── gui/
│   ├── styles.py
│   ├── login_window.py
│   ├── signup_window.py
│   ├── admin_dashboard.py
│   └── user_dashboard.py
├── utils/
│   ├── validation.py
│   └── helpers.py
├── reports/
│   └── usage_report.py
└── README.md
```

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| **RAM** | 512 MB | 2 GB |
| **Disk Space** | 200 MB | 500 MB |
| **Processor** | 1 GHz | 2 GHz+ |
| **Screen Resolution** | 1024x768 | 1920x1080 |
| **Python** | 3.7 | 3.9+ |

## Post-Installation

### Backup Database
```bash
# In admin dashboard:
File > Backup Database
```

### Reset Application
To reset to default state:
1. Stop the application
2. Delete `smartcampus.db`
3. Delete any backup files
4. Restart the application

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Running in Production

### Security Considerations
1. Change default admin password
2. Use strong passwords for all accounts
3. Regularly backup the database
4. Keep Python and libraries updated
5. Run behind a firewall if networked

### Database Backup
```bash
# Manual backup
cp smartcampus.db smartcampus_backup.db
```

### Performance Optimization
1. Archive old records
2. Optimize database queries
3. Clear old logs periodically
4. Monitor disk space

## Support & Troubleshooting

For detailed troubleshooting:
1. Check `logs/` directory for error logs
2. Review README.md for detailed documentation
3. Check inline code comments for implementation details

## Uninstallation

To uninstall the application:

**Windows:**
1. Delete the SmartCampus folder
2. If using virtual environment, delete the venv folder

**macOS/Linux:**
```bash
rm -rf /path/to/SmartCampus
rm -rf /path/to/venv
```

Optionally remove Python:
- Windows: Control Panel > Programs > Programs and Features > Python
- macOS: Use `brew uninstall python3` (if installed with Homebrew)
- Linux: Use your package manager (apt, yum, etc.)

---

**Installation Complete!** The application is ready to use.
