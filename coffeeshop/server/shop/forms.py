"""
Forms for adding shops and reviews
"""

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL, AnyOf
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed


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
        validators=[AnyOf((0, 1))],
        choices=[
            (1, '👍'),
            (0, '👎')
        ],
        coerce=int
    )
    comment = StringField(label='Comment')
    shop_id = HiddenField('shop_id')

    submit = SubmitField()


class SearchForm(FlaskForm):
    q = StringField('Find a coffee shop', validators=[DataRequired()])
    submit = SubmitField()
