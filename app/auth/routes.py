"""
This module defines the routes for authentication-related functionalities in the Flask application.

It includes the following routes:
- User login
- User registration
- User logout

Functions:
- login(): Handles user login.
- register(): Handles user registration.
- logout(): Logs out the current user.
"""

from flask import current_app,  render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.models import db, User, Vet, Farmer
from app.utils import allowed_file
import os

from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to handle user login.

    GET: Renders the login form.
    POST: Processes the login form and logs in the user.

    Returns:
        Response: Rendered HTML template for the login page or redirects to the appropriate profile page.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not email or not password:
            flash('Please fill in all fields', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        # Check if the user exists and the password is correct
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login the user
        login_user(user)
        flash('Login successful!', 'success')
        
        # Redirect based on role
        if user.user_role == 'farmer':
            return redirect(url_for('farmer.farmer_profile'))
        elif user.user_role == 'vet':
            return redirect(url_for('vet.vet_profile'))
        
        return redirect(url_for('auth.login'))
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    """
    Route to handle user registration.

    GET: Renders the registration form.
    POST: Processes the registration form and registers the user.

    Returns:
        Response: Rendered HTML template for the registration page or redirects to the login page.
    """
    if request.method == 'POST':
        # Get common data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        user_role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        errors = []
        if not all ([full_name, email, phone, user_role, password, confirm_password]):
            errors.append('All required fields must be filled')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if user_role not in ['farmer', 'vet']:
            errors.append('Invalid user role')
            
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('auth.register'))
            if User.query.filter_by(phone=phone).first():
                flash('Phone number already registered', 'danger')
                return redirect(url_for('auth.register'))

            # Create new user
            new_user = User(
                full_name = full_name,
                email = email,
                phone = phone,
                user_role = user_role
            )
            new_user.set_password(password)

            # Handling form-specific data
            if user_role == 'farmer':
                farmer = Farmer(
                    farm_name = request.form.get('farm_name'),
                    farm_location = request.form.get('farm_location')
                )
                new_user.farmer_profile = farmer
            elif user_role == 'vet':
                # Handle file upload
                if 'verification_documents' not in request.files:
                    flash('No verification document uploaded', 'danger')
                    return redirect(url_for('auth.register'))
                
                file = request.files['verification_documents']
                if file.filename == '':
                    flash('No selected file', 'danger')
                    return redirect(url_for('auth.register'))
                
                if file and allowed_file(file.filename):
                    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                else:
                    flash('Invalid file type', 'danger')
                    return redirect(url_for('auth.register'))

                vet = Vet(
                    specialization = request.form.get('specialization'),
                    years_experience = request.form.get('years_experience'),
                    verification_document_path = file_path,
                    clinic_name = request.form.get('clinic_name'),
                    service_area = request.form.get('service_area')
                )
                new_user.vet_profile = vet
        
            # Save to database
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            flash('Registration successful!', 'success')
            
            if user_role == 'farmer':
                return redirect(url_for('farmer.farmer_profile'))
            elif user_role == 'vet':
                return redirect(url_for('vet.vet_profile'))
                    
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    # GET request - show registration form 
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Route to log out the current user.

    Returns:
        Response: Redirects to the login page with a success message.
    """
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))