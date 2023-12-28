from flask import Flask
from flask_cors import CORS

from app.models.dbModels import db
from app.models.userModel import User
from app.models.bookings import Bookings
from app.models.busInfoModel import BusInfo
from app.models.passengerInfo import PassengerDetails
from app.strings import SECRET_KEY
from app.views.userViews import userapi_blueprint
from app.views.busviews import busapi_blueprint
app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER="/home/divum/Downloads/new_training/HarshiniSaminathan/BusBookingSystem/app/uploads"

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/busbooking'}

db.init_app(app)

app.register_blueprint(userapi_blueprint)
app.register_blueprint(busapi_blueprint)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(debug=True)


