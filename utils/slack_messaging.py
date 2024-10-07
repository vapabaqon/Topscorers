"""Module providing a function to post to a Slack channel."""

import json
import os
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Findet den absoluten Pfad zur credentials.json basierend auf dem Verzeichnis des Skripts
credentials_path = os.path.join(parent_dir, 'credentials.json')

# Öffne die credentials.json Datei
with open(credentials_path, 'r', encoding="utf-8") as file:
    credentials = json.load(file)
    slack_credentials = credentials.get('Slack')
    if not slack_credentials:
        raise ValueError("Anmeldeinformationen für Slack nicht gefunden.")
    slack_token = slack_credentials.get('token')
    slack_channel = slack_credentials.get('channel')
client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel = slack_channel,  # Channel ID oder Name mit '#'
        text="Hallo, dies ist eine Nachricht über die API"
    )
except SlackApiError as e:
    print(f"Fehler: {e.response['error']}")
