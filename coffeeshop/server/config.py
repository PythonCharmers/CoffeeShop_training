# project/server/config.py
import environs

env = environs.Env()
env.read_env()


class BaseConfig(object):
    """Base configuration."""

    # Flask settings
    APP_NAME = env("APP_NAME", "CoffeeShop")
    FLASK_ENV = env("FLASK_ENV", "development")
    SECRET_KEY = env("SECRET_KEY", "pythoncharmers")

    # database
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", 4)
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_DATABASE_URI = env('SQLALCHEMY_DATABASE_URI')

    # security
    SECURITY_PASSWORD_HASH = env("SECURITY_PASSWORD_HASH")
    SECURITY_PASSWORD_SALT = env("SECURITY_PASSWORD_SALT")
    SECURITY_TRACKABLE = env("SECURITY_TRACKABLE")
    SECURITY_REGISTERABLE = env("SECURITY_REGISTERABLE")
    SECURITY_SEND_REGISTER_EMAIL = env("SECURITY_SEND_REGISTER_EMAIL")

    # s3 file upload
    S3_BUCKET = env('S3_BUCKET')
    S3_KEY_BASE = env('S3_KEY_BASE')
    S3_LOCATION = env('S3_LOCATION')

    # other
    WTF_CSRF_ENABLED = False
    MAX_CONTENT_LENGTH = env.int('MAX_CONTENT_LENGTH', 4194304)

class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    pass

class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    pass
