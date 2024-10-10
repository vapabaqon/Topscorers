"""Main programme"""

from utils.logger import logger
from utils.logger import setup_logger
from utils import slack_messaging
from utils.scheduler import schedule_task
from services import roster
from services import login
from services import account

setup_logger()

jwt_token = login.get_jwt_token()
login_bonus = account.get_login_bonus(jwt_token)

# Nachricht an Slack-Kanal senden, wenn ein Bonus vorhanden ist
if login_bonus:
    slack_messaging.post_to_slack(f'Login Bonus: {login_bonus}')
else:
    slack_messaging.post_to_slack('Kein Bonus verfügbar oder bereits erhalten.')


if jwt_token:
    # Spielername abrufen
    schedule_task(roster.get_roster, "00:02", jwt_token)
else:
    logger.error('Kein JWT-Token erhalten, Abbruch.')
