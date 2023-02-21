# 使用者註冊後，回傳給使用者"sucess"，偵測到人臉拍照傳給使用者
from __future__ import unicode_literals

import sys
import time
import cv2
import random
from random import randint
import json
import threading
import configparser
import numpy as np



from picamera.array import PiRGBArray

from picamera import PiCamera
from flask import Flask, request, abort, make_response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 宣告一個flask物件
app = Flask(__name__)


# get config values from config.ini
config = configparser.ConfigParser()
config.read('config.ini')


# initialize objects related to line-bot-sdk
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'), timeout=3000)
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

USER_LIST_FILE = './user.json'


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

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face detector
def detector(filename):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    # 判斷有沒有人臉
    if len(faces) == 0:
        detect = False
    else:
        detect = True

    return detect


# rectangle
def rectangle(filename):
    img = cv2.imread("{}".format(filename))
    cv2.putText(img, 'detect', (10, 30), cv2.FONT_HERSHEY_PLAIN, \
            3, (0, 255, 0), 3, cv2.LINE_AA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)    # 新增矩形圖案

    cv2.imwrite("capture.jpg", img) 

    

@app.route('/picamera/<counter>', methods=['GET'])
def picamera_image(counter):
    while True:
        try:
            rectangle('capture.jpg')
            image_data = open('capture.jpg', 'rb').read()
            print("1")
            response = make_response(image_data)
            print('3')
            response.headers['Content-Type'] = 'image/jpg'
            return response

        except Exception as e:
            print(e)


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # enroll as a user
    if event.message.text == 'enroll':
        print('got a \"enroll\" message')

        # append current user id into user_list file
        with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
            user_list = json.load(file)
        user_list.append(event.source.user_id)
        user_list = list(set(user_list))
        with open(USER_LIST_FILE, 'w', encoding='utf-8') as file:
            json.dump(user_list, file, ensure_ascii=False, indent=4)

        # reply success message
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='success'))
        # 呼叫auto_photo()函式
        auto_photo()

def auto_photo():
    print('start detection') 
    try:
        content = False
        camera = PiCamera()
        camera.resolution = (320, 240)
        while not content:
            camera.capture('capture.jpg')    # 拍照並儲存至 foo.jpg
            img = cv2.imread('capture.jpg')
            cv2.imshow('capture.jpg', img)   # 將 img 輸出至視窗
            cv2.waitKey(1000)
            camera.close()
            content = True
            print("start detecting")
            detected = detector('capture.jpg')
            print("decting")

            if detected == True:
                print('detected faces')

                random_num = randint(0, sys.maxsize)
                with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
                    user_list = json.load(file)
                for user_id in user_list:
                    line_bot_api.push_message(user_id,
                        TextSendMessage(text='detected someone appeared in front of your RPi'))
                    line_bot_api.push_message(user_id,
                        ImageSendMessage(
                            original_content_url=config.get('ngrok', 'server_name') + '/picamera/{}'.format(str(random_num)), 
                            preview_image_url=config.get('ngrok', 'server_name') + '/picamera/{}'.format(str(random_num))
                        )
                    )
                print("picamera take a break")
                content = False
               #camera.close()
                    
            else:
                content = False
                detected = False
                print("no one is infront of your camera")


    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit()

    except Exception as e:
        print(e)
 

if __name__ == '__main__':
    try:
        with open(USER_LIST_FILE, 'r', encoding='utf-8') as file:
            user_list = json.load(file)
        if type(user_list) != list:
            raise TypeError()
    except:
        with open(USER_LIST_FILE, 'w', encoding='utf-8') as file:
            json.dump(list(), file, ensure_ascii=False, indent=4)
    finally:
        # threading.Thread(target=auto_photo).start()
        app.run(debug=False, port=5000)

# todo 
# (1) 連線picamera
# (2) 偵測人臉
# (3) 偵測到人臉傳送資料

# tasks
# (1) 回傳圖片人臉要標方框
# 先寫一個方框函式在外面，
# 判斷有沒有人臉，有人臉呼叫方框函式，產生圖片url，push message
# 沒有人臉print("no one")
# (2) 圖片要怎麼直接產生url回傳
# 找一下google