# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
lower_purple = np.array([-10, 100, 100])
upper_purple = np.array([10, 255, 255])
points = []
Height=640
Width=420
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	con_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(con_image, lower_purple, upper_purple)
	_, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
			cv2.circle(image, (int(x), int(y)), int(radius),(0, 0, 255), 2)
			cv2.circle(image, center, 5, (0, 255, 0), -1)
			detect_frame = image.copy()
			#machine(detect_frame,Height,Width,radius,center)

	points.append(center)		
	# show the frame
	cv2.imshow("Frame", image)
	cv2.imshow("HSV", con_image)
	
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
#print(image)
