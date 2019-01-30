"""
Forms for the User blueprint
"""
from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ExtendedRegisterForm(RegisterForm):
    """
    Add the screen name to the Flask-Security RegisterFrom
    """
    screen_name = StringField('Screen name', [DataRequired()])
