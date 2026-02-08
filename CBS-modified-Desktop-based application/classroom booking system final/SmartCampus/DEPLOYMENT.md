# DEPLOYMENT.md - Deployment Guide

## Deployment Instructions

### Local Development Deployment

1. **Clone/Extract Project**
   ```bash
   cd path/to/SmartCampus
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

### Production Deployment

#### Windows Executable Creation

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create Executable**
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico main.py
   ```

3. **Distribution**
   - Executable located in `dist/` folder
   - Include in installer with all dependencies
   - Create installer using NSIS or InnoSetup

#### Linux Deployment

1. **Create AppImage**
   ```bash
   pip install appimage-builder
   appimage-builder --recipe AppImageBuilder.yml
   ```

2. **Create DEB Package**
   ```bash
   pip install stdeb
   python setup.py --command-packages=stdeb.command bdist_deb
   ```

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=:0
CMD ["python", "main.py"]
```

**Build and Run:**
```bash
docker build -t smartcampus:latest .
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix smartcampus:latest
```

### System Requirements

**Minimum:**
- OS: Windows 7/Linux/macOS 10.12+
- RAM: 512 MB
- Disk: 200 MB
- CPU: 1 GHz processor

**Recommended:**
- OS: Windows 10/11, Latest Linux/macOS
- RAM: 2-4 GB
- Disk: 500 MB SSD
- CPU: 2+ GHz multi-core

### Configuration for Deployment

1. **Update config.py**
   - Change default admin password
   - Set appropriate timeout values
   - Configure logging levels

2. **Database Setup**
   - First run creates SQLite database
   - Backup before deployment
   - Set proper permissions

3. **Security**
   - Change default credentials
   - Enable HTTPS if network-based
   - Implement firewall rules
   - Regular security updates

### Post-Deployment

1. **Verify Installation**
   - Test login with admin account
   - Verify database creation
   - Check file permissions
   - Test all major features

2. **Create Backup**
   ```bash
   cp smartcampus.db smartcampus_backup_$(date +%Y%m%d).db
   ```

3. **User Onboarding**
   - Import users from CSV (if feature added)
   - Set initial passwords
   - Send login credentials
   - Provide user documentation

4. **Monitoring**
   - Check log files regularly
   - Monitor disk space
   - Backup schedule
   - Performance metrics

---

For detailed installation instructions, see INSTALLATION.md
For usage guide, see USER_MANUAL.md
