import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get('SECRET_KEY')
MONGO_URI = os.environ.get('MONGO_URI')
JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRY_IN_MINUTES')
JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES = os.environ.get('JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES')
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')



class Config(object):
    DEBUG = False
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = key

    # MongoDB configuration
    # MONGO_URI = os.environ.get('MONGO_URI','mongodb://localhost:27017/abg-auth')
    MONGO_URI = os.environ.get('MONGO_URI','mongodb://abgtravel-dbuser:zyS3Q%23RrABGtnL@13.233.18.99:27017/abgtravel-users')

    # flask-mail
    MAIL_SECRET_KEY = os.environ.get('MAIL_SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

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
