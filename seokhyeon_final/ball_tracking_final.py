import numpy as np
import imutils
import cv2

def ball_tracking ():
	before_x = 250
	before_y = 175

	# define the lower and upper boundaries of the "yellow object" (or "ball") in the HSV color space, then initialize the list of tracked points
	colorLower = (80, 100, 100)
	colorUpper = (100, 255, 255)

	# grab the reference to the webcam
	camera = cv2.VideoCapture(0)

	# keep looping
	#while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	#frame = cv2.flip(frame, -1)

	# resize the frame, inverted ("vertical flip" w/ 180degrees), blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	frame = imutils.rotate(frame, angle=180)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform a series of dilations and erosions to remove any small blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			if (before_x - int(x) > 10):
				#print("Left")
				valid_x = -1
			elif (before_x - int(x) < 10):
				#print("Right")
				valid_x = 1
			else:
				#print("Same")
				valid_x = 0
			if (before_y - int(y) > 10):
				#print("Down")
				valid_y = -1
			elif (before_y - int(y) < 10):
				#print("Up")
				valid_y = 1
			else:
				#print("Same")
				valid_y = 0
			before_x = int(x)
			before_y = int(y)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(10) & 0xFF # if the 'ESC' key is pressed, stop the loop
	if key == 27:
		break
	
	return valid_x, valid_y