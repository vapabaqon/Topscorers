"""Main programme"""

from utils import logger
from utils import slack_messaging
from services import login
from services import account

logger.setup_logger()

jwt_token = login.get_jwt_token()
login_bonus = account.get_login_bonus(jwt_token)

# Nachricht an Slack-Kanal senden, wenn ein Bonus vorhanden ist
if login_bonus:
    slack_messaging.post_to_slack(f'Login Bonus: {login_bonus}')
else:
    slack_messaging.post_to_slack('Kein Bonus verfügbar oder bereits erhalten.')
    