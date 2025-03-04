"""
This module provides email sending functionality for the Flask application.

Functions:
- send_email(recipient_email, msg): Sends an email using SMTP.
"""

import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch email credentials from environment variables
email_user = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASSWORD")

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