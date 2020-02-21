#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

lower_purple = np.array([-10, 100, 100])
upper_purple = np.array([10, 255, 255])
#Height = 640
#Width = 480
points = []

class image_converter:
	

	def __init__(self):
		self.image_pub1 = rospy.Publisher("image_topic_1",Int32,queue_size=10)
		self.image_pub2 = rospy.Publisher("image_topic_2",Int32,queue_size=10)

		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/raspicam_node/image",Image,self.callback)

	def callback(self,data):
		try:
			
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		(rows,cols,channels) = cv_image.shape
		if cols > 60 and rows > 60 :
      #cv2.circle(cv_image, (50,50), 10, 255)
			con_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(con_image, lower_purple, upper_purple)
			_, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			center =   int(cols/2), int(rows/2)
			if len(contours) > 0:
				c = max(contours, key=cv2.contourArea)
				(x, y), radius = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
		  
				try:
				
					center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				except:
					center =   int(cols/2), int(rows/2)
				if radius > 25:
					cv2.circle(cv_image, (int(x), int(y)), int(radius),(0, 0, 255), 2)
					cv2.circle(cv_image, center, 5, (0, 255, 0), -1)
					detect_frame = cv_image.copy()
			points.append(center)
			print(center)
			print(center[0])
			print(center[1])
			x_axis=center[0]
		
			  
			
			  
			 
		  
      

		#cv2.imshow("Image window", cv_image)
		#cv2.waitKey(3)

		try:
			#self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
			self.image_pub1.publish(center[0])
			self.image_pub2.publish(center[1])
			
		except CvBridgeError as e:
			print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
