from slack_sdk import WebClient

SLACK_API_TOKEN = "xoxb-1966984563746-3928276940790-f2jbvGy9NkNlLJiXZW31RifV"
CHANNEL = "#buy-data"

def send_message( message ):
    client = WebClient( token = SLACK_API_TOKEN )
    client.chat_postMessage(channel = CHANNEL, text = message )
