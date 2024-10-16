# Import required modules
import logging
from logging.handlers import RotatingFileHandler

# Define logger configuration
def setup_logger(app):
    """
    Configure logger for Flask app.

    :param app: The Flask app.
    """
    # Configure logging level
    log_level = logging.getLevelName(app.config['LOG_LEVEL'].upper())
    app.logger.setLevel(log_level)

    # Configure logging to file
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


