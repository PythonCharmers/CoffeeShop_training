# project/server/user/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_security import login_user, logout_user, login_required

from coffeeshop.server import bcrypt, db
from coffeeshop.server.models import User


user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/members")
@login_required
def members():
    return render_template("user/members.html")
