from flask import Flask
from flask_cors import CORS

from app.Views.Asset_view import asset_api_blueprint
from app.Views.user_view import api_blueprint
from app.Views.vendor_view import vendorapi_blueprint
from config import SECRET_KEY
from app.models.user_model import db

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_blueprint, url_prefix='')
app.register_blueprint(vendorapi_blueprint,url_prefix='')
app.register_blueprint(asset_api_blueprint,url_prefix='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/python_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
