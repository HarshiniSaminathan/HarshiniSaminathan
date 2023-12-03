from flask_cors import CORS
from flask import Flask

from app.models.dbModels import db
from app.models.userModel import User
from app.models.userProfileModel import UserProfile
from app.views.adminViews import adminapi_blueprint
from app.views.userViews import userapi_blueprint
from config import SECRET_KEY

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/home/divum/Downloads/new_training/HarshiniSaminathan/Social-Media Application/uploads'

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/socialmedia'}

db.init_app(app)

app.register_blueprint(adminapi_blueprint)
app.register_blueprint(userapi_blueprint)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(debug=True)


