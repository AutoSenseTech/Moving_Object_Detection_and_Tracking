#!/usr/bin/env python

import cv2
import numpy as np
import rospy
from move_target_track.msg import trackPara 
from move_target_track.msg import pid_input 
def track():
    #Capture from external USB webcam instead of the in-built webcam (shitty quality)
    cap = cv2.VideoCapture(0)

    #kernel window for morphological operations
    kernel = np.ones((5,5),np.uint8)

    #resize the capture window to 640 x 480
    ret = cap.set(3,640)
    ret = cap.set(4,480)

    #upper and lower limits for the color yellow in HSV color space
    lower_yellow = np.array([45,100,50])
    upper_yellow = np.array([75,255,255])
    pub = rospy.Publisher('error', pid_input, queue_size=10)
    rospy.init_node('track', anonymous=True)
    #rate = rospy.Rate(10)
    msg = pid_input()
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        frame = frame[:, :640, :]
        #Smooth the frame
        frame = cv2.GaussianBlur(frame,(11,11),0)
        #Convert to HSV color space
        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        else:
            continue

        #Mask to extract just the yellow pixels
        mask = cv2.inRange(hsv,lower_yellow,upper_yellow)

        #morphological opening
        mask = cv2.erode(mask,kernel,iterations=2)
        mask = cv2.dilate(mask,kernel,iterations=2)

        #morphological closing
        mask = cv2.dilate(mask,kernel,iterations=2)
        mask = cv2.erode(mask,kernel,iterations=2)

        #Detect contours from the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]


        if(len(cnts) > 0):
            #Contour with greatest area
            c = max(cnts,key=cv2.contourArea)
            #Radius and center pixel coordinate of the largest contour
            ((x,y),radius) = cv2.minEnclosingCircle(c)

            if radius > 5:
	    #Draw an enclosing circle
                cv2.circle(frame,(int(x), int(y)), int(radius),(0, 255, 255), 2)

	    #Draw a line from the center of the frame to the center of the contour
                cv2.line(frame,(320,240),(int(x), int(y)),(0, 0, 255), 1)
	    #Reference line
                cv2.line(frame,(320,0),(320,480),(0,255,0),1)

                radius = int(radius)

	    #distance of the 'x' coordinate from the center of the frame
	    #wdith of frame is 640, hence 320
                length = 320-(int(x))
                msg.pid_vel = 0
                msg.pid_error = length
                rospy.loginfo(msg)
                pub.publish(msg)


    #Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    track()
