import blescan
import sys
import math
import bluetooth._bluetooth as bluez
import time

dev_id = 0
sock = bluez.hci_open_dev(dev_id)
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
distance_count = 0

def testblescan():
	global distance_count
	returnedList = blescan.parse_events(sock, 10)
	valid = 0
	for beacon in returnedList:
		if beacon[18:50] == "e2c56db5dffb48d2b060d0f5a71096e0":
			txpower_s = beacon[56:58]
			txpower = int(txpower_s) + 1
			rssi_s = beacon[60:62]
			rssi = int(rssi_s) + 1
			distance = pow(10, ((rssi-txpower)/20.0))
			#print (beacon)
			print ("The distance is %fm" % distance)
			if distance > 15.0:
				distance_count = distance_count + 1
			else:
				distance_count = 0
			if (distance_count > 2):
				#print ("It's too far!") #speaker
				valid = 1
			else:
				#print("You're here") #speaker
				valid = 0
	return valid