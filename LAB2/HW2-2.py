import sys
import cv2
import cv2
import random
import time
import numpy as np


capture = cv2.VideoCapture('example.mp4')

fps = int(capture.get(cv2.CAP_PROP_FPS))
total_frame = int (capture.get(cv2.CAP_PROP_FRAME_COUNT))   # Amount of frames
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

CURSOR_UP_ONE = '\x1b[1A' # cursor 游標
ERASE_LINE = '\x1b[2K'

print('Start Processing...\n')



def mosaic_effect(img):
    new_img = img.copy()
    h = img.shape[0]
    w = img.shape[1]
    size = 10    # 馬賽克大小
    for i in range(size, h - 1 - size, size):
        for j in range(size, w - 1 - size, size):
            i_rand = random.randint(i - size, i)
            j_rand = random.randint(j - size, j)
            new_img[i - size:i + size, j - size:j + size] = img[i_rand, j_rand, :]
    return new_img

sum_t=0.0

while (True):
    time_start = time.time() #開始計時
    for i in range(total_frame):
        # Erase the last line in terminal
        # sys.stdout.write(CURSOR_UP_ONE) # stdout：標準輸出
        # sys.stdout.write(ERASE_LINE)
        print('progress: {} %'.format(round(((i + 1) / total_frame) * 100, 2)))
        # round():返回浮點小數值

        status, frame = capture.read()  # Read the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # 把BGR格式轉成gray_scale
        faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect the faces

        size = 10

        print("start convoltion")
        for (x, y, w, h) in faces:
            # 裁切圖片
            crop_img = frame[y:y+h, x:x+w]
            paste_img = mosaic_effect(crop_img)
            frame[y:y+h, x:x+w] = paste_img
            paste_img = mosaic_effect(crop_img) # 呼叫馬賽克涵式處理圖片
            frame[y:y+h, x:x+w] = paste_img # 把馬賽克處理好的圖片貼回圖片原本位置
            
        out.write(frame)
        
        
    capture.release()

    time_end = time.time()    #結束計時
    time_c= time_end - time_start   #執行所花時間
    print('time cost', time_c, 's')
