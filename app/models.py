"""
This module defines the database models for the Flask application.

It includes the following models:
- User: Represents a user in the system.
- Farmer: Represents a farmer profile.
- Vet: Represents a vet profile.
- VetAvailability: Represents the availability slots for vets.
- Appointment: Represents appointments between farmers and vets.

Each model includes fields, relationships, and methods relevant to its purpose.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        full_name (str): The full name of the user.
        email (str): The email address of the user.
        phone (str): The phone number of the user.
        password_hash (str): The hashed password of the user.
        user_role (str): The role of the user (farmer or vet).
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
        farmer_profile (relationship): One-to-one relationship with the Farmer profile.
        vet_profile (relationship): One-to-one relationship with the Vet profile.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Enum('farmer', 'vet', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer_profile = db.relationship('Farmer', backref='user', uselist=False, cascade='all, delete-orphan')
    vet_profile = db.relationship('Vet', backref='user', uselist=False, cascade='all, delete-orphan')

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


class Farmer(db.Model):
    """
    Represents a farmer profile.

    Attributes:
        id (int): The unique identifier for the farmer profile.
        user_id (int): The ID of the associated user.
        farm_name (str): The name of the farm.
        farm_location (str): The location of the farm.
    """

    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    farm_name = db.Column(db.String(255))
    farm_location = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Farmer {self.farm_name}>'


class Vet(db.Model):
    """
    Represents a vet profile.

    Attributes:
        id (int): The unique identifier for the vet profile.
        user_id (int): The ID of the associated user.
        specialization (str): The specialization of the vet.
        years_experience (int): The number of years of experience the vet has.
        verification_document_path (str): The path to the verification document.
        clinic_name (str): The name of the clinic.
        service_area (str): The service area of the vet.
        is_verified (bool): Indicates if the vet is verified.
    """

    __tablename__ = 'vets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    years_experience = db.Column(db.Integer, nullable=False)
    verification_document_path = db.Column(db.String(255), nullable=False)
    clinic_name = db.Column(db.String(255))
    service_area = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Vet {self.specialization}>'


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
        notes (str): Additional notes for the appointment.
        status (str): The status of the appointment (pending, confirmed, completed, cancelled).
        created_at (datetime): The timestamp when the appointment was created.
    """

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('vet_availability.id'), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='farmer_appointments')
    vet = db.relationship('User', foreign_keys=[vet_id], backref='vet_appointments')
    slot = db.relationship('VetAvailability', backref='appointment')

    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'