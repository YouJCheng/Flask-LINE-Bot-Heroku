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
            url='https://zh.wikipedia.org/wiki/Google_Chrome#/media/File:Google_Chrome_icon_(September_2014).svg',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(uri='http://google.com', label='Google')
        )
    )
)
carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    ),
                    URIAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)
location_message = LocationSendMessage(
    title='Tokyo',
    address='Tokyo',
    latitude=35.65910807942215,
    longitude=139.70372892916203
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
    elif get_message == 'carousel':
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif get_message == 'quick':
        text_message = TextSendMessage(text=f"{get_message}",
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="A", text="快速回復A")),
                                    QuickReplyButton(action=MessageAction(label="B", text="快速回復B")),
                                   QuickReplyButton(action=MessageAction(label="C", text="快速回復C")),
                               ]))  
        line_bot_api.reply_message(event.reply_token, text_message)
    elif get_message == 'location':
        line_bot_api.reply_message(event.reply_token, location_message)
    else:
        reply = TextSendMessage(text=f"{get_message}") 
        line_bot_api.reply_message(event.reply_token, text_message)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    # Send To Line
    reply = TextSendMessage(text=f"{message_id}")
    line_bot_api.reply_message(event.reply_token, reply)

