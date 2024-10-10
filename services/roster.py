"""Module providing to manage the roster."""

import requests
from utils.api_requests import make_get_request
from utils import slack_messaging
from config import Config

def get_roster(jwt_token):
    """Function to get the name of the player with position_id 1 and line_up_position 1."""
    url = f'https://topscorers.ch/api/user/teams/{Config.TEAM_ID}'
    try:
        response = make_get_request(url, jwt_token)

         # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            response_data = response.json()
            players = response_data.get("data", {}).get("players", [])

            # Spieler mit position_id 1 und line_up_position 1 suchen
            for player in players:
                if player.get('position_id') == 1 and player.get('line_up_position') == 1:
                    firstname = player.get('firstname')
                    lastname = player.get('lastname')
                    full_name = f"{firstname} {lastname}"
                    slack_messaging.post_to_slack(f"Dein Goalie ist: {full_name}")
                # Kein Spieler gefunden
                slack_messaging.post_to_slack("Du hast keinen Goalie aufgestellt!")


        else:
            print(f"API-Call fehlgeschlagen mit Status-Code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim API-Call: {e}")
        return None
