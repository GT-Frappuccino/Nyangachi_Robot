import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

light_sensor = 4

def rc_time (light_sensor):
    count = 0
  
    GPIO.setup(light_sensor, GPIO.OUT)
    GPIO.output(light_sensor, GPIO.LOW)
    time.sleep(0.5)

    GPIO.setup(light_sensor, GPIO.IN)
  
    while (GPIO.input(light_sensor) == GPIO.LOW):
        count += 1

    return count

light_count = rc_time(light_sensor)

t = time.time()
time_local = time.localtime(t)
hour = time_local.tm_hour

try:
    while True:
        if ((hour > 14) and (rc_time(light_sensor) < 50)) :
           print("Go Home") # spreker
           print rc_time(light_sensor)
        else : 
            print("It's Okay")
            print rc_time(light_sensor)
except KeyboardInterrupt:
    pass
finally: GPIO.cleanup()
    
