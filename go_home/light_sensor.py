import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit
light_sensor = 4

def rc_time (light_sensor):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(light_sensor, GPIO.OUT)
    GPIO.output(light_sensor, GPIO.LOW)
    time.sleep(1)

    #Change the pin back to input
    GPIO.setup(light_sensor, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(light_sensor) == GPIO.LOW):
        count += 1

    return count

light_count = rc_time(light_sensor)

t = time.time()
time_local = time.localtime(t)
hour = time_local.tm_hour

if ((hour > 14) && (light_count < 60)) :
    print("go home") # spreker

GPIO.cleanup()
