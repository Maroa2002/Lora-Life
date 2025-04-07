
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class LivestockForm(FlaskForm):
    """
    Form for adding or updating livestock details.

    Attributes:
        name (StringField): Field for livestock name.
        age (IntegerField): Field for livestock age.
        weight (FloatField): Field for livestock weight.
        breed (StringField): Field for livestock breed.
    """
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])