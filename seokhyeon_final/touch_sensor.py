import RPi.GPIO as g
import time

IN_TOUCH = 4 # GPIO 4

g.setmode(g.BCM)

g.setup(IN_TOUCH, g.IN)

g.add_event_detect(IN_TOUCH, g.BOTH)

def touch (arg1):
   value = g.input(arg1)
   print "Touch" + "GPIO Value : "+str(value)
   return value
   #if value == 1:
      # from omxplayer.player import OMXPlayer
      # from pathlib import Path
      #from time import sleep
      #import commands
      #import sys 

      # AUDIO_PATH = Path("/home/pi/gyuri/meow1.wav")

      # player = OMXPlayer(AUDIO_PATH)

      #import random

      
      #files=os.listdir(/home/pi/gyuri/meow)
      #file=random.choice(files)

      #if len(sys.argv) > 1:
      #   file = sys.argv[1]


      


      #player.quit()
   
      
#g.add_event_callback(IN_TOUCH, sensorCallback)
#print "Start"
#try:
#   while True:
#      time.sleep(1)

#except KeyboardInterrupt:
#   print "Keyboard Interrupt"

#except:
#   print "other error"

#finally:
#   g.cleanup()