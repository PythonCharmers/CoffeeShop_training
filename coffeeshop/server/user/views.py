"""
Views for the user blueprint
"""
from flask import render_template, Blueprint
from flask_security import roles_required


user_blueprint = Blueprint("user", __name__)  # pylint: disable=C0103


@user_blueprint.route("/members")
@roles_required('admin')
def members():
    """
    A page which requires the user to be an admin
    """
    return render_template("user/members.html")
