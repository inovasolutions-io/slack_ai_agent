from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

load_dotenv()

bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

if not bot_token or not app_token:
    raise ValueError(
        "Missing required environment variables: SLACK_BOT_TOKEN and/or SLACK_APP_TOKEN"
    )

app = App(token=bot_token)


@app.event("app_mention")
def handle_hello(body, say, client):
    event = body["event"]
    thread_ts = event.get("thread_ts", event["ts"])

    say(text="Processing...", thread_ts=thread_ts)

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
