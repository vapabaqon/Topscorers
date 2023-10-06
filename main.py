from utils import logger
from services import account as acc

logger.setup_logger()

jwt_token = acc.get_jwt_token()
login_bonus = acc.get_login_bonus(jwt_token)
account_overview = acc.get_account_overview(jwt_token)
team_overview = acc.get_team_overview(jwt_token)