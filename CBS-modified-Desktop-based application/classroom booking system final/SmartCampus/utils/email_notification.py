"""
Email Notification Module for Smart Campus
Handles sending email notifications for booking approvals and other events
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class EmailNotificationService:
    """Service for sending email notifications"""
    
    # Email configuration
    SENDER_EMAIL = "smartcampus.fjwu@gmail.com"
    SENDER_PASSWORD = "qjxm mlun ugzw ijvr"  # App-specific password for Gmail
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    @staticmethod
    def send_approval_email(booking, user):
        """
        Send email notification for booking approval
        
        Args:
            booking: Booking object with details
            user: User object with email address
        """
        try:
            if not user.email:
                print(f"Warning: User {user.username} has no email address")
                return False
            
            subject = f"Booking Approved - {booking.course_name}"
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Segoe UI, Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                        <h2 style="color: #059669; text-align: center;">Booking Approval Notification</h2>
                        
                        <p>Dear <strong>{user.fullname}</strong>,</p>
                        
                        <p>Your classroom booking request has been <span style="color: #059669; font-weight: bold;">APPROVED</span>.</p>
                        
                        <div style="background-color: #f0f9f7; padding: 20px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="color: #059669; margin-top: 0;">Booking Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 40%;">Booking ID:</td>
                                    <td style="padding: 8px;">{booking.id}</td>
                                </tr>
                                <tr style="background-color: #e8f5f2;">
                                    <td style="padding: 8px; font-weight: bold;">Course Name:</td>
                                    <td style="padding: 8px;">{booking.course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Date:</td>
                                    <td style="padding: 8px;">{booking.booking_date}</td>
                                </tr>
                                <tr style="background-color: #e8f5f2;">
                                    <td style="padding: 8px; font-weight: bold;">Start Time:</td>
                                    <td style="padding: 8px;">{booking.start_time}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">End Time:</td>
                                    <td style="padding: 8px;">{booking.end_time}</td>
                                </tr>
                                <tr style="background-color: #e8f5f2;">
                                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                                    <td style="padding: 8px; color: #059669; font-weight: bold;">✓ Approved</td>
                                </tr>
                            </table>
                        </div>
                        
                        <p>Your classroom has been reserved for your course. Please ensure you arrive 10 minutes early.</p>
                        
                        <p style="color: #666; font-size: 14px;">
                            <strong>Need assistance?</strong><br>
                            Contact us at: <strong>hajrasarwar11@gmail.com</strong><br>
                            Phone: <strong>03273456789</strong>
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            Fatima Jinnah Women University<br>
                            Smart Campus Resource Management System<br>
                            Sent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailNotificationService._send_email(user.email, subject, html_body)
            
        except Exception as e:
            print(f"Error sending approval email: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def send_rejection_email(booking, user, reason=""):
        """
        Send email notification for booking rejection
        
        Args:
            booking: Booking object with details
            user: User object with email address
            reason: Reason for rejection (optional)
        """
        try:
            if not user.email:
                print(f"Warning: User {user.username} has no email address")
                return False
            
            subject = f"Booking Rejected - {booking.course_name}"
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Segoe UI, Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                        <h2 style="color: #DC2626; text-align: center;">Booking Rejection Notification</h2>
                        
                        <p>Dear <strong>{user.fullname}</strong>,</p>
                        
                        <p>Unfortunately, your classroom booking request has been <span style="color: #DC2626; font-weight: bold;">REJECTED</span>.</p>
                        
                        <div style="background-color: #fef2f2; padding: 20px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="color: #DC2626; margin-top: 0;">Booking Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 40%;">Booking ID:</td>
                                    <td style="padding: 8px;">{booking.id}</td>
                                </tr>
                                <tr style="background-color: #fee2e2;">
                                    <td style="padding: 8px; font-weight: bold;">Course Name:</td>
                                    <td style="padding: 8px;">{booking.course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Date:</td>
                                    <td style="padding: 8px;">{booking.booking_date}</td>
                                </tr>
                                <tr style="background-color: #fee2e2;">
                                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                                    <td style="padding: 8px; color: #DC2626; font-weight: bold;">✗ Rejected</td>
                                </tr>
                            </table>
                        </div>
                        
                        {f'<div style="background-color: #fef3c7; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #F59E0B;"><strong>Reason:</strong> {reason}</div>' if reason else ''}
                        
                        <p>Please contact the administration office to discuss alternative time slots or classrooms that may be available for your course.</p>
                        
                        <p style="color: #666; font-size: 14px;">
                            <strong>Need assistance?</strong><br>
                            Contact us at: <strong>hajrasarwar11@gmail.com</strong><br>
                            Phone: <strong>03273456789</strong>
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            Fatima Jinnah Women University<br>
                            Smart Campus Resource Management System<br>
                            Sent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailNotificationService._send_email(user.email, subject, html_body)
            
        except Exception as e:
            print(f"Error sending rejection email: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def send_admin_notification_new_booking(booking, user, classroom):
        """
        Send email notification to admin for new booking request awaiting approval
        
        Args:
            booking: Booking object with details
            user: User object who made the request
            classroom: Classroom object for the requested room
        """
        try:
            admin_email = "hajrasarwar11@gmail.com"  # Admin email
            subject = f"New Booking Request - {booking.course_name} (Booking ID: {booking.id})"
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Segoe UI, Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                        <h2 style="color: #0EA5E9; text-align: center;">New Booking Request</h2>
                        
                        <p>Dear <strong>Administrator</strong>,</p>
                        
                        <p>A new classroom booking request has been submitted and is <span style="color: #F59E0B; font-weight: bold;">PENDING APPROVAL</span>.</p>
                        
                        <div style="background-color: #f0f7ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="color: #0EA5E9; margin-top: 0;">Request Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 40%;">Booking ID:</td>
                                    <td style="padding: 8px; background-color: #e0f2fe;">{booking.id}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Requested By:</td>
                                    <td style="padding: 8px;">{user.fullname} ({user.username})</td>
                                </tr>
                                <tr style="background-color: #e0f2fe;">
                                    <td style="padding: 8px; font-weight: bold;">Email:</td>
                                    <td style="padding: 8px;">{user.email}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Phone:</td>
                                    <td style="padding: 8px;">{user.phone if user.phone else 'N/A'}</td>
                                </tr>
                                <tr style="background-color: #e0f2fe;">
                                    <td style="padding: 8px; font-weight: bold;">Course Name:</td>
                                    <td style="padding: 8px;">{booking.course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Classroom:</td>
                                    <td style="padding: 8px;">Room {classroom.room_number} ({classroom.classroom_type})</td>
                                </tr>
                                <tr style="background-color: #e0f2fe;">
                                    <td style="padding: 8px; font-weight: bold;">Building:</td>
                                    <td style="padding: 8px;">{classroom.building}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Capacity:</td>
                                    <td style="padding: 8px;">{classroom.capacity} students</td>
                                </tr>
                                <tr style="background-color: #e0f2fe;">
                                    <td style="padding: 8px; font-weight: bold;">Date:</td>
                                    <td style="padding: 8px;">{booking.booking_date}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Time Slot:</td>
                                    <td style="padding: 8px;">{booking.start_time} - {booking.end_time}</td>
                                </tr>
                                <tr style="background-color: #e0f2fe;">
                                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                                    <td style="padding: 8px; color: #F59E0B; font-weight: bold;">⏳ Pending Approval</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #fef3c7; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #F59E0B;">
                            <p style="margin: 0;"><strong>Action Required:</strong> Please review this booking request in the Admin Dashboard and either approve or reject it.</p>
                        </div>
                        
                        <p style="color: #666; font-size: 14px;">
                            <strong>Quick Links:</strong><br>
                            • Admin Dashboard: Smart Campus System<br>
                            • Go to: Bookings Tab → Edit Request
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            Fatima Jinnah Women University<br>
                            Smart Campus Resource Management System<br>
                            Sent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailNotificationService._send_email(admin_email, subject, html_body)
            
        except Exception as e:
            print(f"Error sending admin notification: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def send_cancellation_email(booking, user, reason=""):
        """
        Send email notification for booking cancellation
        
        Args:
            booking: Booking object with details
            user: User object with email address
            reason: Reason for cancellation (optional)
        """
        try:
            if not user.email:
                print(f"Warning: User {user.username} has no email address")
                return False
            
            subject = f"Booking Cancelled - {booking.course_name}"
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body style="font-family: Segoe UI, Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                        <h2 style="color: #7C3AED; text-align: center;">Booking Cancellation Notification</h2>
                        
                        <p>Dear <strong>{user.fullname}</strong>,</p>
                        
                        <p>Your classroom booking has been <span style="color: #7C3AED; font-weight: bold;">CANCELLED</span>.</p>
                        
                        <div style="background-color: #f3e8ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="color: #7C3AED; margin-top: 0;">Booking Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 40%;">Booking ID:</td>
                                    <td style="padding: 8px;">{booking.id}</td>
                                </tr>
                                <tr style="background-color: #ede9fe;">
                                    <td style="padding: 8px; font-weight: bold;">Course Name:</td>
                                    <td style="padding: 8px;">{booking.course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">Date:</td>
                                    <td style="padding: 8px;">{booking.booking_date}</td>
                                </tr>
                                <tr style="background-color: #ede9fe;">
                                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                                    <td style="padding: 8px; color: #7C3AED; font-weight: bold;">✗ Cancelled</td>
                                </tr>
                            </table>
                        </div>
                        
                        {f'<div style="background-color: #fef3c7; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #F59E0B;"><strong>Reason:</strong> {reason}</div>' if reason else ''}
                        
                        <p style="color: #666; font-size: 14px;">
                            <strong>Need assistance?</strong><br>
                            Contact us at: <strong>hajrasarwar11@gmail.com</strong><br>
                            Phone: <strong>03273456789</strong>
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            Fatima Jinnah Women University<br>
                            Smart Campus Resource Management System<br>
                            Sent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailNotificationService._send_email(user.email, subject, html_body)
            
        except Exception as e:
            print(f"Error sending cancellation email: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def _send_email(recipient_email, subject, html_body):
        """
        Internal method to send email via Gmail SMTP
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            html_body: Email body in HTML format
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = EmailNotificationService.SENDER_EMAIL
            message["To"] = recipient_email
            
            # Attach HTML part
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email via Gmail SMTP
            with smtplib.SMTP(EmailNotificationService.SMTP_SERVER, EmailNotificationService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailNotificationService.SENDER_EMAIL, EmailNotificationService.SENDER_PASSWORD)
                server.sendmail(EmailNotificationService.SENDER_EMAIL, recipient_email, message.as_string())
            
            print(f"✓ Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email to {recipient_email}: {e}")
            import traceback
            traceback.print_exc()
            return False
