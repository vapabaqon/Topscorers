"""Main programme"""

from utils.logger import setup_logger
from utils import slack_messaging
from utils.scheduler import schedule_task
from services import roster
from services import login
from services import account
from config import Config

logger = setup_logger()

jwt_token = login.get_jwt_token()

if jwt_token:
    login_bonus = account.get_login_bonus(jwt_token)

    # Nachricht an Slack-Kanal senden, wenn ein Bonus vorhanden ist
    if login_bonus:
        bonus_amount = login_bonus.get('amount')
        budget = login_bonus.get('budget')
        slack_message = (
            f'Login Bonus heute: {bonus_amount}, '
            f'aktuelles Budget {budget:,}'
        )
        slack_message = slack_message.replace(',', "'")
        slack_messaging.post_to_slack(slack_message)
    else:
        slack_messaging.post_to_slack(
            'Kein Bonus verfügbar oder bereits erhalten: '
            'Entweder wurde der Bonus bereits abgeholt oder '
            'es liegt kein neuer Bonus vor.'
        )

    # Spielername abrufen
    SCHEDULE_TIME = Config.SCHEDULE_TIME if hasattr(Config, 'SCHEDULE_TIME') else None
    if SCHEDULE_TIME:
        # Hol die Mannschaftsdaten und die heutigen Spiele
        roster_data = roster.get_roster(jwt_token)
        today_games_data = roster.get_today_games(jwt_token)

        # Schedule die Überprüfung, ob der Goalie heute spielt
        schedule_task(roster.check_goalie_in_today_games(
            roster_data, today_games_data
            ),SCHEDULE_TIME, jwt_token)
    else:

        # Hol die Mannschaftsdaten und die heutigen Spiele
        roster_data = roster.get_roster(jwt_token)
        today_games_data = roster.get_today_games(jwt_token)

        # Überprüfe, ob der Goalie heute spielt
        roster.check_goalie_in_today_games(roster_data, today_games_data)
else:
    logger.error('Kein JWT-Token erhalten, Abbruch.')
