from flask import Flask
from flask_cors import CORS
from app.blueprint.user_blueprint import api_blueprint
from config import SECRET_KEY
from app.models.user_model import db

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint, url_prefix='')


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/python_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    with app.app_context():
        db.create_all()
    app.run(debug=True)
