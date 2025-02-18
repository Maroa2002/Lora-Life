from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Farmer(db.Model):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    farm_name = db.Column(db.String(255))
    farm_location = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Farmer {self.farm_name}>'


class Vet(db.Model):
    __tablename__ = 'vets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    years_experience = db.Column(db.Integer, nullable=False)
    verification_document_path = db.Column(db.String(255), nullable=False)
    clinic_name = db.Column(db.String(255))
    service_area = db.Column(db.Text, nullable=False)
    is_verifed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Vet {self.specialization}>'
    