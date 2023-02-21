import time
from types import CodeType
import numpy as np
import tensorflow as tf
from tensorflow import keras
# tnesorflow keras ：是把艱深的tnesorflow library 包裝成較好理解的API
from tensorflow.keras.models import load_model
import cv2



def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def main(label_path, model_path, img_name):
    labels = load_labels(label_path) 
    model = load_model(model_path, compile=False) 
    print("Model Loaded Successfully.")

    _, height, width, channel = model.layers[0].output_shape[0]
    print("Required input Shape ({}, {}, {})".format(height, width, channel))

    # load image for inference
    image_show = cv2.imread(img_name)
    image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)

    # 黑白圖片
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret , thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # image = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2RGB)
    # cv2.imwrite("black-white.jpg", image)

    # 上下左右翻轉
    image = cv2.flip(image, -1)

    # # 加入雜訊：
    noise = np.random.normal(0, 0.1, image.shape)
    print(noise[0][0][0])
    print(image[0][0][0])
    gaussian_out = image/255 + noise
    # *所有值介於0~1之間
    gaussian_out = np.clip(gaussian_out, 0, 1)
    gaussian_out = np.uint8(gaussian_out*255)
    image = gaussian_out
    image2 = np.uint8(image)
    cv2.imwrite("HW3-2.jpg", image2)

    
    #  加入方框：
    # image = cv2.rectangle(image, (127, 80), (255, 127), (0, 255, 0), -1)
    # cv2.imwrite("Rectangle.jpg", image)

    # 水平翻轉：
    # image = cv2.flip(image, 1) 
    # cv2.imwrite("Flipped-Horizonal.jpg", image)

    # 垂直翻轉：
    # image = cv2.flip(image, 0)
    # cv2.imwrite("Flipped-Vertucal.jpg", image)


    

    
    image = cv2.resize(image, (width, height))
    image = image / 255.0
    image = np.reshape(image, (1, height, width, channel))

    
    # run inference on input image
    # predict()：模型中用來預測，返回數值，表示樣本屬於每一個類別的概率
    results = model.predict(image)[0]  # inference first time
    start_time = time.time()
    results = model.predict(image)[0]  # inference second time
    stop_time = time.time()
   
    label_id = np.argmax(results)
    prob = results[label_id]

    # print predict result~
    print(50 * "=")
    print("Object in {} is a/an...".format(img_name))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")
    print("Time spend: {:.5f} sec.".format(stop_time - start_time))


if __name__ == "__main__":
    print(tf.__version__) # 印出tensorflow安裝版本
    label_path = 'model/cifar10_label.txt' # 前面要有modle/是因為放在modle的資料夾裡面
    model_path = 'model/cifar10_mobilenetv2.h5'
    img_name = 'catdog_subset\cat2.jpg'  # <- you can change to any other test sample in "cifar10_subset" folder
    main(label_path, model_path, img_name)
    print('Bye')