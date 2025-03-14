"""
This module defines the database models for the Flask application.

It includes the following models:
- User: Represents a user in the system.
- Farmer: Represents a farmer profile.
- Vet: Represents a vet profile.
- Admin: Represents an admin user in the system.
- Location: Represents a location.
- Livestock: Represents livestock data.
- LivestockHealth: Represents livestock health data.
- VetAvailability: Represents the availability slots for vets.
- Appointment: Represents appointments between farmers and vets.

Each model includes fields, relationships, and methods relevant to its purpose.
"""

from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        phone (str): The phone number of the user.
        password_hash (str): The hashed password of the user.
        profile_picture (str): The path to the user's profile picture.
        otp_secret (str): Secret key for two-factor authentication.
        email_verified (bool): Indicates if the user's email is verified.
        profile_picture (str): The path to the user's profile picture.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
        farmer_profile (relationship): One-to-one relationship with the Farmer profile.
        vet_profile (relationship): One-to-one relationship with the Vet profile.
        admin_profile (relationship): One-to-one relationship with the Admin profile.
        location (relationship): One-to-one relationship with the Location.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    otp_secret = db.Column(db.String(32), nullable=True) # Secret key for two-factor authentication
    email_verified = db.Column(db.Boolean, default=False) # Indicates if the user's email is verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer_profile = db.relationship('Farmer', backref='user', uselist=False, cascade='all, delete-orphan')
    vet_profile = db.relationship('Vet', backref='user', uselist=False, cascade='all, delete-orphan')
    admin_profile = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')
    location = db.relationship('Location', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Sets the password for the user.

        Args:
            password (str): The password to set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored password hash.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Admin(db.Model):
    """
    Represents an admin user in the
    
    Attributes:
        id (int): The unique identifier for the admin.
        user_id (int): The ID of the associated user.
        role (Enum): The role of the admin (super, moderator).
        permissions (json): The permissions of the admin.
    """
    
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    role = db.Column(db.Enum('super', 'moderator', name='admin_roles'), nullable=False)
    permissions = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<Admin {self.id}>'


class Farmer(db.Model):
    """
    Represents a farmer profile.

    Attributes:
        id (int): The unique identifier for the farmer profile.
        user_id (int): The ID of the associated user.
        farm_name (str): The name of the farm.
        livestock_type (str): The type of livestock on the farm.
        animal_count (int): The number of animals on the farm.
        alert_preference (str): The preferred method of receiving alerts.
        preferred_language (str): The preferred language for communication.
    """

    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    farm_name = db.Column(db.String(255))
    livestock_type = db.Column(db.String(255), nullable=False)
    animal_count = db.Column(db.Integer, nullable=False, default=0)
    alert_preference = db.Column(db.Enum('email', 'sms', 'whatsapp' , 'app', name='alert_preferences'), nullable=False, default='app')
    preferred_language = db.Column(db.String(255), nullable=False, default='English')
    
    # Relationships
    livestock = db.relationship('Livestock', backref='farmer', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Farmer {self.farm_name}>'


class Vet(db.Model):
    """
    Represents a vet profile.

    Attributes:
        id (int): The unique identifier for the vet profile.
        user_id (int): The ID of the associated user.
        license_number (str): The license number of the vet.
        experience_years (int): The number of years of experience the vet has.
        specialization (str): The specialization of the vet.
        verification_document_path (str): The path to the verification document.
        clinic_name (str): The name of the clinic.
        avg_rating (float): The average rating of the vet.
        is_verified (bool): Indicates if the vet is verified.
    """

    __tablename__ = 'vets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    license_number = db.Column(db.String(255), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False, default=0)
    specialization = db.Column(db.String(255), nullable=False)
    verification_document_path = db.Column(db.String(255), nullable=False)
    clinic_name = db.Column(db.String(255), nullable=True)
    avg_rating = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Vet {self.specialization}>'
    

class Location(db.Model):
    """
    Represents a location.

    Attributes:
        id (int): The unique identifier for the location.
        user_id (int): The ID of the associated user.
        county (str): The county of the location.
        town (str): The town of the location.
    """

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    county = db.Column(db.String(255), nullable=False)
    town = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Location {self.county} - {self.town}>'
    

class Livestock(db.Model):
    """
    Represents livestock data.

    Attributes:
        id (int): The unique identifier for the livestock.
        farmer_id (int): The ID of the associated farmer.
        name (str): The name of the livestock.
        age (int): The age of the livestock.
        breed (str): The breed of the livestock.
        created_at (datetime): The timestamp when the livestock was created.
    """
    
    __tablename__ = 'livestock'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    health_data = db.relationship('LivestockHealth', backref='livestock', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='livestock', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Livestock {self.name}>'


class LivestockHealth(db.Model):
    """
    Represents livestock health data.

    Attributes:
        id (int): The unique identifier for the health data.
        farmer_id (int): The ID of the associated farmer.
        livestock_id (int): The ID of the associated livestock.
        temperature (float): The temperature of the livestock.
        pulse (int): The pulse rate of the livestock.
        created_at (datetime): The timestamp when the health data was created.
        updated_at (datetime): The timestamp when the health data was last updated.
    """
    
    __tablename__ = 'livestock_health'
    
    id = db.Column(db.Integer, primary_key=True)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestock.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pulse = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LivestockHealth {self.id}>'


class VetAvailability(db.Model):
    """
    Represents the availability slots for vets.

    Attributes:
        id (int): The unique identifier for the availability slot.
        vet_id (int): The ID of the associated vet.
        start_time (datetime): The start time of the availability slot.
        end_time (datetime): The end time of the availability slot.
        is_booked (bool): Indicates if the slot is booked.
        created_at (datetime): The timestamp when the slot was created.
    """

    __tablename__ = 'vet_availability'

    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, nullable=False)
    available_days = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vet = db.relationship('User', backref='availability_slots')

    def __repr__(self):
        return f'<Availability {self.start_time} to {self.end_time}>'


class Appointment(db.Model):
    """
    Represents appointments between farmers and vets.

    Attributes:
        id (int): The unique identifier for the appointment.
        farmer_id (int): The ID of the associated farmer.
        vet_id (int): The ID of the associated vet.
        slot_id (int): The ID of the associated availability slot.
        livestock_id (int): The ID of the associated livestock.
        notes (str): Additional notes for the appointment.
        status (str): The status of the appointment (pending, confirmed, completed, cancelled).
        created_at (datetime): The timestamp when the appointment was created.
    """

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('vet_availability.id'), nullable=False)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestock.id'), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='farmer_appointments')
    vet = db.relationship('User', foreign_keys=[vet_id], backref='vet_appointments')
    slot = db.relationship('VetAvailability', backref='appointment')

    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'