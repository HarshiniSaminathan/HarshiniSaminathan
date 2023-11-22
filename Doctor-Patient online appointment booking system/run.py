from flask import Flask
from flask_cors import CORS

from config import SECRET_KEY
from app.views.adminViews import adminapi_blueprint
from app.views.patientViews import patientapi_blueprint
from app.views.doctorViews import doctorapi_blueprint


from app.models.patientModel import db,PatientTable
from app.models.adminModel import db,AdminTable
from app.models.appointmentModel import db,appointmentTable
from app.models.slotModel import db,slotTable
from app.models.doctorModel import db,DoctorTable
from app.models.medicalRecordsModel import db,MedicalRecordsTable
from app.models.prescriptionModel import db,PrescriptionTable
from app.models.feedbackModel import db,FeedbackSession
from app.models.userModel import db


app = Flask(__name__)
CORS(app)

app.register_blueprint(adminapi_blueprint)
app.register_blueprint(patientapi_blueprint)
app.register_blueprint(doctorapi_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/appointmentbooking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
