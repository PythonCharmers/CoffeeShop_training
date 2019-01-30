"""
Forms for adding shops and reviews
"""
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL, AnyOf


images = UploadSet('images', IMAGES)  # pylint: disable=C0103


class URLValidator(URL):
    """
    Subclass the URL validator to remove the implicit requirement for a value
    """
    def __call__(self, form, field):

        if field.data:
            super().__call__(form, field)


class ShopForm(FlaskForm):
    """
    HTML form a a Shop
    """
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
    """
    HTML form for a Review
    """
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
    """
    HTML form to enter a search term
    """
    q = StringField('Find a coffee shop', validators=[DataRequired()])
    submit = SubmitField()
