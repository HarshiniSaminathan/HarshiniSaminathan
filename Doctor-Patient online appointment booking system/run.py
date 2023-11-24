from datetime import time
import time
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery
from config import SECRET_KEY
from app.views.adminViews import adminapi_blueprint
from app.views.patientViews import patientapi_blueprint
from app.views.doctorViews import doctorapi_blueprint
from werkzeug.utils import secure_filename
from flask_apscheduler import APScheduler
from app.controller.patientController import check_for_PMR_beforeDay


from app.models.patientModel import db,PatientTable
from app.models.adminModel import db,AdminTable
from app.models.appointmentModel import db,appointmentTable
from app.models.slotModel import db,slotTable
from app.models.doctorModel import db,DoctorTable
from app.models.medicalRecordsModel import db,MedicalRecordsTable
from app.models.prescriptionModel import db,PrescriptionTable
from app.models.feedbackModel import db,FeedbackSession
from app.controller.patientController import check_for_PMR_beforeDay
from app.models.userModel import db

UPLOAD_FOLDER = '/home/divum/Downloads/new_training/HarshiniSaminathan/Doctor-Patient online appointment booking system/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/appointmentbooking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'uploads'

celery = Celery(app.name, broker='redis://localhost:6379/0')
celery.conf.update(app.config)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sharshini2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'znwm mgfw jaxc bdyp'
mail = Mail(app)
db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(adminapi_blueprint)
app.register_blueprint(patientapi_blueprint)
app.register_blueprint(doctorapi_blueprint)

@scheduler.task('cron', id='check_for_PMR', hour=16, minute=00)  # 4:00 PM
def scheduled_check_for_PMR():
    with app.app_context():
        check_for_PMR_beforeDay()


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    with app.app_context():
        # db.drop_all()
        db.create_all()
    scheduler.start()
    app.run(debug=True)

