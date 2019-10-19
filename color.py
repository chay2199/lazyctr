# Python program for Detection of a
# specific color(blue here) using OpenCV with Python
import cv2
import numpy as np
import pyautogui as mouse
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2

mouse.FAILSAFE = False

# Webcamera no 0 is used to capture the frames
cap = cv2.VideoCapture(0)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

# This drives the program into an infinite loop.
while(1):
     # Captures the live stream frame-by-frame
     _, frame = cap.read()
     # Converts images from BGR to HSV
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     lower_red = np.array([20, 110, 110])
     upper_red = np.array([50, 255, 255])

     # Here we are defining range of bluecolor in HSV
     # This creates a mask of blue coloured
     # objects found in the frame.
     mask = cv2.inRange(hsv, lower_red, upper_red)

     # The bitwise and of the frame and mask is done so
     # that only the blue coloured objects are highlighted
     # and stored in res
     res = cv2.bitwise_and(frame, frame, mask=mask)
     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
     if len(cnts) > 0:
         area = max(cnts, key=cv2.contourArea)
         (x, y, w, h) = cv2.boundingRect(area)
         cv2.rectangle(res, (x, y), (x+w, y+h), (255, 0, 0), 2)
         (p1, p2) = (int((2*x + w)/2), int((2*y + h)/2))
         cv2.circle(res, (p1, p2), 2, (0, 0, 255), 2)
         mouse.moveTo(p1*4, p2*3)
     cv2.imshow('frame', frame)
     cv2.imshow('mask', mask)
     cv2.imshow('res', res)

     # This displays the frame, mask
     # and res which we created in 3 separate windows.
     k = cv2.waitKey(5) & 0xFF
     if k == 27:
        break

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()

# release the captured frame
cap.release()
