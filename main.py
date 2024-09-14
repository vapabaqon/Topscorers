"""Main programme"""

from utils import logger
from services import login
from services import account

logger.setup_logger()

jwt_token = login.get_jwt_token()
login_bonus = account.get_login_bonus(jwt_token)
