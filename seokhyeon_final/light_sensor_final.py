import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

lit_sensor = 4

def rc_time(light_sensor):
    count = 0
    GPIO.setup(light_sensor, GPIO.OUT)
    GPIO.output(light_sensor, GPIO.LOW)
    time.sleep(0.5)
    GPIO.setup(light_sensor, GPIO.IN)
    while (GPIO.input(light_sensor) == GPIO.LOW):
        count += 1
    return count

light_count = rc_time(lit_sensor)
t = time.time()
time_local = time.localtime(t)
hour = time_local.tm_hour

def light_sensor():
    if ((hour > 10) and (rc_time(lit_sensor) < 50)): # Need to change time!
        #print("Go Home!") #speaker
        valid = 1
    else:
        #print("Stay here") #speker
        valid = 0
    return valid