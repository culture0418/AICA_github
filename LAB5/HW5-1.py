# 偵測近物自動傳送照片
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from random import randint
import configparser

from picamera import PiCamera
from flask import Flask, request, abort, make_response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 宣告一個Flask物件
app = Flask(__name__)

# get config values from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# initialize objects related to line-bot-sdk
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'), timeout=3000)
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 在路徑'callbacl'被存取時，執行函式callback
@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route('/picamera/<counter>', methods=['GET'])
def picamera_image(counter):
    while True:
        try:
            camera = PiCamera()
            camera.start_preview()
            camera.capture('./image.jpg')
            camera.stop_preview()
            camera.close()
            
            break
        except Exception as e:
            print(e)

    image_data = open('./image.jpg', 'rb').read()
    # make_response()：產生一個HTTP response物件，用以自訂header等參數
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    

    return response
    


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # enroll as a user
    content = False
    if event.message.text == '即時影像' and not content:
        content = True
        random_num = randint(0, sys.maxsize)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=config.get('ngrok', 'server_name') + '/picamera/{}'.format(str(random_num)), 
                preview_image_url=config.get('ngrok', 'server_name') + '/picamera/{}'.format(str(random_num))
            )
        )


if __name__ == '__main__':
    app.run(debug=False, port=5000)
        
        
            
