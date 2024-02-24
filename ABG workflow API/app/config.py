import os
import urllib
from urllib import parse
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get('SECRET_KEY')
db_uri = os.getenv('MONGO_URI')
JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES')
JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES = os.environ.get('JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES')
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
MAIL_SECRET_KEY = os.environ.get('MAIL_SECRET_KEY')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
ORG_BASE_URL = os.environ.get('ORG_BASE_URL')
# Configure Flask-Caching to use Redis as a caching backend
CACHE_TYPE = 'redis'
CACHE_REDIS_URL= 'redis://localhost:6379/0'  # Update with your Redis server details


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = key

    # MongoDB configuration
    MONGO_URI = db_uri

    #flask-mail
    MAIL_SECRET_KEY = os.environ.get('MAIL_SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # Configure Flask-Caching to use Redis as a caching backend
    # CACHE_TYPE = os.environ.get('CACHE_TYPE')
    # CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')


    @staticmethod
    def get(key, default=None):
        return getattr(Config, key, default)


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig
}