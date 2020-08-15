import cv2
import numpy as np
from PIL import Image
import os
import time


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

#face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
path = 'dataset'
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
#iniciate id counter
id = 0

# names related to ids: example ==> loze: id=1,  etc
names = ['0', '1', '2', '3', '4', '5']
face_id = 2

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    #if face_id >= 1:
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            print ("Hi there!") #speaker
            time.sleep(1)
        else:
            id = ("unknown")
            confidence = "  {0}%".format(round(100 - confidence))
            time.sleep(1)
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
    if id == "unknown":
        # if face_id == 0:
            # cv2.imshow('camera',img)
        print ("You are stranger") #speaker
        print ("You need to save your face") #speaker
        #face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        print ("Look at the camera") #speaker
        count = 0
        while True:
            #ret, img = cam.read()
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces2 = faceCascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces2:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                #Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
                cv2.destroyWindow('image')
            #k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            #if k == 27:
                #break
            if count >= 30: # Take 30 face sample and stop video
                break
        #path = 'dataset'
        #recognizer = cv2.face.LBPHFaceRecognizer_create()
        #def getImagesAndLabels(path):
            #imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            #faceSamples=[]
            #ids = []
            #for imagePath in imagePaths:
                #PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                #img_numpy = np.array(PIL_img,'uint8')
                #id1 = int(os.path.split(imagePath)[-1].split(".")[1])
                #faces3 = face_detector.detectMultiScale(img_numpy)
                #for (x,y,w,h) in faces3:
                    #faceSamples.append(img_numpy[y:y+h,x:x+w])
                    #ids.append(id1)
            #return faceSamples,ids
        print ("Training faces...") #speaker
        faces3,ids = getImagesAndLabels(path)
        recognizer.train(faces3, np.array(ids))
        recognizer.write('trainer/trainer'+ str(face_id) +'.yml')
        recognizer.read('trainer/trainer'+ str(face_id) +'.yml')
        print("{0} faces trained.".format(len(np.unique(ids))))
        face_id = face_id + 1
        print ("It's done!") #speaker
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
#print("\n [INFO] Exiting Program and cleanup stuff")
#cam.release()
#cv2.destroyAllWindows()
