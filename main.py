from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langgraph.prebuilt import create_react_agent

import os

load_dotenv()

bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

if not bot_token or not app_token:
    raise ValueError(
        "Missing required environment variables: SLACK_BOT_TOKEN and/or SLACK_APP_TOKEN"
    )

app = App(token=bot_token)

@app.event("message")
def handle_message_events(body, logger):
    """Handle general message events."""
    logger.info(body)


@app.event("app_mention")
def handle_hello(body, say):
    event = body["event"]
    message = event["text"]
    thread_ts = event.get("thread_ts", event["ts"])

    agent = create_react_agent(
        model="openai:gpt-4o-mini",
        tools= []
    )
    response = agent.invoke({"messages": [{"role": "user", "content": message}]})
    text = response["messages"][-1].content

    say(text=text, thread_ts=thread_ts)

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
