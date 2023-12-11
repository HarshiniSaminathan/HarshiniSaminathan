from flask_cors import CORS
from flask import Flask

from app.models.dbModels import db
from app.models.userModel import User
from app.models.userProfileModel import UserProfile
from app.models.postsModel import Post
from app.models.followersModel import Followers
from app.models.likeModel import Like
from app.models.messageModel import Message
from app.models.hashtagModel import Hashtag
from app.views.adminViews import adminapi_blueprint
from app.views.userViews import userapi_blueprint
from config import SECRET_KEY
from flask_mail import Mail

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/home/divum/Downloads/new_training/HarshiniSaminathan/Social-Media Application/uploads'

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/socialmedia'}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sharshini2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'znwm mgfw jaxc bdyp'
mail = Mail(app)
db.init_app(app)

app.register_blueprint(adminapi_blueprint)
app.register_blueprint(userapi_blueprint)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(debug=True)


