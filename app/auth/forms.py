from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class RoleSelectForm(FlaskForm):
    user_role = SelectField(
        'Select Role:', # Label
        choices=[
            ('', 'Select a Role'), # Default option
            ('admin', 'Admin'),
            ('farmer', 'Farmer'),
            ('vet', 'Vet')
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField('Submit')