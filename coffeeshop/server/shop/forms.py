"""
Forms for adding shops and reviews
"""

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired


from .models import Shop, Review


images = UploadSet('images', IMAGES)


class URLValidator(URL):
    """
    Subclass the URL validator to remove the implicit requirement for a value
    """
    def __call__(self, form, field):

        if field.data:
            super().__call__(form, field)


class ShopForm(FlaskForm):
    name = StringField(label='Shop name', validators=[DataRequired()])
    address = StringField(label='Address')
    url = StringField(label='Website', validators=[URLValidator()])
    photo = FileField(label='Photo', validators=[
        FileAllowed(IMAGES, 'Images only!')
    ])
    latitude = HiddenField('latitude')
    longitude = HiddenField('longitude')

    submit = SubmitField()


class ReviewForm(FlaskForm):
    rating = RadioField(
        label='How was the coffee?',
        validators=[DataRequired()],
        choices=[
            (1, '👍'),
            (2, '👎')
        ],
        coerce=int
    )
    comment = StringField(label='Comment')
    shop_id = HiddenField('shop_id')

    submit = SubmitField()
