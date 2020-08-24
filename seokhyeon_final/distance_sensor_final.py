import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 13
echo = 6
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def distance_sensor():
  GPIO.output(trig, False)
  time.sleep(0.5)
  GPIO.output(trig, True)
  time.sleep(0.00001)
  GPIO.output(trig, False)
  while GPIO.input(echo) == False:
    pulse_start = time.time()
  while GPIO.input(echo) == True:
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17000
  distance = round(distance, 2)
  if distance < 10:
    #print ("Put that away!") #speaker
    valid = 1
  else:
    #print("Go straight") #speaker
    valid = 0
  return valid