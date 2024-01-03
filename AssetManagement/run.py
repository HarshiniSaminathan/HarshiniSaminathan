from flask import Flask
from flask_cors import CORS


from app.models.assetModel import AssetTable
from app.models.vendorModel import VendorTable
from app.models.employeeModel import EmployeeTable
from app.models.accessoriesModel import AccessoriesTable
from app.models.assetAssignmentModel import AssetAssignmentTable
from app.models.assetReturnModel import AssetReturnTable
from app.models.dbModel import db

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/assetmanagement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
