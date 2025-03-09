from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, StringField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, InputRequired, Regexp
from flask_wtf.file import FileAllowed, FileRequired
from app.utils import KENYA_COUNTIES

class RoleSelectForm(FlaskForm):
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
    """
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=20),
        Regexp(r'^\+\d{1,3}\d{7,10}$', message='Phone number must be in the format +254712345678')
        ], render_kw={"placeholder": "e.g. +254712345678"})
    
    county = SelectField('County', choices=KENYA_COUNTIES, validators=[DataRequired()])
    town = SelectField('Town', choices=[('', 'Select a Town')], validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=255),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message='Password must have at least one uppercase letter, one lowercase letter, one number, and one special character.')
        ])
    
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class FarmerRegistrationForm(BaseRegistrationForm):
    """
    Registration form for farmers.
    """
    farm_name = StringField('Farm Name', validators=[Length(min=2, max=255)])
    livestock_type = SelectField(
        'Livestock Type',
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
        'Number of Animals', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, message='Number of animals must be a positive number.')
            ]
        )
    
    alert_preference = SelectField(
        'Alert Preference',
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
        'Preferred Language',
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
    """
    license_number = StringField('License Number', validators=[DataRequired(), Length(min=5, max=255)])
    
    experience_years = IntegerField(
        'Years of Experience', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, message='Years of experience must be a positive number.')
            ]
        )
    
    specialization = SelectField(
        'Specialization',
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
    
    clinic_name = StringField('Clinic Name', validators=[Length(min=2, max=255)])
    
    verification_document = FileField(
        'Verification Document', 
        validators=[
            FileRequired(), 
            FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'PDF, DOC, DOCX, JPG, JPEG, PNG only!')
            ]
        )
    
    submit = SubmitField('Register')
    