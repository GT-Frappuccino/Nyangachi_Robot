Vocal emotion recognition via OpenVokaturi API
=============  
* how to use  
```python
$ cd /home/pi/OpenVokaturi...  
$ python2.7 measure_wav.py path_to_sound_file.wav
# 다른 버전의 파이썬에서도 사용 가능한지 여부 확인 필요
# 음성 파일 포맷:S16_LE , 샘플레이트: 44100hz
```
* how to record  
``` python
$ arecord -D hw:1,0 -f S16_LE -d duration -r 44100 file_name.wav
```
