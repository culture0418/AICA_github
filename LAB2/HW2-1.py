from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import os

camera = PiCamera()
camera.resolution = (320, 240)

import time
from datetime import datetime
## %H????
filename = datetime.now().strftime("%m%d_%H%M")
print(filename)

import RPi.GPIO as GPIO
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(COUNTER_PIN, GPIO.IN)


try:    
    with PiRGBArray(camera) as output:
        for foo in camera.capture_continuous(output, 'bgr', use_video_port=True): # 透過 for loop 連續讀取影像，每跑一個迴圈都會獲得一張新影像
            img = output.array
            img = cv2.rotate(img, cv2.ROTATE_180) # 旋轉圖片（依相機實際擺設方向而定）
            cv2.imshow('capture', img) # 顯示影像
            cv2.waitKey(10) # 和 time.sleep() 雷同
            output.truncate(0) # 只保留最後一張影像，以免過多影像塞爆暫存
            if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
                cv2.imwrite("captured.jpg", img)
                print(1)
            if  GPIO.input(COUNTER_PIN) == GPIO.HIGH: # 當按下GPIO接收到訊號，儲存影像當按下GPIO接收到訊號，儲存影像
                cv2.imwrite("captured.jpg", img)
                print(1) # debug
                net = cv2.dnn.readNetFromTorch('starry_night.t7') 
                net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

                img = cv2.imread("captured.jpg")
                h = img.shape[0]
                w = img.shape[1]
                print("already read img")
                # h:hight w：width

                # 把影像修改成神經網路可以使用的格式
                blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
                print("start transfer")

                net.setInput(blob)  # 把影像丟入模型做風格轉換
                out = net.forward() # 開始轉換
                out = out.reshape(3, out.shape[2], out.shape[3])
                out[0] += 103.939
                out[1] += 116.779
                out[2] += 123.68
                # out /= 255
                out = out.transpose(1, 2, 0)
                pre_savename = '/home/pi/Desktop/picture'
                outputimg = cv2.imwrite("/home/pi/Desktop/picture/{}.jpg".format(filename), out)
                # Path??
                path = os.path.join(pre_savename, "{}.jpg".format(filename))
                print("done")

except KeyboardInterrupt:
        print('interrupt')

finally:
        camera.close()
        cv2.destroyAllWindows()



