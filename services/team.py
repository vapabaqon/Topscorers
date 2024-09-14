import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from utils.logger import logger
from config import Config
from datetime import datetime as dt
import requests
import json
from utils.api_requests import make_get_request
from config import Config

def get_account_overview(jwt_token):
    url = 'https://topscorers.ch/api/user/teams'
    return make_get_request(url, jwt_token)

def get_team_overview(jwt_token):
    url = f'https://topscorers.ch/api/user/teams/{Config.TEAM_ID}'
    return make_get_request(url, jwt_token)