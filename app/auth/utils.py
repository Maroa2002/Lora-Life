from flask import flash, current_app, url_for
from flask_login import login_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail
from app.models import User, Location, Farmer, Vet
from app.utils import save_file
import pyotp

def register_user(form, role):
    print('Registering user...')
    
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    phone = form.phone.data
    county = form.county.data
    town = form.town.data
    password = form.password.data
    confirm_password = form.confirm_password.data
    profile_picture = form.profile_picture.data
    
    print(f"Received data: {first_name}, {last_name}, {email}, {phone}, {county}, {town}, {password}, {confirm_password}, {profile_picture}")
    
    # Check if password and confirm password match
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        print('Passwords do not match!')
        return None
    
    # Check if user already exists
    if User.query.filter((User.email == email) | (User.phone == phone)).first():
        flash('Email or phone number already exists!', 'danger')
        print('Email or phone number already exists!')
        return None
    
    try:
        # Save profile picture
        profile_pic_folder = current_app.config.get('PROFILE_PIC_FOLDER', 'static/uploads/profile_pics')
        profile_pic_path = save_file(profile_picture, profile_pic_folder) if profile_picture else None
        
        otp_secret = pyotp.random_base32() # Generate a random  OTP secret key
        
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            user_role = role,
            profile_picture = profile_pic_path,
            otp_secret = otp_secret,
            # email_verified = False
        )
        new_user.set_password(password)
        
        print('User:', new_user)
        
        # Set location
        location = Location(county=county, town=town)
        new_user.location = location
        
        # Role-specific details
        if role == 'farmer':
            farmer = Farmer(
                farm_name = form.farm_name.data,
                livestock_type = form.livestock_type.data,
                animal_count = form.animal_count.data,
                alert_preference = form.alert_preference.data,
                preferred_language = form.preferred_language.data
            )
            new_user.farmer_profile = farmer
            print('Farmer:', farmer)
        elif role == 'vet':
            verification_folder = current_app.config.get('VERIFICATION_FOLDER', 'static/uploads/verification')
            verification_doc_path = save_file(form.verification_document.data, verification_folder)
            
            vet = Vet(
                license_number = form.license_number.data,
                experience_years = form.experience_years.data,
                specialization = form.specialization.data,
                verification_document_path = verification_doc_path,
                clinic_name = form.clinic_name.data
            )
            new_user.vet_profile = vet
            print('Vet:', vet)
            
        db.session.add(new_user)
        db.session.commit()
        print('User added successfully!')
        
        # login_user(new_user)
        flash('Account created successfully!', 'success')
        return new_user
    
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
        print('Error:', e)
        return None

def get_serializer():
    """
    Get URLSafeTimedSerializer object for email confirmation.
    
    Returns:
        URLSafeTimedSerializer: Serializer object.
    """
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_confirmation_token(email):
    """
    Generate a token for email confirmation.
    
    Args:
        email (str): User's email address.
    
    Returns:
        str: Token for email confirmation.
    """
    s = get_serializer()
    
    token = s.dumps(email, salt='email-confirm')
    
    return token

def send_verification_email(user):
    """
    Send an email to verify the user's email address.
    
    Args:
        user (User): User object.
    """
    token = generate_confirmation_token(user.email)
    
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    
    msg = Message('Confirm Your Email Address', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'Click the link below to verify your email address:\n{verify_url}'
    
    try:
        mail.send(msg)
        flash('A verification email has been sent to your email address.', 'info')
    except Exception as e:
        flash('An error occurred sending the verification email.', 'danger')
        print('Error:', e)

def verify_email_token(token):
    """
    Verify the email confirmation token.
    
    Args:
        token (str): Token to verify.
    
    Returns:
        str: Email address if the token is valid, None otherwise.
    """
    s = get_serializer()
    
    try:
        email = s.loads(token, salt='email-confirm', max_age=86400)
    except:
        return False
    return email