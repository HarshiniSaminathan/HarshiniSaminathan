
from flask import Flask
from flask_pymongo import PyMongo
from app.config import app_config
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from flask_caching import Cache
# import redis


mongo = PyMongo()
mail = Mail()
bcrypt = Bcrypt()
# cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(app_config[config_name])
    mongo.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    # cache.init_app(app)

    # register blueprints
    from app.views.workflow import workflow_blueprint
    from app.views.workflow import user_blueprint
    from app.views.fileUpload import file_upload_blueprint
    app.register_blueprint(workflow_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(file_upload_blueprint)
    return app
