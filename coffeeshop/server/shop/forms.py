"""
Forms for adding shops and reviews
"""

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired


from .models import Shop, Review


images = UploadSet('images', IMAGES)


class ShopForm(FlaskForm):
    name = StringField(label='Shop name', validators=[DataRequired()])
    address = StringField(label='Address')
    url = StringField(label='Website', validators=[URL()])
    photo = FileField(label='Photo', validators=[
        FileAllowed(IMAGES, 'Images only!')
    ])
    latitude = HiddenField('latitude')
    longitude = HiddenField('longitude')

    submit = SubmitField()

