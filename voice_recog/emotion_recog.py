# Call syntax:
#   python3 measure_wav_linux32.py path_to_sound_file.wav

import sys
import scipy.io.wavfile
import commands
import time
from time import sleep

sys.path.append("../api")
import Vokaturi

print ("Loading library...")
Vokaturi.load("../lib/Vokaturi_linux32.so")
print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

print("Now recording...")
commands.getstatusoutput("arecord -D hw:1,0 -f S16_LE -d 5 -r 44100 /home/pi/gyuri/vokaturi/emotion.wav")

print ("Reading sound file...")
file_name = "/home/pi/gyuri/vokaturi/emotion.wav"
(sample_rate, samples) = scipy.io.wavfile.read(file_name)
print ("   sample rate %.3f Hz" % sample_rate)

print ("Allocating Vokaturi sample array...")
buffer_length = len(samples)
print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.SampleArrayC(buffer_length)
if samples.ndim == 1:
	c_buffer[:] = samples[:] / 32768.0
else:
	c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

print ("Creating VokaturiVoice...")
voice = Vokaturi.Voice (sample_rate, buffer_length)

print ("Filling VokaturiVoice with samples...")
voice.fill(buffer_length, c_buffer)

print ("Extracting emotions from VokaturiVoice...")
quality = Vokaturi.Quality()
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.extract(quality, emotionProbabilities)

if quality.valid:
	print ("Neutral: %.3f" % emotionProbabilities.neutrality)
	print ("Happy: %.3f" % emotionProbabilities.happiness)
	print ("Sad: %.3f" % emotionProbabilities.sadness)
	print ("Angry: %.3f" % emotionProbabilities.anger)
	print ("Fear: %.3f" % emotionProbabilities.fear)

	emotion = max(emotionProbabilities.neutrality, emotionProbabilities.happiness, emotionProbabilities.sadness, emotionProbabilities.anger, emotionProbabilities.fear)

	if emotion == emotionProbabilities.neutrality:
		files=os.listdir(/home/pi/gyuri/neutrality)
    	file=random.choice(files)
		commands.getstatusoutput("aplay " + file)

	elif emotion == emotionProbabilities.happiness:
		files=os.listdir(/home/pi/gyuri/happiness)
    	file=random.choice(files)
		commands.getstatusoutput("aplay " + file)
	
	elif emotion == emotionProbabilities.sadness:
		files=os.listdir(/home/pi/gyuri/sadness)
    	file=random.choice(files)
		commands.getstatusoutput("aplay " + file)

	elif emotion == emotionProbabilities.anger:
		files=os.listdir(/home/pi/gyuri/anger)
    	file=random.choice(files)
		commands.getstatusoutput("aplay " + file)

	elif emotion == emotionProbabilities.fear:
		files=os.listdir(/home/pi/gyuri/fear)
    	file=random.choice(files)
		commands.getstatusoutput("aplay " + file)

	else:
		print ("emotion value error")	
		commands.getstatusoutput("aplay " + file)

else:
	print ("Not enough sonorancy to determine emotions")

voice.destroy()

if os.path.isfile(/home/pi/gyuri/vokaturi/emotion.wav):
  os.remove(/home/pi/gyuri/vokaturi/emotion.wav)

sleep(5)