"""Module providing a function to schedule tasks."""

from datetime import datetime
import time
import schedule
import pytz
from utils.logger import logger
from services.login import get_jwt_token
from services.roster import get_roster  # Importiere die api_call-Funktion

# Zeitzone für CET festlegen
def schedule_api_call(token):
    """Function providing a schdule for API-calls."""
    cet = pytz.timezone('Europe/Zurich')  # CET Zeitzone festlegen
    now = datetime.now(cet)
    print(f"Der API-Call wurde gestartet um {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Hier den API-Aufruf machen
    get_roster(token)

# Zeitplan erstellen
schedule.every().day.at("19:00").do(schedule_api_call)

# Endlos-Schleife, die den Zeitplan überwacht und bei Bedarf die Funktion ausführt
while True:
    schedule.run_pending()  # Führt geplante Aufgaben aus
    time.sleep(60)  # Warten für 1 Minute, um die CPU zu entlasten

if __name__ == '__main__':
    jwt_token = get_jwt_token()
    if jwt_token:
        schedule_api_call(jwt_token)
    else:
        logger.error('Kein JWT-Token erhalten, Abbruch.')
        