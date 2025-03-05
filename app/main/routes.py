"""
This module defines the main routes for the Flask application.

It includes the following routes:
- Home page
- Contact form submission

Functions:
- home(): Renders the home page.
- contact(): Handles the contact form submission and sends an email.
"""

from flask import render_template, request, redirect, url_for, flash
from app.utils import send_email
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')

from . import main_bp

@main_bp.route('/')
def home():
    """
    Route to render the home page.

    Returns:
        Response: Rendered HTML template for the home page.
    """
    return render_template('index.html')

@main_bp.route('/contact', methods=['POST'])
def contact():
    """
    Route to handle contact form submission.

    Processes the contact form data and sends an email with the provided information.

    Returns:
        Response: Redirects to the home page with a success message.
    """
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    message = request.form.get('message')
    
    msg = "Subject: Contact Us\n\n{}\n\n{}\n\n{}".format(user_name, user_email, message)
    
    send_email(EMAIL_USER, msg)
    flash('Message sent successfully', 'success')
    return redirect(url_for('main.home'))
