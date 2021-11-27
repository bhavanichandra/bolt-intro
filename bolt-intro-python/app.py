import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv("SLACK_BOT_TOKEN"))
SLACK_APP_TOKEN = str(os.getenv("SLACK_APP_TOKEN"))

logger = logging.getLogger(__name__)

app = App(logger=logger, token=SLACK_BOT_TOKEN)


@app.message("onboard")
def onboard_employee(message, say):
    user = message['user']
    say(
        text=f"Hey <@{user}>",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Click the button to start the process"
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Start OnBoarding"},
                    "action_id": "onboarding_action",
                    "style": "primary"
                }
            }
        ]
    )


@app.action("onboarding_action")
def onboarding_action(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> has started the process")


if __name__ == "__main__":
    SocketModeHandler(app, app_token=SLACK_APP_TOKEN).start()
