import light_sensor_final
import distance_sensor_final
import camera_final
import testblescan_final
import threading
import concurrent.futures # pip install futures
import time
import commands
import sys
import emotion_recog
import touch_sensor
import random

t = time.time()
time_local = time.localtime(t)
minute = time_local.tm_min

print("Okay, let's start!")

while True:
	threads = []

	thread_light_sensor = threading.Thread(target = light_sensor_final.light_sensor)
	threads.append(thread_light_sensor)
	valid_light = thread_light_sensor.start()

	thread_distance_sensor = threading.Thread(target = distance_sensor_final.distance_sensor)
	threads.append(thread_distance_sensor)
	valid_distance = thread_distance_sensor.start()

	thread_testblescan = threading.Thread(target = testblescan_final.testblescan)
	threads.append(thread_testblescan)
	valid_ble = thread_testblescan.start()

	thread_face_detect = threading.Thread(target = camera_final.face_detect)
	threads.append(thread_face_detect)
	valid_face = thread_face_detect.start()

	thread_touch = threading.Thread(target = touch_sensor.touch)
	threads.append(thread_touch)
	valid_touch = thread_touch.start()

	#print (threading.active_count())

	for x in threads:
		x.join()

	#print (threading.active_count())

	with concurrent.futures.ThreadPoolExecutor() as executor:
		valid_light = executor.submit(light_sensor_final.light_sensor).result()
		valid_distance = executor.submit(distance_sensor_final.distance_sensor).result()
		valid_ble = executor.submit(testblescan_final.testblescan).result()
		valid_face = executor.submit(camera_final.face_detect).result()
		valid_touch = executor.submit(touch_sensor.touch).result()

	if valid_light == 1:
		#print("Go home!") #speaker
		commands.getstatusoutput("aplay " + "go_home.wav")
		time.sleep(4)
	else:
		print("Stay here")

	if valid_distance == 1:
		#print("Put that away!") #speaker
		commands.getstatusoutput("aplay " + "put_that_away.wav")
		time.sleep(3)
	else:
		print("Go straight")

	if valid_ble == 1:
		#print ("It's too far!") #speaker
		commands.getstatusoutput("aplay " + "its_too_far.wav")
		time.sleep(3)
	else:
		print("You're here")

	if valid_face == 1:
		#print ("Hi there!") #speaker
		commands.getstatusoutput("aplay " + "hi_there.wav")
		time.sleep(4)
	elif valid_face == -1:
		#print ("You are stranger") #speaker
		#print ("You need to save your face") #speaker
		#print ("Look at the camera") #speaker
		commands.getstatusoutput("aplay " + "save_face.wav")
		time.sleep(5)
		camera_final.face_detect_add()
		#print ("It's done") #speaker
		commands.getstatusoutput("aplay " + "its_done.wav")
		time.sleep(4)
	else:
		print ("Nobody's here")

	if valid_touch == 1:
		files = os.listdir(/home/pi/gyuri/meow)
		file = random.choice(files)
		commands.getstatusoutput("aplay " + file)
		time.sleep(5)
	else:
		print("No touch")

	if minute % 10 == 0:
		commands.getstatusoutput("aplay " + "your_emotion.wav")
		time.sleep(3)
		emotion_recog.emotion()
		time.sleep(65)

	print("-------------")