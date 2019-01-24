# project/server/__init__.py
import os

from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
security = Security()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "coffeeshop.server.config.DevelopmentConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from coffeeshop.server.user.views import user_blueprint
    from coffeeshop.server.main.views import main_blueprint
    from coffeeshop.server.shop.views import shop_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(shop_blueprint)

    # flask security
    from coffeeshop.server.models import User, Role
    from coffeeshop.server.user.forms import ExtendedRegisterForm
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security_ctx = security.init_app(
        app,
        datastore,
        register_form=ExtendedRegisterForm  # extend the register
    )

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # GNU Terry Pratchett
    @app.after_request
    def gnu_terry_pratchett(resp):
        resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
        return resp

    return app
