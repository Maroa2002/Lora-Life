"""
This module provides utility functions for the Flask application.

Functions:
- allowed_file(filename): Checks if a file is allowed based on its extension.
- send_email(recipient_email, msg): Sends an email using SMTP.
"""

import smtplib
import os

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """
    Check if a file is allowed based on its extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(recipient_email, msg):
    """
    Send an email using SMTP.

    Args:
        recipient_email (str): The email address of the recipient.
        msg (str): The message to send.

    Raises:
        smtplib.SMTPException: If there is an error sending the email.
        Exception: If there is a general error.
    """
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, recipient_email, msg=msg)
        server.quit()
    except smtplib.SMTPException as e:
        print('Error sending email: {}'.format(e))
    except Exception as e:
        print('Error: {}'.format(e))