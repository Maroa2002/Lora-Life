from flask import flash, current_app
from flask_login import login_user
from app import db
from app.models import User, Location, Farmer, Vet
from app.utils import save_file

def register_user(form, role):
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    phone = form.phone.data
    county = form.county.data
    town = form.town.data
    password = form.password.data
    confirm_password = form.confirm_password.data
    profile_picture = form.profile_picture.data
    
    # Check if password and confirm password match
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return None
    
    # Check if user already exists
    if User.query.filter((User.email == email) | (User.phone == phone)).first():
        flash('Email or phone number already exists!', 'danger')
        return None
    
    try:
        # Save profile picture
        profile_pic_folder = current_app.config.get('PROFILE_PIC_FOLDER', 'static/uploads/profile_pics')
        profile_pic_path = save_file(profile_picture, profile_pic_folder) if profile_picture else None
        
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            user_role = role,
            profile_picture = profile_pic_path
        )
        new_user.set_password(password)
        
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
            
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('Account created successfully!', 'success')
        return new_user
    
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
        return None