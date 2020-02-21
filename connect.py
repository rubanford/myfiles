'''
import os

print(os.getcwd())
f = os.getcwd()
list1 = os.listdir(f)
print(list1)
''' 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import tensorflow as tf 
from tensorflow import keras
#from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
from scipy import misc

new_model = tf.keras.models.load_model('/home/ford/Desktop/with10epochs.h5')

##test_img = 'datasets/testing.jpg' 


def machine(img,Height,Width,radius,center):


##    test_img = image.load_img(img,target_size=(100,100))
    test_img = misc.imresize(img,(100,100))
    
    test_size = image.img_to_array(test_img)


    test_img = np.expand_dims(test_img,axis=0)

    test_img = test_img/255

    pvalue =  new_model.predict(test_img)

    pclass = new_model.predict_classes(test_img)

    if pvalue > 0.8 :
        
        print(pclass)

##        print(pvalue)

        object_center = center

        camer_center =   int(Width/2), int(Height/2)
        try:
            move = math.sqrt(int(math.pow(camer_center[0] - object_center[0]),2) + nt(math.pow(camer_center[1] - object_center[1]),2))
            print(move)
        except:
            pass
       
    else:
        print('no tomato')
        print(center)

cap = cv2.VideoCapture(0)

lower_purple = np.array([-10, 100, 100])
upper_purple = np.array([10, 255, 255])

points = []


ret, frame = cap.read()
detect_frame = frame.copy()
Height, Width = frame.shape[:2]
frame_count = 0

while True:
    test_img1 = 'datasets/testing.jpg' 
    ret, frame = cap.read()
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_purple, upper_purple)
    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center =   int(Height/2), int(Width/2)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        except:
            center =   int(Height/2), int(Width/2)
        if radius > 25:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            detect_frame = frame.copy()
            machine(detect_frame,Height,Width,radius,center)

    points.append(center)

            

    frame = cv2.flip(frame, 1)
    cv2.imshow("Object Tracker", frame)

    if cv2.waitKey(1) == 27: 
        break


cap.release()
cv2.destroyAllWindows()

