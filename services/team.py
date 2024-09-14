"""Module providing functions to retrieve topcsorers team data."""
import os
import sys

from utils.api_requests import make_get_request
from config import Config

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def get_account_overview(jwt_token):
    """Function to get all teams of an account."""
    url = 'https://topscorers.ch/api/user/teams'
    return make_get_request(url, jwt_token)

def get_team_overview(jwt_token):
    """Function to get a specific team."""
    url = f'https://topscorers.ch/api/user/teams/{Config.TEAM_ID}'
    return make_get_request(url, jwt_token)
