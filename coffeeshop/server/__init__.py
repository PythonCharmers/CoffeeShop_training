"""
Entry point for the Flask application

This contains the application factory method create_app to create the Flask app
object. You can point the FLASK_APP environment here when running the app to
have flask automatically call the create_app method, or another Python file (the
WSGI file) can call create_app itself.
"""
import os

import boto3
from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES

# instantiate the extensions
# pylint: disable=C0103
# note stylistically I'd prefer these to be lower case, so I can disable the
# pylint error check for a particular line of code.
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
security = Security()
photos = UploadSet('photos', IMAGES)
s3 = boto3.client("s3")  # even without credentials this should work
# pylint: enable=C0103


def create_app(script_info=None):
    """
    Application factory to create the Flask application.
    """

    from logging.config import dictConfig

    # Set up logging at DEBUG level ...
    # From here: http://flask.pocoo.org/docs/dev/logging/
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })

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
    from coffeeshop.server.shop.views import coffee_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(coffee_blueprint)

    # flask security
    from coffeeshop.server.models import User, Role
    from coffeeshop.server.user.forms import ExtendedRegisterForm
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(
        app,
        datastore,
        register_form=ExtendedRegisterForm  # extend the register
    )

    # jinja2 filters
    from .filters import env_override
    app.jinja_env.filters['env_override'] = env_override

    # error handlers
    # pylint: disable=W0613,W0612
    @app.errorhandler(401)
    def unauthorized_page(error):
        """Custom template for 401"""
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        """Custom template for 403"""
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        """Custom template for 404"""
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        """Custom template for 500"""
        return render_template("errors/500.html"), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.after_request
    def gnu_terry_pratchett(resp):
        """
        GNU Terry Pratchett

        See http://gnuterrypratchett.com/ for how and why.
        """
        resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
        return resp
    # pylint: enable=W0613,W0612

    # flask-uploads
    configure_uploads(app, (photos, ))
    patch_request_class(app, None)

    return app
