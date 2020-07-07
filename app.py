import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import logging

from config import Channel_Access_Token, Channel_Secret
from handler import line_reply_handler

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)



## MESSENGER
from pymessenger import Bot
PAGE_ACCESS_TOKEN="EAAIXsvACy2QBAOZBOdvLVGTOQ2NNZBYNCe94g4qWylFYguZCu9H6oov2xXKpDkMhZBgRZC94kVnY8AhXCaZCXGdJ95ezWvvo9BtQcL7SHSDrZCJB60HBZAa2VZAFqXVPnA8gVrZAPKDdsMQirqAB2u13EZCkyqDJbZBHHDrHODVHl0oWPaZBBE1h7Jl5O"
MESSENGER_AUTH_TOKEN = "messenger_auth_token"
bot = Bot(PAGE_ACCESS_TOKEN)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/messenger", methods=['GET'])
def verify():
 # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == MESSENGER_AUTH_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route("/callback/messenger", methods=['POST'])
def webhook():
    data = request.get_json()
    app.logger.info("postback: " + str(data))
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                    # Echo
                    response = messaging_text
                    bot.send_text_message(sender_id, messaging_text)
    return "ok", 200



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

