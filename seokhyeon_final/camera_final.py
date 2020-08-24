import cv2
import numpy as np
from PIL import Image
import os
import imutils
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml");

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id2 = int(os.path.split(imagePath)[-1].split(".")[1])
        faces3 = faceCascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces3:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id2)
    return faceSamples,ids

def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))

id = 0 # iniciate id counter
names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # names related to ids

def face_detect():
    ret, img = cam.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)),)
    valid = 0
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            #confidence = "  {0}%".format(round(100 - confidence))
            #print ("Hi there!") #speaker
            valid = 1
        else:
            id = ("unknown")
            #confidence = "  {0}%".format(round(100 - confidence))
            valid = -1
    #cv2.imshow('camera',img)
    return valid

face_id = 2
path = 'dataset'

def face_detect_add():
    global face_id
    count = 0
    while True:
        ret2, img2 = cam.read()
        img2 = cv2.flip(img2, -1)
        gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        faces2 = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces2:
            cv2.rectangle(img2, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            #cv2.imshow('image', img2)
            #cv2.destroyWindow('image')
        if count >= 30: # Take 30 face sample and stop video
            break
    faces3,ids = getImagesAndLabels(path)
    recognizer.train(faces3, np.array(ids))
    recognizer.write('trainer/trainer'+ str(face_id) +'.yml')
    recognizer.read('trainer/trainer'+ str(face_id) +'.yml')
    #print ("{0} faces trained.".format(len(np.unique(ids))))
    face_id = face_id + 1
    #cv2.imshow('camera2',img)

flag = 0
before_x = 250
before_y = 175

def ball_tracking():
    global flag
    global before_x
    global before_y
    # define the lower and upper boundaries of the "yellow object" (or "ball") in the HSV color space, then initialize the list of tracked points
    colorLower = (80, 100, 100)
    colorUpper = (100, 255, 255)
    # grab the current frame
    (grabbed, frame2) = cam.read()
    frame = frame2 [40:280, 100:380]
    frame = cv2.flip(frame, -1)
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
    if flag == 0:
        before_x = 250
        before_y = 175
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if (radius > 10) and (radius < 20):
            flag = 1
            # draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            mapObjectPosition(int(x), int(y))
            if (before_x - int(x) > 10):
                #print ("Left")
                valid_x = -1
            elif (before_x - int(x) < 10):
                #print ("Right")
                valid_x = 1
            else:
                #print ("X is Same")
                valid_x = 0
            if (before_y - int(y) > 10):
                #print ("Down")
                valid_y = -1
            elif (before_y - int(y) < 10):
                #print ("Up")
                valid_y = 1
            else:
                #print ("Y is Same")
                valid_y = 0
            before_x = int(x)
            before_y = int(y)
        else:
            flag = 0
            valid_x = 0
            valid_y = 0
    else:
        flag = 0
        valid_x = 0
        valid_y = 0
    #cv2.imshow("frame", frame)
    return [valid_x, valid_y]