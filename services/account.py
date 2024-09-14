import os
import sys
import json
import requests
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from utils.logger import logger
from utils.api_requests import make_get_request
from config import Config
from datetime import datetime as dt

def get_jwt_token():
    try:
        # Datei credentials.json einlesen
        with open('credentials.json', 'r') as file:
            request_body = json.load(file)

        url = 'https://topscorers.ch/api/login'
        headers = Config.BASIC_HEADERS
        request_response = requests.post(url, json=request_body, headers=headers).text
        return request_response
    
    except Exception as e:
        logger.error(f'Ein Fehler ist aufgetreten: {e}')

def get_login_bonus(jwt_token):
    try:
        url = 'https://topscorers.ch/api/user/teams'
        headers = Config.BASIC_HEADERS
        headers["Authorization"] = f'Bearer {jwt_token}'
        request_response = make_get_request(url, jwt_token)
        if request_response and request_response.get("bonus") is not None:
            logger.info(f'{dt.now().strftime("%d.%m.%Y")}: Bonus erfolgreich erhalten.')
            return 5000
        else:
            logger.info(f'{dt.now().strftime("%d.%m.%Y")}: Bonus bereits erhalten.')
            return None

    except Exception as e:
        logger.error(f'Ein Fehler ist aufgetreten: {e}')

if __name__ == '__main__':
    jwt_token = get_jwt_token()
    if jwt_token:
        get_login_bonus(jwt_token)
    else:
        logger.error('Kein JWT-Token erhalten, Abbruch.')

    exit(0)
