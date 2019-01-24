# project/server/models.py
from geoalchemy2 import Geography
from sqlalchemy_utils import URLType, ChoiceType

from coffeeshop.server import db
from ..models import User


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    address = db.Column(db.String)
    location = db.Column(Geography(
        geometry_type='POINT', srid=4326, spatial_index=True
    ))
    url = db.Column(URLType)
    photo = db.Column(db.String)  # store the URL location of uploaded photos, or perhaps just the filename.

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship(User, backref=db.backref('shops'))

    def __repr__(self):
        return f'<Shop name={self.name} address={self.address} location={self.location} url={self.url} photo={self.photo} user={self.user_id}>'


class Review(db.Model):
    __tablename__ = 'review'

    SCORES = [
        (0, 'Bad'),
        (1, 'Good')
    ]

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(ChoiceType(SCORES, impl=db.Integer), nullable=False)
    comment = db.Column(db.String)

    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    shop = db.relationship(Shop, backref=db.backref('reviews'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('reviews'))
