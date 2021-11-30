import os
import re
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

flex_message = FlexSendMessage(
    alt_text='hello',
    contents=BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url='https://example.com/cafe.jpg',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(uri='http://example.com', label='label')
        )
    )
)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if get_message == 'sticker':
        sticker_message = StickerSendMessage(
                package_id='1',
                sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif get_message == 'flex':
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        reply = TextSendMessage(text=f"{get_message}") 
        text_message = TextSendMessage(text=f"{get_message}",
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="label", text="text"))
                               ]))  
        line_bot_api.reply_message(event.reply_token, text_message)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    # Send To Line
    reply = TextSendMessage(text=f"{message_id}")
    line_bot_api.reply_message(event.reply_token, reply)

