from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Dein Slack Bot-Token
SLACK_TOKEN = "xxx"
client = WebClient(token=SLACK_TOKEN)

try:
    response = client.chat_postMessage(
        channel='xxxxx',  # Channel ID oder Name mit '#'
        text="Hallo, dies ist eine Nachricht über die API"
    )
except SlackApiError as e:
    print(f"Fehler: {e.response['error']}")
