"""Module providing to manage the roster."""

import requests
from utils.api_requests import make_get_request
from config import Config

def get_roster(jwt_token):
    """Function providing to get the current roster."""
    url = f'https://topscorers.ch/api/user/teams/{Config.TEAM_ID}/lineup'
    try:
        response = make_get_request(url, jwt_token)
        if response.status_code == 200:
            print(f"API-Call erfolgreich: {response.json()}")
        else:
            print(f"API-Call fehlgeschlagen mit Status-Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim API-Call: {e}")
