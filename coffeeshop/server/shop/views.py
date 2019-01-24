"""
Views for the actual coffee shops
"""
import os.path

from flask import render_template, Blueprint, redirect, current_app
from flask_security import login_required, current_user

from coffeeshop.server import db
from .forms import ShopForm
from .utils import secure_filename, upload_file_to_s3
from .models import Shop, Review

coffee_blueprint = Blueprint("coffee", __name__)


# http://zabana.me/notes/upload-files-amazon-s3-flask.html


@coffee_blueprint.route('/shop/<int:id>')
def shops(id):
    shop = Shop.query.get(1)
    return str(id)


@coffee_blueprint.route('/shop/add', methods=['GET', 'POST'])
@login_required
def add_shop():
    form = ShopForm()
    if form.validate_on_submit():

        shop_name = form.name.data
        address = form.address.data
        url = form.url.data

        latitude = form.latitude.data
        longitude = form.longitude.data
        current_app.logger.debug(f'{latitude} {longitude}')

        geom = None
        if latitude and longitude:
            geom = f'POINT ({longitude} {latitude})'

        photo = None
        f = form.photo.data
        if f:
            f.filename = secure_filename(f.filename)
            photo = upload_file_to_s3(f)

        shop = Shop(name=shop_name, address=address, url=url, photo=photo, location=geom, user=current_user)
        db.session.add(shop)
        db.session.commit()
        current_app.logger.info(f'Created new {shop}')

        return redirect(f'/shop/{shop.id}')
    return render_template('shop/create.html', form=form)


@coffee_blueprint.route('/shop/search')
@login_required
def search_shop():
    pass


@coffee_blueprint.route('/review/add', methods=['GET', 'POST'])
@login_required
def add_review():
    pass


