
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Harshini%402003@localhost:5432/python_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from app.blueprint.user_blueprint import api_blueprint

app.register_blueprint(api_blueprint, url_prefix='/')

with app.app_context():
    db.create_all()
