# project/server/user/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_security import login_required

from coffeeshop.server import bcrypt, db
from .models import Shop, Review

shop_blueprint = Blueprint("shop", __name__)


# http://zabana.me/notes/upload-files-amazon-s3-flask.html
