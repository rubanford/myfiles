import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#cap = cv2.VideoCapture(0)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480)

time.sleep(0.1)

lower_purple = np.array([-10, 100, 100])
upper_purple = np.array([10, 255, 255])
points = []

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	frame_count = 0
	hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv_img, lower_purple, upper_purple)
	_, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        except:
			center=0
            
        if radius > 25:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
    
    points.append(center)
    cv2.imshow("Object Tracker", frame)

    key = cv2.waitKey(1) & 0xFF 
    rawCapture.truncate(0)
    
    if key == ord("q"):
		break    
    











