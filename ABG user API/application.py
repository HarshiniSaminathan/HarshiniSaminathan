from app import create_app
import os
from flask_cors import CORS

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

api_v1_cors_config = {
    "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    "AllowedOrigins": ["*"],
}
CORS(app, resources={"*": api_v1_cors_config})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', os.getenv('PORT')))
