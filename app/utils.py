"""
This module provides utility functions for the Flask application.

Functions:
- allowed_file(filename): Checks if a file is allowed based on its extension.
- send_email(recipient_email, msg): Sends an email using SMTP.
"""

import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch email credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

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
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, recipient_email, msg=msg)
        server.quit()
    except smtplib.SMTPException as e:
        print('Error sending email: {}'.format(e))
    except Exception as e:
        print('Error: {}'.format(e))
        

KENYA_COUNTIES = [
    ('', 'Select County'),  # Default option
    ('baringo', 'Baringo'),
    ('bomet', 'Bomet'),
    ('bungoma', 'Bungoma'),
    ('busia', 'Busia'),
    ('elgeyo_marakwet', 'Elgeyo Marakwet'),
    ('embu', 'Embu'),
    ('garissa', 'Garissa'),
    ('homa_bay', 'Homa Bay'),
    ('isiolo', 'Isiolo'),
    ('kajiado', 'Kajiado'),
    ('kakamega', 'Kakamega'),
    ('kericho', 'Kericho'),
    ('kiambu', 'Kiambu'),
    ('kilifi', 'Kilifi'),
    ('kirinyaga', 'Kirinyaga'),
    ('kisii', 'Kisii'),
    ('kisumu', 'Kisumu'),
    ('kitui', 'Kitui'),
    ('kwale', 'Kwale'),
    ('laikipia', 'Laikipia'),
    ('lamu', 'Lamu'),
    ('machakos', 'Machakos'),
    ('makueni', 'Makueni'),
    ('mandera', 'Mandera'),
    ('marsabit', 'Marsabit'),
    ('meru', 'Meru'),
    ('migori', 'Migori'),
    ('mungoma', 'Mungoma'),
    ('murang_a', 'Murang’a'),
    ('nairobi', 'Nairobi'),
    ('nakuru', 'Nakuru'),
    ('nandi', 'Nandi'),
    ('narok', 'Narok'),
    ('nyamira', 'Nyamira'),
    ('nyandarua', 'Nyandarua'),
    ('nyeri', 'Nyeri'),
    ('samburu', 'Samburu'),
    ('siaya', 'Siaya'),
    ('taita_taveta', 'Taita Taveta'),
    ('tana_river', 'Tana River'),
    ('tharaka_nithi', 'Tharaka Nithi'),
    ('trans_nzoia', 'Trans Nzoia'),
    ('turkana', 'Turkana'),
    ('uasin_gishu', 'Uasin Gishu'),
    ('vihiga', 'Vihiga'),
    ('wajir', 'Wajir'),
    ('west_pokot', 'West Pokot')
]
