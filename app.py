import os
from datetime import datetime
# 利用 route 處理路由
from flask import Flask, abort, request

# 初始化LINT BOT
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

# 利用 handler 處理 LINE 觸發事件
from linebot.models import *


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    get_message = event.message.text
    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    if 
    line_bot_api.reply_message(event.reply_token, reply)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    # Send To Line
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)

