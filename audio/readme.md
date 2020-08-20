### 스피커로 음원 출력시  

* sampling rate: 44.1khz (cd 품질)  
* 확장자: wav  
* 변환 사이트: https://online-audio-converter.com/ko/  
* 터미널에서 재생하기   
```  
    aplay 파일이름  
```      
* 코드에서 재생하기  
```
    from omxplayer.player import OMXPlayer
    from pathlib import Path
    from time import sleep  
    
    AUDIO_PATH = Path("/path/to/your/audiofile")  
    
    player = OMXPlayer(AUDIO_PATH)  

    sleep(5)

    player.quit()
```      
