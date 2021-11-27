import os
import logging
from slack_bolt import App
from datetime import datetime
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.context.say import Say
from slack_sdk.web.client import WebClient
from dotenv import load_dotenv
from slack_bolt.context.ack import Ack
from slack_sdk.models.views import View

load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv("SLACK_BOT_TOKEN"))
SLACK_APP_TOKEN = str(os.getenv("SLACK_APP_TOKEN"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = App(logger=logger, token=SLACK_BOT_TOKEN)


@app.event("app_home_opened")
def app_home_opened(client, event, logger):
    try:
        client.views_publish(user_id=event['user'],
                             view={"type": "home", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": f"<@{event['user']}> :tada: Welcome to Helpy, your app for all of your IT needs"}}, {"type": "divider"}, {"type": "header", "text": {"type": "plain_text", "text": "HR Features", "emoji": True}}, {"type": "section", "text": {"type": "mrkdwn", "text": "Onboard Employee"}, "accessory": {"type": "button", "style": "primary", "text": {"type": "plain_text", "text": ":office_worker: Add him", "emoji": True}, "value": "onBoard", "action_id": "onBoardNewEmployeeEvent"}}, {
                                 "type": "section", "text": {"type": "mrkdwn", "text": "Provision tools"}, "accessory": {"type": "button", "style": "primary", "text": {"type": "plain_text", "text": ":technologist: Get your tools here", "emoji": True}, "value": "provision", "action_id": "onProvisionAddEvent"}}, {"type": "section", "text": {"type": "mrkdwn", "text": "Notifications"}, "accessory": {"type": "button", "style": "primary", "text": {"type": "plain_text", "text": ":envelope_with_arrow: Register", "emoji": True}, "value": "provision", "action_id": "onNotificationTurnedOn"}}, {"type": "divider"}]}
                             )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.view("newEmployeeOnBoardView")
def handle_view_events(ack: Ack, body, client: WebClient, say: Say):
    ack()
    values = dict(body['view']['state']['values'])
    obj = {}
    for key, value in values.items():
        new_dict = dict(value)
        for _, action in new_dict.items():
            if action['type'] == "plain_text_input":
                obj[key] = action['value']
            if action['type'] == "datepicker":
                obj[key] = action['selected_date']
    resp = client.conversations_open(users=body['user']['id'])
    channel = resp.data['channel']
    date_of_birth = datetime.strptime(obj.get('dob'), '%Y-%m-%d')
    

    say(
        text="Data submitted and sent to backend systems",
        channel=channel['id'],
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f"Hey <@{body['user']['id']}>, The following is the data you submitted during onboarding process of Ravi."}, "fields": [{"type": "mrkdwn", "text": f"*Employee Name*:\n {obj.get('name')}"}, {
                "type": "mrkdwn", "text": f"*Email*: \n {obj.get('email')}"}, {"type": "mrkdwn", "text": f"*Date of Birth*: \n {date_of_birth.strftime('%B %d, %Y')}"}, {"type": "mrkdwn", "text": f"*Submission Date*: \n {datetime.today().strftime('%B %d, %Y')}"}]}
        ])


@app.action("onBoardNewEmployeeEvent")
def new_employee_onboard(ack: Ack, body, client: WebClient):
    try:
        ack()
        client.views_open(trigger_id=body['trigger_id'],
                          view={
                              "type": "modal",
                              "callback_id": "newEmployeeOnBoardView",
                              "title": {"type": "plain_text", "text": "New Employee Onboarding"},
                              "submit": {"type": "plain_text", "text": "OnBoard"},
                              "close": {"type": "plain_text", "text": "Close"},
                              "blocks": [{"block_id": "name", "type": "input", "element": {"type": "plain_text_input", "action_id": "nameAction", "placeholder": {"type": "plain_text", "text": "Enter Employee's Full Name", "emoji": True}}, "label": {"type": "plain_text", "text": "Employee Name", "emoji": True}}, {"type": "input", "block_id": "email", "element": {"type": "plain_text_input", "action_id": "emailAction", "placeholder": {"type": "plain_text", "text": "Enter Employee's Email", "emoji": True}}, "label": {"type": "plain_text", "text": "Employee Personal Email", "emoji": True}}, {"type": "input", "block_id": "dob", "element": {"type": "datepicker", "placeholder": {"type": "plain_text", "text": "Enter Employee Date of Birth", "emoji": True}, "action_id": "dobAction"}, "label": {"type": "plain_text", "text": "Employee DOB", "emoji": True}}]
        })
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("onboarding_action")
def onboarding_action(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> has started the process")


if __name__ == "__main__":
    SocketModeHandler(app, app_token=SLACK_APP_TOKEN).start()
