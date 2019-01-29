from flask import render_template, Blueprint
from flask_security import current_user
from sqlalchemy import func

from coffeeshop.server import db
from coffeeshop.server.shop.models import Shop, Review


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    """
    Display more useful information on the homepage

    Include the last 10 added shops in the application, the last 10 reviewed
    shop and the last 10 added shops by the user.
    """
    # most recently added 10 shops (the exercise)
    shops = Shop.query.order_by(Shop.date_added.desc()).limit(10)

    # most recently reviewed shops - going a bit further
    reviewed_query = db.session.query(
        Review.shop_id,
        func.max(Review.date_added).label('max_date')
    ).group_by(
        Review.shop_id
    ).subquery()
    reviewed_shops = db.session.query(
        Shop
    ).join(
        reviewed_query,
        Shop.id == reviewed_query.c.shop_id
    ).order_by(
        reviewed_query.c.max_date.desc()
    ).limit(10)

    # and further again to take advantage of logged in user.
    if current_user.is_authenticated:

        user_shops = Shop.query.filter(
            Shop.user == current_user
        ).order_by(
            Shop.date_added.desc()
        ).limit(10)

    else:
        user_shops = None

    return render_template(
        "main/home.html",
        shops=shops,
        reviewed_shops=reviewed_shops,
        user_shops=user_shops
    )


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
