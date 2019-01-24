# project/server/user/forms.py
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_security.forms import RegisterForm


class ExtendedRegisterForm(RegisterForm):
    screen_name = StringField('Screen name', [DataRequired()])
