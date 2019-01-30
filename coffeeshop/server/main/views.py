"""
Views for the main component of the application
"""
from flask import render_template, Blueprint


main_blueprint = Blueprint("main", __name__)  # pylint: disable=C0103


@main_blueprint.route("/")
def home():
    """
    Home page view
    """
    return render_template("main/home.html")


@main_blueprint.route("/about/")
def about():
    """
    About page view
    """
    return render_template("main/about.html")
