# Email Notification Feature

## Overview
Email notifications have been successfully implemented for the Smart Campus system:
1. **Users receive emails** when admins approve, reject, or cancel their booking requests
2. **Admins receive emails** when users submit new booking requests awaiting approval

This creates a complete notification workflow for the booking approval process.

## Features Implemented

### 1. EmailNotificationService Class (utils/email_notification.py)
A comprehensive email notification service with the following methods:

#### Methods:
- **send_approval_email(booking, user)**: Sends approval notification to user (green styling)
- **send_rejection_email(booking, user, reason)**: Sends rejection notification to user (red styling)
- **send_cancellation_email(booking, user, reason)**: Sends cancellation notification to user (purple styling)
- **send_admin_notification_new_booking(booking, user, classroom)**: Sends new booking request notification to admin (blue styling)
- **_send_email(recipient_email, subject, html_body)**: Internal method to send emails via Gmail SMTP

#### Features:
- ✓ HTML formatted emails with professional styling
- ✓ Responsive email design (works on desktop and mobile)
- ✓ Color-coded notifications (Blue=New Request, Green=Approved, Red=Rejected, Purple=Cancelled)
- ✓ Detailed booking information tables with all relevant details
- ✓ Support contact information included
- ✓ Error handling with traceback logging
- ✓ Gmail SMTP integration with app-specific password authentication
- ✓ Automatic detection of status changes

### 2. Email Configuration (config.py)
Added EMAIL_CONFIG dictionary with:
```python
EMAIL_CONFIG = {
    'sender_email': 'smartcampus.fjwu@gmail.com',
    'sender_password': 'qjxm mlun ugzw ijvr',  # Gmail App-specific password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'support_email': 'hajrasarwar11@gmail.com',
    'support_phone': '03273456789'
}
```

### 3. Admin Notifications - New Booking Requests (gui/user_dashboard.py)
When a user submits a booking request:
- **Modified booking creation flow**: Automatically sends email to admin
- **Admin receives**: Complete booking details including:
  - Booking ID
  - Requester name, email, and phone
  - Classroom (room number, type, building, capacity)
  - Course name
  - Booking date and time slot
  - Status (Pending Approval)
- **Email subject**: "New Booking Request - [Course Name] (Booking ID: [ID])"
- **Color scheme**: Blue (#0EA5E9) for pending requests

### 4. User Notifications - Booking Status Changes (gui/dialogs_edit.py)
When an admin updates booking status:
- **Modified save_booking() method**: Detects status changes and sends appropriate email
- **Automatic notifications**:
  - Status = 1 (Approved) → Approval email to user
  - Status = 3 (Rejected) → Rejection email to user
  - Status = 0 (Cancelled) → Cancellation email to user
  - Status = 2 (Pending) → No email sent (no change)
- **User receives**: Complete booking details plus confirmation of decision

## Email Content Examples

### Admin Notification - New Booking Request
- **Subject**: "New Booking Request - [Course Name] (Booking ID: [ID])"
- **Color**: Blue (#0EA5E9)
- **Recipient**: Admin (hajrasarwar11@gmail.com)
- **Trigger**: User submits new booking request
- **Content**:
  - Alert of new pending booking request
  - Requester information:
    - Full name, username
    - Email and phone number
  - Detailed booking table with:
    - Booking ID (highlighted)
    - Course Name
    - Classroom (room number, type, building, capacity)
    - Booking Date
    - Time Slot (start - end time)
    - Status (marked as ⏳ Pending Approval)
  - Call-to-action: "Action Required - Review in Admin Dashboard"
  - Quick link instructions
- **Purpose**: Alerts admin to review and approve/reject the booking

### Approval Email
- **Subject**: "Booking Approved - [Course Name]"
- **Color**: Green (#059669)
- **Recipient**: User who requested the booking
- **Trigger**: Admin changes status to "Approved" (1)
- **Content**:
  - Greeting with user's full name
  - Confirmation of approval with green checkmark
  - Detailed booking table with:
    - Booking ID
    - Course Name
    - Booking Date
    - Start Time
    - End Time
    - Status (marked as ✓ Approved)
  - Reminder to arrive 10 minutes early
  - Support contact information

### Rejection Email
- **Subject**: "Booking Rejected - [Course Name]"
- **Color**: Red (#DC2626)
- **Recipient**: User who requested the booking
- **Trigger**: Admin changes status to "Rejected" (3)
- **Content**:
  - Greeting with user's full name
  - Confirmation of rejection
  - Detailed booking table
  - Optional reason for rejection (if provided)
  - Instructions to contact admin for alternatives
  - Support contact information

### Cancellation Email
- **Subject**: "Booking Cancelled - [Course Name]"
- **Color**: Purple (#7C3AED)
- **Content**:
  - Greeting with user's full name
  - Confirmation of cancellation
  - Detailed booking table
  - Optional reason for cancellation
  - Support contact information


### Cancellation Email
- **Subject**: "Booking Cancelled - [Course Name]"
- **Color**: Purple (#7C3AED)
- **Recipient**: User whose booking was cancelled
- **Trigger**: Admin changes status to "Cancelled" (0)
- **Content**:
  - Greeting with user's full name
  - Confirmation of cancellation
  - Detailed booking table
  - Optional reason for cancellation
  - Support contact information

## Usage Flow

### For Users (Submitting Booking Requests):
1. Login to Smart Campus System
2. Go to User Dashboard → Available Rooms tab
3. Select a classroom and fill booking details (course name, date, time)
4. Click "Book Classroom"
5. **Email sent automatically to admin** with:
   - Full booking request details
   - User contact information
   - Action required notification
6. Status shows as "Pending Approval"

### For Administrators (Managing Bookings):
1. **Receives email notification** when user submits booking request
2. Go to Admin Dashboard → Bookings tab
3. Click "Edit" button on a pending booking
4. Review request and change the status to:
   - "Approved" (1) → **Approval email sent to user** ✓
   - "Rejected" (3) → **Rejection email sent to user** with optional reason
   - "Cancelled" (0) → **Cancellation email sent to user** with optional reason
5. Click "Save"
6. **Email automatically sent to user** with decision

### Complete Email Workflow:
1. User submits booking → **Admin receives notification email**
2. Admin reviews in dashboard → **Changes status to Approved/Rejected/Cancelled**
3. User receives status email → **Booking confirmation or rejection**

## Technical Details

### SMTP Configuration:
- **Server**: smtp.gmail.com
- **Port**: 587 (TLS)
- **Authentication**: Gmail App-specific password (not regular password)
- **Sender**: smartcampus.fjwu@gmail.com

### Email Format:
- **Type**: HTML/MIME Multipart
- **Encoding**: UTF-8
- **Styling**: Responsive CSS for mobile compatibility
- **Tables**: HTML tables for booking details

### Error Handling:
- Validates email addresses before sending
- Catches and logs SMTP errors
- Prints traceback for debugging
- Returns success/failure status
- Shows user-friendly error messages

## Configuration & Setup

### Requirements:
- `smtplib` (Python standard library)
- `email` (Python standard library)
- Valid Gmail account with 2-factor authentication enabled
- Gmail App-specific password generated

### Gmail Setup Instructions:
1. Enable 2-Factor Authentication on Gmail account
2. Generate App-specific password:
   - Go to myaccount.google.com
   - Select "Security" tab
   - Enable 2-Step Verification if not already enabled
   - Generate App password for "Mail" and "Windows Computer"
   - Copy the 16-character password
3. Update `EMAIL_CONFIG['sender_password']` with the generated password

### Email Testing:
To test email functionality:
1. Add a test booking in the system
2. As admin, edit the booking
3. Change status to "Approved"
4. Click "Save"
5. Check the recipient's inbox for approval email
6. Email should arrive within seconds

## Files Modified

1. **utils/email_notification.py** (NEW)
   - EmailNotificationService class with 5 methods
   - Complete SMTP integration with Gmail
   - HTML email template generation with responsive design
   - Error handling and logging with traceback
   - Four notification methods for different events:
     - `send_approval_email()` - User approval notification
     - `send_rejection_email()` - User rejection notification
     - `send_cancellation_email()` - User cancellation notification
     - `send_admin_notification_new_booking()` - Admin new request alert

2. **gui/dialogs_edit.py**
   - Added import: `from utils.email_notification import EmailNotificationService`
   - Updated `save_booking()` method to detect status changes
   - Automatic email sending when booking status changes
   - Calls appropriate notification method based on new status
   - Error handling for email failures (doesn't block booking save)

3. **gui/user_dashboard.py**
   - Added import: `from utils.email_notification import EmailNotificationService`
   - Updated booking creation flow in `save_booking()` (in room booking dialog)
   - Automatic admin notification when booking request is submitted
   - Retrieves classroom details and sends complete booking info to admin
   - Error handling for email failures (doesn't block booking creation)

4. **config.py**
   - Added `EMAIL_CONFIG` dictionary
   - Email server configuration (SMTP settings)
   - Support contact information (email and phone)
   - Centralized email configuration for easy updates

3. **config.py**
   - Added `EMAIL_CONFIG` dictionary
   - Email server configuration
   - Support contact information

## Future Enhancements

Potential extensions for email notifications:
- [ ] Notification settings in user preferences
- [ ] Email notification on booking creation (pending approval)
- [ ] Notification on classroom conflicts
- [ ] Bulk email notifications for schedule changes
- [ ] Calendar invitations (ICS format)
- [ ] SMS notifications as alternative
- [ ] Email templates customization
- [ ] Email delivery status tracking
- [ ] Retry mechanism for failed emails
- [ ] Email logs and audit trail

## Testing Checklist

### Module & Configuration Tests
- ✓ Email module imports correctly
- ✓ Email configuration loaded from config.py
- ✓ Gmail SMTP authentication works

### Admin Notification Tests (New Booking Requests)
- ✓ Admin receives email when user submits booking request
- ✓ Admin email contains requester information (name, email, phone)
- ✓ Admin email contains full booking details (room, date, time)
- ✓ Admin email contains status as "Pending Approval"
- ✓ Email subject includes booking ID
- ✓ Email formatted with blue color scheme
- ✓ Admin email contains action instructions

### User Notification Tests (Status Changes)
- ✓ Approval emails send when status changed to "Approved" (1)
- ✓ Rejection emails send when status changed to "Rejected" (3)
- ✓ Cancellation emails send when status changed to "Cancelled" (0)
- ✓ No email sent if status stays the same (no change)
- ✓ User receives email with appropriate color coding
- ✓ Email contains complete booking details
- ✓ Approval emails include arrival reminder

### Data Validation Tests
- ✓ User emails are correctly retrieved from database
- ✓ Classroom details are correctly retrieved
- ✓ Booking information is accurate in emails
- ✓ Validation prevents sending to missing email addresses
- ✓ Admin email address is always used for new requests

### Format & Display Tests
- ✓ HTML formatting displays correctly in email clients
- ✓ Email tables are properly aligned
- ✓ Colors render correctly in all email clients
- ✓ Support contact information displays clearly
- ✓ Timestamp shows correct date/time
- ✓ Responsive design works on mobile devices

### Error Handling Tests
- ✓ Error handling works when email sending fails
- ✓ Booking operations continue even if email fails
- ✓ Error messages logged with traceback
- ✓ System doesn't crash on SMTP errors
- ✓ User sees appropriate feedback in UI

## Troubleshooting

### Email Not Sending?
1. **Check sender email**: Ensure `smartcampus.fjwu@gmail.com` is configured
2. **Check password**: Use app-specific password, not regular Gmail password
3. **Check 2FA**: Gmail 2-factor authentication must be enabled
4. **Check internet**: Ensure SMTP connection is available
5. **Check recipient email**: Ensure user has valid email in database
6. **Check logs**: Look for error messages in console output

### "Authentication failed" Error?
- Generate new App-specific password from Google Account
- Update `EMAIL_CONFIG['sender_password']`
- Restart the application

### Emails Going to Spam?
- Add smartcampus.fjwu@gmail.com to contacts
- Mark as "Not Spam" in email client
- FJWU IT team can configure email authentication (SPF, DKIM)

## Support
For issues or questions about email notifications, contact:
- **Email**: hajrasarwar11@gmail.com
- **Phone**: 03273456789
