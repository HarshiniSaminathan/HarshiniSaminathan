import json
from datetime import time
import time
from os import abort

from celery.worker.state import requests
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_session import Session
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache
from celery import Celery
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
import jwt
from datetime import datetime, timedelta


from app.views.userViews import loginapi_blueprint
from config import SECRET_KEY
from app.views.adminViews import adminapi_blueprint
from app.views.patientViews import patientapi_blueprint
from app.views.doctorViews import doctorapi_blueprint
from werkzeug.utils import secure_filename
from flask_apscheduler import APScheduler
from app.controller.patientController import check_for_PMR_beforeDay, sending_ad

from app.models.patientModel import db,PatientTable
from app.models.adminModel import db,AdminTable
from app.models.appointmentModel import db,appointmentTable
from app.models.slotModel import db,slotTable
from app.models.doctorModel import db,DoctorTable
from app.models.medicalRecordsModel import db,MedicalRecordsTable
from app.models.prescriptionModel import db,PrescriptionTable
from app.models.feedbackModel import db,FeedbackSession
from app.models.CommerceCSVModel import CommerceCSVModel
from app.controller.patientController import check_for_PMR_beforeDay
from app.models.userModel import db

UPLOAD_FOLDER = '/home/divum/Downloads/new_training/HarshiniSaminathan/Doctor-Patient online appointment booking system/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg','xlsx'}

appConf = {
    "OAUTH2_CLIENT_ID": "225930108249-h52egbt16339ih60lg6jpbpet17gljmt.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": f"{SECRET_KEY}",
    "FLASK_PORT": 5000
}

app = Flask(__name__)
CORS(app)

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
    'google',
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",

    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)


@app.route("/")
def home():
    return render_template("home.html", user=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

import secrets

@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state
    return oauth.google.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True), state=state)

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_public_key(private_key_path, public_key_path):
    # Load the private key from file
    with open(private_key_path, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None,
            backend=default_backend()
        )

    # Obtain the public key
    public_key = private_key.public_key()

    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save the public key to a file
    with open(public_key_path, 'wb') as file:
        file.write(public_key_pem)



import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# def decode_oauth_token(oauth_token):
#     try:
#         public_key_path="private_key.pem"
#         # Load the public key from file
#         with open(public_key_path, 'rb') as file:
#             private_key = serialization.load_pem_private_key(
#                 file.read(),
#                 password=None,  # Change this to your actual password
#                 backend=default_backend()
#             )
#
#         issuer = 'https://accounts.google.com'  # Replace with your actual issuer
#         private_key_bytes = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.TraditionalOpenSSL,
#             encryption_algorithm=serialization.NoEncryption()
#         )
#
#         # Convert the private key bytes to string
#         private_key_str = private_key_bytes.decode('utf-8')
#         print("private_key_str",private_key_str)
#
#         decoded_token = jwt.decode(oauth_token, key=private_key_str, algorithms=['RS256'], issuer=issuer)
#
#         return decoded_token
#     except jwt.ExpiredSignatureError:
#         print("Token has expired.")
#     except jwt.InvalidTokenError:
#         print("Invalid token format or content.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

ISSUER = 'https://accounts.google.com'


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


import base64
import json

def decode_oauth_token(oauth_token):
    try:
        header, payload, signature = oauth_token.split('.')

        decoded_header = base64.urlsafe_b64decode(header + '==').decode('utf-8')
        decoded_payload = base64.urlsafe_b64decode(payload + '==').decode('utf-8')

        header_dict = json.loads(decoded_header)
        payload_dict = json.loads(decoded_payload)

        print("Decoded Header:", header_dict)
        print("Decoded Payload:", payload_dict)

        return payload_dict

    except Exception as e:
        print(f"Error decoding OAuth token: {e}")
        return None


@app.route("/signin-google")
def googleCallback():
    try:
        received_state = request.args.get("state")
        stored_state = session.pop("oauth_state", None)


        if received_state != stored_state:
            return "CSRF Warning! State mismatch."

        token = oauth.google.authorize_access_token()
        oAuthToken =token['access_token']
        email = token['userinfo']['email']
        id_token = token['id_token']
        decoded_token = decode_oauth_token(id_token)
        user_id = decoded_token.get('sub')
        email = decoded_token.get('email')
        exp = decoded_token.get('exp')
        print("user_id",user_id,"email",email,"exp",exp)

        print("decoded_token",decoded_token)


        # person_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
        # person_data = requests.get(person_data_url, headers={"Authorization": f"Bearer {token['access_token']}"})
        # person_data_json = person_data.json()
        # token["personData"] = person_data_json

        session["user"] = token

        return redirect(url_for("home"))
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'my_cache_prefix', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
# cache_timeout = 600
app.cache = cache

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/appointmentbooking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'uploads'


# app.config['CACHE_TYPE'] = 'redis'
# app.config['CACHE_KEY_PREFIX'] = 'my_cache_prefix'
# app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/16'
#
# cache = Cache(app)

# celery = Celery(app.name, broker='redis://localhost:6379/0')
# celery.conf.update(app.config)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sharshini2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'znwm mgfw jaxc bdyp'
mail = Mail(app)
db.init_app(app)

migrate = Migrate(app, db)
scheduler = APScheduler()
scheduler.init_app(app)


app.register_blueprint(adminapi_blueprint)
app.register_blueprint(patientapi_blueprint)
app.register_blueprint(doctorapi_blueprint)
app.register_blueprint(loginapi_blueprint)


# @scheduler.task('cron', id='check_for_PMR', hour=16, minute=00)  # 4:00 PM
# def scheduled_check_for_PMR():
#     with app.app_context():
#         check_for_PMR_beforeDay()

# @scheduler.task('cron', id='sending_ad', hour=23)
# def advertisement_sending():
#     with app.app_context():
#         sending_ad()


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    with app.app_context():
        # db.drop_all()
        db.create_all()
    scheduler.start()
    app.run(debug=True,port=5000)
