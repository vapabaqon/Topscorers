"""Module used for logging."""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)

def setup_logger():
    """Function to define log levels"""

    # Verzeichnis 'logs' erstellen, falls es nicht existiert
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    formatter.encoding = 'utf-8'

    error_handler = TimedRotatingFileHandler(
        'logs/service_error.log', when='midnight', backupCount=14, encoding='utf-8'
    )
    error_handler.setLevel(logging.WARNING)  # log ERROR and WARNING
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    file_handler = TimedRotatingFileHandler(
        'logs/service_info.log', when='midnight', backupCount=7, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)  # log everything
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
