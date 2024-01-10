from flask import Flask
from flask_cors import CORS
import config

from app.views.adminViews import adminapi_blueprint

from app.models.assetModel import AssetTable,db
from app.models.vendorModel import VendorTable,db
from app.models.employeeModel import EmployeeTable,db
from app.models.accessoriesAssModel import AccessoriesAssTable,db
from app.models.acceessoriesModel import AccessoriesTable,db
from app.models.assetAssignmentModel import AssetAssignmentTable,db
from app.models.dbModel import db


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/home/divum/asset-management-backend/uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

app.register_blueprint(adminapi_blueprint)

if __name__ == "__main__":
    app.secret_key = config.SECRET_KEY
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
