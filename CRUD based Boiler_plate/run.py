# run.py
from flask import Flask
from flask_cors import CORS
from app.blueprint.user_blueprint import api_blueprint
from config import SECRET_KEY

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint, url_prefix='')

if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(debug=True)
