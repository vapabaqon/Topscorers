"""Module providing login function."""

import os
import sys
import json

import requests
from utils.logger import logger
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
