import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

class EmailService:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        # For development, we'll use a mock email service
        # In production, these would be configured with real SMTP settings
        self.smtp_server = smtp_server or "smtp.gmail.com"
        self.smtp_port = smtp_port or 587
        self.username = username or "noreply@statebd.org"
        self.password = password or "app_password"
        self.from_email = "noreply@statebd.org"
        self.from_name = "State Bangladesh Society"
    
    def send_application_confirmation(self, application, pdf_bytes=None):
        """Send application confirmation email with PDF attachment"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = application.email
            msg['Subject'] = f"Application Confirmation - {application.reference_number}"
            
            # Email body
            body = self.create_confirmation_email_body(application)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach PDF if provided
            if pdf_bytes:
                pdf_attachment = MIMEApplication(pdf_bytes, _subtype='pdf')
                pdf_attachment.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=f'Application_{application.reference_number}.pdf'
                )
                msg.attach(pdf_attachment)
            
            # For development, we'll just log the email instead of sending
            self.log_email(msg, application.email)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def create_confirmation_email_body(self, application):
        """Create HTML email body for application confirmation"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c5530; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .info-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .info-table th, .info-table td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                .info-table th {{ background: #f2f2f2; font-weight: bold; }}
                .footer {{ background: #2c5530; color: white; padding: 15px; text-align: center; font-size: 12px; }}
                .status {{ background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>State Bangladesh Society</h1>
                    <p>Application Confirmation</p>
                </div>
                
                <div class="content">
                    <h2>Dear {application.full_name},</h2>
                    
                    <p>Thank you for submitting your application to State Bangladesh Society. We have successfully received your application and it is currently being processed.</p>
                    
                    <h3>Application Details:</h3>
                    <table class="info-table">
                        <tr>
                            <th>Reference Number</th>
                            <td>{application.reference_number}</td>
                        </tr>
                        <tr>
                            <th>Category</th>
                            <td>{application.category.name}</td>
                        </tr>
                        <tr>
                            <th>Submission Date</th>
                            <td>{application.created_at.strftime('%B %d, %Y at %I:%M %p')}</td>
                        </tr>
                        <tr>
                            <th>Current Status</th>
                            <td><span class="status">{application.status}</span></td>
                        </tr>
                    </table>
                    
                    <h3>What's Next?</h3>
                    <ul>
                        <li>Your application will be reviewed by our team</li>
                        <li>You will receive updates via email as your application progresses</li>
                        <li>You can track your application status using your reference number: <strong>{application.reference_number}</strong></li>
                        <li>If approved, you will be contacted for further steps</li>
                    </ul>
                    
                    <h3>Important Information:</h3>
                    <ul>
                        <li>Please save your reference number: <strong>{application.reference_number}</strong></li>
                        <li>You can track your application status on our website</li>
                        <li>If you have any questions, please contact us with your reference number</li>
                        <li>The attached PDF contains your complete application details</li>
                    </ul>
                    
                    <p>Thank you for choosing State Bangladesh Society. We are committed to empowering communities through development projects and social initiatives.</p>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 State Bangladesh Society. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this email address.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def send_status_update(self, application, old_status, new_status):
        """Send status update email to applicant"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = application.email
            msg['Subject'] = f"Application Status Update - {application.reference_number}"
            
            # Email body
            body = self.create_status_update_email_body(application, old_status, new_status)
            msg.attach(MIMEText(body, 'html'))
            
            # For development, we'll just log the email instead of sending
            self.log_email(msg, application.email)
            
            return True
            
        except Exception as e:
            print(f"Error sending status update email: {str(e)}")
            return False
    
    def create_status_update_email_body(self, application, old_status, new_status):
        """Create HTML email body for status update"""
        status_colors = {
            'Pending': '#ffc107',
            'In Progress': '#17a2b8',
            'Approved': '#28a745',
            'Rejected': '#dc3545'
        }
        
        status_color = status_colors.get(new_status, '#6c757d')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c5530; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .status {{ background: {status_color}; color: white; padding: 8px 15px; border-radius: 5px; display: inline-block; font-weight: bold; }}
                .info-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .info-table th, .info-table td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                .info-table th {{ background: #f2f2f2; font-weight: bold; }}
                .footer {{ background: #2c5530; color: white; padding: 15px; text-align: center; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>State Bangladesh Society</h1>
                    <p>Application Status Update</p>
                </div>
                
                <div class="content">
                    <h2>Dear {application.full_name},</h2>
                    
                    <p>We are writing to inform you that the status of your application has been updated.</p>
                    
                    <table class="info-table">
                        <tr>
                            <th>Reference Number</th>
                            <td>{application.reference_number}</td>
                        </tr>
                        <tr>
                            <th>Category</th>
                            <td>{application.category.name}</td>
                        </tr>
                        <tr>
                            <th>Previous Status</th>
                            <td>{old_status}</td>
                        </tr>
                        <tr>
                            <th>Current Status</th>
                            <td><span class="status">{new_status}</span></td>
                        </tr>
                        <tr>
                            <th>Updated On</th>
                            <td>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
                        </tr>
                    </table>
                    
                    <p>You can continue to track your application status on our website using your reference number.</p>
                    
                    <p>If you have any questions about this update, please contact us with your reference number.</p>
                    
                    <p>Thank you for your patience.</p>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 State Bangladesh Society. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this email address.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def log_email(self, msg, recipient):
        """Log email for development purposes"""
        print(f"📧 EMAIL SENT (Development Mode)")
        print(f"To: {recipient}")
        print(f"Subject: {msg['Subject']}")
        print(f"From: {msg['From']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
    
    def send_real_email(self, msg):
        """Send real email (for production use)"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.from_email, msg['To'], text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending real email: {str(e)}")
            return False

