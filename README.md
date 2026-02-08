# Smart Campus Resource Management System
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
