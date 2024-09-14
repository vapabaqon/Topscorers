# api_requests.py
import requests
import json
from config import Config
from utils.logger import logger

def make_get_request(url, jwt_token):
    try:
        headers = Config.BASIC_HEADERS
        headers["Authorization"] = f'Bearer {jwt_token}'
        response = requests.get(url, headers=headers, timeout=10)  # Timeout von 10s gesetzt
        response.raise_for_status()  # Prüft auf HTTP-Fehler
        return response.json()  # Prüft, ob die Antwort ein gültiges JSON ist
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP Fehler aufgetreten: {http_err}')
    except requests.exceptions.RequestException as req_err:
        logger.error(f'Netzwerkfehler aufgetreten: {req_err}')
    except json.JSONDecodeError as json_err:
        logger.error(f'Fehler beim Verarbeiten der JSON-Antwort: {json_err}')
    except Exception as e:
        logger.error(f'Ein unbekannter Fehler ist aufgetreten: {e}')
    return None
