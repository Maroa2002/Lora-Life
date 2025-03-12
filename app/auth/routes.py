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

from flask import current_app,  render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
import pyotp
from werkzeug.utils import secure_filename
from app.models import db, User, Vet, Farmer, Location
from app.utils import allowed_file
from .forms import RoleSelectForm, FarmerRegistrationForm, VetRegistrationForm, LoginForm, OTPForm
from app.utils import COUNTY_TOWNS
from .utils import register_user
from app import mail

from . import auth_bp

@auth_bp.route('/register/select-role', methods=['GET', 'POST'])
def select_role():
    """
    Route to handle selection of user role during registration.

    GET: Renders the role selection form.
    POST: Processes the role selection form and redirects to the appropriate registration form.

    Returns:
        Response: Rendered HTML template for the role selection page or redirects to the registration page.
    """
    form = RoleSelectForm()
    if form.validate_on_submit():
        user_role = form.user_role.data
        if user_role == 'farmer':
            return redirect(url_for('auth.register_farmer'))
        elif user_role == 'vet':
            return redirect(url_for('auth.register_vet'))
        elif user_role == 'admin':
            return redirect(url_for('auth.register_admin'))
    
    return render_template('select_role.html', form=form)

@auth_bp.route('/register/farmer', methods=['POST', 'GET'])
def register_farmer():
    """
    Route to handle farmer registration.

    GET: Renders the registration form.
    POST: Processes the registration form and registers the user.

    Returns:
        Response: Rendered HTML template for the registration page or redirects to the login page.
    """
    form = FarmerRegistrationForm()
    
    # Get the selected county from the request(for both POST and GET requests)
    selected_county = request.form.get('county') or request.args.get('county')
    # Set the town choices based on the selected county
    if selected_county and selected_county in COUNTY_TOWNS:
        form.town.choices = [(town, town) for town in COUNTY_TOWNS[selected_county]]
    else:
        form.town.choices = [('', 'Select a Town')]
    
    if form.validate_on_submit():
        print('Form validated successfully')
        user = register_user(form, 'farmer')
        if user:
            print('User created successfully', user)
            return redirect(url_for('farmer.farmer_profile'))
        else:
            print('User not created')
    else:
        print('Form validation failed', form.errors)
    
    return render_template('register_farmer.html', form=form)

@auth_bp.route('/register/vet', methods=['POST', 'GET'])
def register_vet():
    """
    Route to handle vet registration.

    GET: Renders the registration form.
    POST: Processes the registration form and registers the user.

    Returns:
        Response: Rendered HTML template for the registration page or redirects to the login page.
    """
    form = VetRegistrationForm()
    
    # Get the selected county from the request(for both POST and GET requests)
    selected_county = request.form.get('county') or request.args.get('county')
    # Set the town choices based on the selected county
    if selected_county and selected_county in COUNTY_TOWNS:
        form.town.choices = [(town, town) for town in COUNTY_TOWNS[selected_county]]
    else:
        form.town.choices = [('', 'Select a Town')]
    
    if form.validate_on_submit():
        print('Form validated successfully')
        user = register_user(form, 'vet')
        if user:
            print('User created successfully', user)
            return redirect(url_for('vet.vet_profile'))
    else:
        print('Form validation failed', form.errors)
    
    return render_template('register_vet.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to handle user login.

    GET: Renders the login form.
    POST: Processes the login form and logs in the user.

    Returns:
        Response: Rendered HTML template for the login page or redirects to the appropriate profile page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        print('Form validated successfully')
        email = form.email.data
        password = form.password.data
        
        if not email or not password:
            flash('Please fill in all fields', 'warning')
            print('Please fill in all fields')
            return redirect(url_for('auth.login_user'))
        
        user = User.query.filter(User.email == email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            print('Invalid email or password')
            return redirect(url_for('auth.login'))
        
        session['email'] = email # Store the email in the session
        
        # Generate 6-digit OTP
        otp = pyotp.TOTP(user.otp_secret).now()
        print('OTP:', otp)
        
        # Send OTP to user's email
        msg = Message('Your 2FA Code', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your One-Time password (OTP) is: {otp}'
        mail.send(msg)
        
        flash('A 6-digit OTP has been sent to your email', 'info')
        return redirect(url_for('auth.verify_otp'))
    else:
        print('Form validation failed', form.errors)
    
    return render_template('user_login.html', form=form) 

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """
    Route to handle OTP verification.

    GET: Renders the OTP verification form.
    POST: Processes the OTP verification form and logs in the user.

    Returns:
        Response: Rendered HTML template for the OTP verification page or redirects to the appropriate profile page.
    """
    if 'email' not in session:
        flash('Unauthorized access', 'warning')
        return redirect(url_for('auth.login'))
    
    form = OTPForm()
    if form.validate_on_submit():
        print('Form validated successfully')
        otp = form.otp.data
        
        user = User.query.filter(User.email == session['email']).first()

        if user:
            print(f'Stored OTP secret: {user.otp_secret}')
            print(f'Entered OTP: {otp}')
            print(f'Generated OTP: {pyotp.TOTP(user.otp_secret).now()}')

            if pyotp.TOTP(user.otp_secret).verify(otp, valid_window=1):
                session['user_id'] = user.id # Store the user ID in the session
                print(f'Logged in user: {user.email}')
                login_user(user)
                print('Logged in successfully')
                flash('You have successfully logged in', 'success')
                
                print(f'User role: {user.user_role}')
                
                if user.user_role == 'farmer':
                    return redirect(url_for('farmer.farmer_profile'))
                elif user.user_role == 'vet':
                    return redirect(url_for('vet.vet_profile'))
                elif user.user_role == 'admin':
                    return redirect(url_for('admin.admin_profile'))
                
                flash('Invalid user role', 'danger')
                return redirect(url_for('auth.login'))
            
            else:
                flash('Invalid OTP', 'danger')
                print('OTP verification failed')
    else:
        print('Form validation failed', form.errors)
        
    return render_template('verify_otp.html', form=form)  

@auth_bp.route('/get_towns', methods=['GET'])
def get_towns():
    """
    Route to get towns based on the selected county.

    POST: Processes the county selected and returns the towns in that county.

    Returns:
        Response: JSON object with the towns in the selected county.
    """
    county = request.args.get('county')
    towns = COUNTY_TOWNS.get(county)
    return jsonify({'towns': towns})
    
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