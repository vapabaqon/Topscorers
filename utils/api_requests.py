"""Module making GET requests."""

import json
import requests
from config import Config
from utils.logger import logger

def make_get_request(url, jwt_token):
    """Function making the request."""
    try:
        headers = Config.BASIC_HEADERS
        headers["Authorization"] = f'Bearer {jwt_token}'
        response = requests.get(url, headers=headers, timeout=10)  # Timeout von 10s gesetzt
        response.raise_for_status()  # Prüft auf HTTP-Fehler
        return response.json()  # Prüft, ob die Antwort ein gültiges JSON ist
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP Fehler aufgetreten: %s',{http_err})
    except requests.exceptions.RequestException as req_err:
        logger.error('Netzwerkfehler aufgetreten: %s',{req_err})
    except json.JSONDecodeError as json_err:
        logger.error('Fehler beim Verarbeiten der JSON-Antwort: %s',{json_err})
    return None

def load_credentials(service_name):
    """Lädt die Anmeldeinformationen für den angegebenen Dienst aus der credentials.json Datei"""
    with open('credentials.json', 'r', encoding="utf-8") as file:
        credentials = json.load(file)
    return credentials.get(service_name)
