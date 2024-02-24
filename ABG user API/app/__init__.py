from flask import Flask
from flask_pymongo import PyMongo
from app.config import app_config
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os


mongo = PyMongo()
mail = Mail()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(app_config[config_name])

    mongo.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from app.views.user import user_blueprint
    from app.views.user import device_blueprint
    from app.views.role import role_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(device_blueprint)
    app.register_blueprint(role_blueprint)
    return app
