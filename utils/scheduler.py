"""Module providing a function to schedule tasks."""

from datetime import datetime
import time
import schedule
import pytz

def schedule_task(func, time_str, *args, **kwargs):
    """Function to schedule a task at a specific time."""
    def wrapped_func():
        cet = pytz.timezone('Europe/Zurich')  # CET Zeitzone festlegen
        now = datetime.now(cet)
        print(f"Der API-Call wurde gestartet um {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # Ausführung der übergebenen Funktion
        func(*args, **kwargs)

    # Den Zeitplan festlegen
    schedule.every().day.at(time_str).do(wrapped_func)

    # Endlos-Schleife, die den Zeitplan überwacht und bei Bedarf die Funktion ausführt
    while True:
        schedule.run_pending()  # Führt geplante Aufgaben aus
        time.sleep(60)  # Warten für 1 Minute, um die CPU zu entlasten
