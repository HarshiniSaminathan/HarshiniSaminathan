# Import required modules
import os
from datetime import timedelta

# Define commonly used constants
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # Root directory of the Flask application
APP_NAME = "My Flask App" # Name of the Flask application
DEBUG_MODE = True # Debug mode setting for the Flask application
JWT_SECRET_KEY = "mysecretkey" # Secret key for JWT token encryption
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) # Access token expiration time
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) # Refresh token expiration time

# Define commonly used functions
def get_env_variable(name):
    """
    Get the value of an environment variable by name.

    :param name: The name of the environment variable.
    :return: The value of the environment variable.
    """
    try:
        return os.environ[name]
    except KeyError:
        error_msg = f"Environment variable {name} not set."
        raise ValueError(error_msg)

def get_database_uri():
    """
    Get the URI for connecting to the database.

    :return: The database URI.
    """
    db_host = get_env_variable("DB_HOST")
    db_port = get_env_variable("DB_PORT")
    db_name = get_env_variable("DB_NAME")
    db_user = get_env_variable("DB_USER")
    db_password = get_env_variable("DB_PASSWORD")

    return f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
