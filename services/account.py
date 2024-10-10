"""Module providing functions to retrieve token and bonus."""

import os
import sys
from datetime import datetime as dt

import requests
from utils.logger import logger
from utils.api_requests import make_get_request
from services.login import get_jwt_token

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def get_login_bonus(token):
    """Function to retrieve the login bonus."""
    try:
        url = 'https://topscorers.ch/api/user/teams'
        request_response = make_get_request(url, token)
        if request_response and request_response.status_code == 200:
            response_data = request_response.json()
            if response_data.get("bonus") is not None:
                bonus_value = response_data.get("bonus")
                logger.info('%s: Bonus erfolgreich erhalten.', dt.now().strftime("%d.%m.%Y"))
                return bonus_value
            else:
                logger.info(
                    '%s: Bonus bereits erhalten.',
                    dt.now().strftime("%d.%m.%Y")
                )
                return None
        else:
            logger.error(
                'Fehlerhafte Antwort vom Server, Status-Code: %s', request_response.status_code
                )
            return None

    except requests.exceptions.RequestException as e:
        logger.error('Ein Fehler ist aufgetreten: %s', e)

if __name__ == '__main__':
    jwt_token = get_jwt_token()
    if jwt_token:
        get_login_bonus(jwt_token)
    else:
        logger.error('Kein JWT-Token erhalten, Abbruch.')

    exit(0)
