"""Module providing functions to retrieve token and bonus."""

import os
import sys
import json
from datetime import datetime as dt

import requests
from utils.logger import logger
from utils.api_requests import make_get_request
from config import Config

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def get_jwt_token():
    """Function to get the JWT token."""
    try:
        # Datei credentials.json einlesen
        with open('credentials.json', 'r', encoding="utf-8") as file:
            request_body = json.load(file)

        url = 'https://topscorers.ch/api/login'
        headers = Config.BASIC_HEADERS
        request_response = requests.post(url, json=request_body, headers=headers, timeout=10).text
        return request_response
    except requests.exceptions.RequestException as e:
        logger.error('Ein Fehler ist aufgetreten: %s', {e})

def get_login_bonus(token):
    """Function to retrieve the login bonus."""
    try:
        url = 'https://topscorers.ch/api/user/teams'
        headers = Config.BASIC_HEADERS
        headers["Authorization"] = f'Bearer {token}'
        request_response = make_get_request(url, token)
        if request_response and request_response.get("bonus") is not None:
            logger.info('%s: Bonus erfolgreich erhalten.', {dt.now().strftime("%d.%m.%Y")})
            return 5000
        else:
            logger.info('%s: Bonus bereits erhalten.', {dt.now().strftime("%d.%m.%Y")})
            return None

    except requests.exceptions.RequestException as e:
        logger.error('Ein Fehler ist aufgetreten: %s', {e})

if __name__ == '__main__':
    jwt_token = get_jwt_token()
    if jwt_token:
        get_login_bonus(jwt_token)
    else:
        logger.error('Kein JWT-Token erhalten, Abbruch.')

    exit(0)
