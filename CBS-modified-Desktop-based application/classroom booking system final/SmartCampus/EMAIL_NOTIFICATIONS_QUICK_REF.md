# Email Notifications - Quick Reference

## What's New?
Email notifications have been added for booking status changes. When an admin approves, rejects, or cancels a booking, the user automatically receives a professional formatted email notification.

## How It Works

### For Admins:
1. Open Admin Dashboard
2. Go to **Bookings Tab**
3. Click **Edit** on any booking
4. Change the status:
   - ✓ **Approved** → Green email sent
   - ✗ **Rejected** → Red email sent
   - ⊗ **Cancelled** → Purple email sent
   - ⏳ **Pending** → No email (no change)
5. Click **Save**
6. Email automatically sends to the user

### For Users:
- Check your email inbox for booking notifications
- Emails include all booking details and support contact info
- Approve/Reject/Cancel notifications arrive within seconds

## Email Features

✓ **Professional HTML Formatting** - Responsive design for all devices
✓ **Color-Coded Status** - Green/Red/Purple for quick identification
✓ **Booking Details Table** - All relevant information included
✓ **Support Contact Info** - Easy way to reach support team
✓ **Automatic Timestamps** - When email was sent
✓ **University Branding** - FJWU logo and information

## Email Contains:
- Recipient's full name (personalized)
- Booking ID
- Course name
- Booking date
- Start time
- End time
- Booking status (Approved/Rejected/Cancelled)
- Optional reason (for rejections/cancellations)
- Support email: hajrasarwar11@gmail.com
- Support phone: 03273456789

## System Configuration

**Email Settings (in config.py):**
- Sender: smartcampus.fjwu@gmail.com
- SMTP: smtp.gmail.com:587
- Sender uses Gmail app-specific password authentication

## Files Modified

1. ✓ **utils/email_notification.py** - NEW (Email service module)
2. ✓ **gui/dialogs_edit.py** - Updated with email integration
3. ✓ **config.py** - Added EMAIL_CONFIG settings

## Testing the Feature

### Test Approval Email:
1. Go to Admin Dashboard → Bookings
2. Click Edit on any pending booking
3. Change status to "Approved"
4. Click Save
5. Check user's inbox for approval email

### Test Rejection Email:
1. Go to Admin Dashboard → Bookings
2. Click Edit on any pending booking
3. Change status to "Rejected"
4. Click Save
5. Check user's inbox for rejection email

### Test Cancellation Email:
1. Go to Admin Dashboard → Bookings
2. Click Edit on any approved booking
3. Change status to "Cancelled"
4. Click Save
5. Check user's inbox for cancellation email

## Important Notes

⚠️ **Email requires:**
- Valid user email address in database
- Internet connection to Gmail SMTP
- Gmail 2-factor authentication enabled
- App-specific password (not regular password)

⚠️ **Emails only send when:**
- Status actually changes (Pending→Approved, etc.)
- User has valid email address
- SMTP connection is available
- Email credentials are correct

## Troubleshooting

**Q: Email not sending?**
A: Check console for error messages. Ensure internet connection and user has email address.

**Q: "Authentication failed" error?**
A: App-specific password may have expired. Generate new password from Google Account settings.

**Q: Email in spam folder?**
A: Add smartcampus.fjwu@gmail.com to your contacts and mark as "Not Spam".

**Q: Want to disable email?**
A: Comment out email lines in dialogs_edit.py save_booking() method (lines 269-273).

## Future Enhancements

Planned additions:
- Email on new booking creation
- Calendar invitations (ICS format)
- Bulk notifications for schedule changes
- SMS notifications option
- Email notification preferences per user
- Email template customization
- Email delivery tracking and logs

---

**Documentation**: See EMAIL_NOTIFICATIONS.md for detailed technical information
**Support**: hajrasarwar11@gmail.com | 03273456789
