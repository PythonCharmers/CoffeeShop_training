"""
Configuration settings for the Flasak application.

Using class based configuration coming from an environment .env file. Handy,
because it us do additional things in config on top of the environment if we
have to.
"""
import environs

ENV = environs.Env()
ENV.read_env()


class BaseConfig:
    """Base configuration."""

    # Flask settings
    APP_NAME = ENV("APP_NAME", "CoffeeShop")
    FLASK_ENV = ENV("FLASK_ENV", "development")
    SECRET_KEY = ENV("SECRET_KEY", "pythoncharmers")

    # database
    BCRYPT_LOG_ROUNDS = ENV.int("BCRYPT_LOG_ROUNDS", 4)
    SQLALCHEMY_TRACK_MODIFICATIONS = ENV.bool(
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        False
    )
    SQLALCHEMY_DATABASE_URI = ENV('SQLALCHEMY_DATABASE_URI')

    # security
    SECURITY_PASSWORD_HASH = ENV("SECURITY_PASSWORD_HASH")
    SECURITY_PASSWORD_SALT = ENV("SECURITY_PASSWORD_SALT")
    SECURITY_TRACKABLE = ENV.bool("SECURITY_TRACKABLE")
    SECURITY_REGISTERABLE = ENV.bool("SECURITY_REGISTERABLE")
    SECURITY_SEND_REGISTER_EMAIL = ENV.bool("SECURITY_SEND_REGISTER_EMAIL")
    SECURITY_POST_LOGIN_VIEW = ENV('SECURITY_POST_LOGIN_VIEW')
    SECURITY_POST_LOGOUT_VIEW = ENV('SECURITY_POST_LOGOUT_VIEW')
    SECURITY_POST_REGISTER_VIEW = ENV('SECURITY_POST_REGISTER_VIEW')

    # other
    WTF_CSRF_ENABLED = ENV.bool('WTF_CSRF_ENABLED')
    MAX_CONTENT_LENGTH = ENV.int('MAX_CONTENT_LENGTH', 4194304)

    # Flask-Uploads
    UPLOADED_PHOTOS_DEST = ENV('UPLOADED_PHOTOS_DEST', '/var/tmp')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG_TB_ENABLED = ENV.bool('DEBUG_TB_ENABLED')
    DEBUG_TB_INTERCEPT_REDIRECTS = ENV.bool('DEBUG_TB_INTERCEPT_REDIRECTS')


class ProductionConfig(BaseConfig):
    """Production configuration."""

    # s3 file upload
    S3_BUCKET = ENV('S3_BUCKET')
    S3_KEY_BASE = ENV('S3_KEY_BASE')
    S3_LOCATION = ENV('S3_LOCATION')


class TestingConfig(ProductionConfig):
    """Testing configuration."""

    TESTING = True
