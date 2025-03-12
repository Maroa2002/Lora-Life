"""
This module defines the forms used for authentication and registration in the Flask application.

It includes the following forms:
- RoleSelectForm: Form to select user role.
- BaseRegistrationForm: Base registration form for all user types.
- FarmerRegistrationForm: Registration form for farmers.
- VetRegistrationForm: Registration form for vets.
- LoginForm: Form for user login.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, StringField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, InputRequired, Regexp
from flask_wtf.file import FileAllowed, FileRequired
from app.utils import KENYA_COUNTIES

class RoleSelectForm(FlaskForm):
    """
    Form to select user role.

    Attributes:
        user_role (SelectField): Field to select user role.
        submit (SubmitField): Submit button for the form.
    """
    user_role = SelectField(
        'Select Role:', # Label
        choices=[
            ('', 'Select a Role'), # Default option
            ('admin', 'Admin'),
            ('farmer', 'Farmer'),
            ('vet', 'Vet')
        ],
        validators=[InputRequired()],
    )
    submit = SubmitField('Submit')

class BaseRegistrationForm(FlaskForm):
    """
    Base registration form for all user types.

    Attributes:
        first_name (StringField): Field for user's first name.
        last_name (StringField): Field for user's last name.
        email (StringField): Field for user's email.
        phone (StringField): Field for user's phone number.
        county (SelectField): Field for user's county.
        town (SelectField): Field for user's town.
        password (PasswordField): Field for user's password.
        confirm_password (PasswordField): Field to confirm user's password.
        profile_picture (FileField): Field for user's profile picture.
    """
    first_name = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email *', validators=[DataRequired(), Email(), Length(max=255)])
    
    phone = StringField('Phone Number *', validators=[
        DataRequired(),
        Length(min=10, max=20),
        Regexp(r'^\+\d{1,3}\d{7,10}$', message='Phone number must be in the format +254712345678')
        ], render_kw={"placeholder": "e.g. +254712345678"})
    
    county = SelectField('County *', choices=KENYA_COUNTIES, validators=[DataRequired()])
    town = SelectField('Town *', choices=[], validators=[DataRequired()])
    
    password = PasswordField('Password *', validators=[
        DataRequired(),
        Length(min=8, max=255),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$',
               message='Password must have at least one uppercase letter, one lowercase letter, one number, and one special character.')
        ])
    
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class FarmerRegistrationForm(BaseRegistrationForm):
    """
    Registration form for farmers.

    Attributes:
        farm_name (StringField): Field for farm name.
        livestock_type (SelectField): Field for livestock type.
        animal_count (IntegerField): Field for number of animals.
        alert_preference (SelectField): Field for alert preference.
        preferred_language (SelectField): Field for preferred language.
        submit (SubmitField): Submit button for the form.
    """
    farm_name = StringField('Farm Name', validators=[Length(min=0, max=255)])
    livestock_type = SelectField(
        'Livestock Type *',
        choices=[
            ('', 'Select Livestock Type'),
            ('cattle', 'Cattle'),
            ('poultry', 'Poultry'),
            ('sheep', 'Sheep'),
            ('goat', 'Goat'),
            ('pig', 'Pig')
            ],
        validators=[DataRequired()]
        )
    
    animal_count = IntegerField(
        'Number of Animals *', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, message='Number of animals must be a positive number.')
            ]
        )
    
    alert_preference = SelectField(
        'Alert Preference *',
        choices=[
            ('', 'Select Preference'), 
            ('email', 'Email'), 
            ('sms', 'SMS'), 
            ('whatsapp', 'WhatsApp'), 
            ('app', 'App')
            ], 
        validators=[DataRequired()]
        )
    
    preferred_language = SelectField(
        'Preferred Language *',
        choices=[
            ('', 'Select Language'),
            ('English', 'English'),
            ('Swahili', 'Swahili')
            ],
        validators=[DataRequired()]
        )
    
    submit = SubmitField('Register')
    
class VetRegistrationForm(BaseRegistrationForm):
    """
    Registration form for vets.

    Attributes:
        license_number (StringField): Field for license number.
        experience_years (IntegerField): Field for years of experience.
        specialization (SelectField): Field for specialization.
        clinic_name (StringField): Field for clinic name.
        verification_document (FileField): Field for verification document.
        submit (SubmitField): Submit button for the form.
    """
    license_number = StringField('License Number *', validators=[DataRequired(), Length(min=5, max=255)])
    
    experience_years = IntegerField(
        'Years of Experience *', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, message='Years of experience must be a positive number.')
            ]
        )
    
    specialization = SelectField(
        'Specialization *',
        choices=[
            ('', 'Select Specialization'),
            ('cattle', 'Cattle'),
            ('poultry', 'Poultry'),
            ('sheep', 'Sheep'),
            ('goat', 'Goat'),
            ('pig', 'Pig'),
            ('general', 'General')
            ],
        validators=[DataRequired()]
        )
    
    clinic_name = StringField('Clinic Name', validators=[Length(min=0, max=255)])
    
    verification_document = FileField(
        'Verification Document *', 
        validators=[
            FileRequired(), 
            FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'PDF, DOC, DOCX, JPG, JPEG, PNG only!')
            ]
        )
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): Field for user's email.
        password (PasswordField): Field for user's password.
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=255),
            Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$',
                   message='Password must have at least one uppercase letter, one lowercase letter, one number, and one special character.')
            ]
        )
    
    submit = SubmitField('Login')

class OTPForm(FlaskForm):
    """
    Form for user OTP verification.

    Attributes:
        otp (StringField): Field for user's OTP.
    """
    otp = StringField('Enter OTP', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify OTP')