# import the necessary packages
#from collections import deque
import numpy as np
#import argparse
import imutils
import cv2

before_x = 127
before_y = 127
left = 0
right = 0
down = 0
up = 0
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video",
#	help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=32,
#	help="max buffer size")
#args = vars(ap.parse_args())

def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (80, 100, 100)
colorUpper = (100, 255, 255)
#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
#else:
#	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	frame = cv2.flip(frame, -1)
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	#if args.get("video") and not grabbed:
	#	break
 
	# resize the frame, inverted ("vertical flip" w/ 180degrees),
	# blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	frame = imutils.rotate(frame, angle=180)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			left = 0
			right = 0
			down = 0
			up = 0
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			mapObjectPosition(int(x), int(y))
			if (before_x - int(x) > 0):
				left = 1
				print("Left")
			elif (before_x - int(x) < 0):
				right = 1
				print("Right")
			else:
				print("Same")
			if (before_y - int(y) > 0):
				down = 1
				print("Down")
			elif (before_y - int(y) < 0):
				up = 1
				print("Up")
			else:
				print("Same")
			before_x = int(x)
			before_y = int(y)
			
	# update the points queue
	#pts.appendleft(center)
	
		# loop over the set of tracked points
	#for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		#if pts[i - 1] is None or pts[i] is None:
		#	continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		#thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		#cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(10) & 0xFF
 
	# if the 'ESC' key is pressed, stop the loop
	if key == 27:
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
