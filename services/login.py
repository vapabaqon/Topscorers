"""Module providing login function."""

import os
import sys
import json

import requests
from utils.logger import logger
from config import Config

# Den absoluten Pfad zum Projektverzeichnis bestimmen
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def get_jwt_token():
    """Function to get the JWT token."""
    try:
        # Absoluter Pfad zu credentials.json
        credentials_path = os.path.join(parent_dir, 'credentials.json')

        # Datei credentials.json einlesen und Anmeldeinformationen für "Topscorers" extrahieren
        with open(credentials_path, 'r', encoding="utf-8") as file:
            credentials = json.load(file)
            topscorers_credentials = credentials.get('Topscorers')
            if not topscorers_credentials:
                raise ValueError("Anmeldeinformationen für Topscorers nicht gefunden.")

            email = topscorers_credentials.get('email')
            password = topscorers_credentials.get('password')
            if not email or not password:
                raise ValueError("Email oder Passwort fehlt für Topscorers.")

        # Request-Body mit den geladenen Anmeldeinformationen erstellen
        request_body = {
            "email": email,
            "password": password
        }

        # API-Anfrage stellen
        url = 'https://topscorers.ch/api/login'
        headers = Config.BASIC_HEADERS
        request_response = requests.post(url, json=request_body, headers=headers, timeout=10).text
        return request_response

    except requests.exceptions.RequestException as e:
        logger.error('Ein Fehler ist aufgetreten: %s', {e})
    except ValueError as e:
        logger.error('Fehler in den Anmeldeinformationen: %s', {e})
