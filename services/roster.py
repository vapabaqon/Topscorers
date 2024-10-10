"""Module providing functions to check the current roster """

from utils.api_requests import make_get_request
from utils import slack_messaging
from utils.logger import logger
from config import Config

# Function to get the roster of the team using the provided JWT token
def get_roster(jwt):
    """Get the roster of the team."""
    # Construct the API URL with the team ID
    url = f'https://topscorers.ch/api/user/teams/{Config.TEAM_ID}'
    # Make a GET request to the URL
    response = make_get_request(url, jwt)
    # If the response is successful, return the roster data as JSON
    if response.status_code == 200:
        return response.json()
    else:
        # Log an error if the request fails
        logger.error("Failed to get roster: %s", response.status_code)
        return None

# Function to get today's games using the live-API endpoint
def get_today_games(jwt):
    """Check if there are games today."""
    url = f'https://topscorers.ch/api/live?user_team_id={Config.TEAM_ID}&all=1'
    # Make a GET request to the URL with a timeout of 10 seconds
    response = make_get_request(url, jwt)
    # If the response is successful, return the games data as JSON
    if response.status_code == 200:
        return response.json()
    else:
        # Log an error if the request fails
        logger.error("Failed to get today's games: %s", response.status_code)
        return None

# Helper function to find the goalie in the lineup
def find_goalie_in_lineup(roster):
    """Find the goalie in the roster who is in the lineup."""
    for player in roster.get('players', []):
        # Check if the player's position is 'Goalie' and if they are in the starting lineup
        if player.get('position_name') == 'Goalie' and player.get('line_up_position') == 1:
            return player
    return None

# Function to check if the goalie from the roster is playing in today's games
def check_goalie_in_today_games(roster, games):
    """Check if the goalie from the roster is playing in today's games."""
    # If either the roster or games data is not available, return early
    if not roster or not games:
        return

    # Find the goalie in the roster who is in the lineup
    roster_goalie = find_goalie_in_lineup(roster)

    # If no goalie is found in the lineup, log that information and return
    if not roster_goalie:
        logger.info("No goalie in lineup today.")
        slack_messaging.post_to_slack("Keiner deiner Goalies spielt heute.")
        return

    # Store the team ID to avoid repeated nested access
    goalie_team_id = roster_goalie['team']['id']

    # Iterate over today's games to check if the goalie is playing
    for game in games.get('games', []):
        # Check if the goalie's team is either the home or away team in the game
        if game['home_team']['id'] == goalie_team_id or game['away_team']['id'] == goalie_team_id:
            # Log that the goalie is playing today
            logger.info(
                "Goalie %s %s is playing today for team %s.",
                roster_goalie['firstname'], roster_goalie['lastname'],
                roster_goalie['team']['name']
            )
            slack_messaging.post_to_slack(
                f"{roster_goalie['firstname']} {roster_goalie['lastname']} spielt heute. "
                "Kein Handlungsbedarf."
            )
            return

    # If no match is found, log that the goalie is not playing today
    logger.info(
        "Goalie %s %s is not playing today.",
        roster_goalie['firstname'], roster_goalie['lastname']
    )
    slack_messaging.post_to_slack(
        f"{roster_goalie['firstname']} {roster_goalie['lastname']} sitzt heute auf der Bank, "
        "du solltest ihn auswechseln!"
    )
