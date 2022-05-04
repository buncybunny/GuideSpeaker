from recorder.Recorder import recorde
from stt.SpeechToText import recognize, voice_recognition
from tts import TextToSpeech as TTS

import requests

import json

import os

import sys
import re

from playsound import playsound

def play(resp):
    #TTS에서 나온 speach를 재생
    global i
    try:
        out = open('output'+str(i)+'.mp3', 'wb')
        out.write(resp.audio_content)
        print('Audio content written to file "output'+str(i)+'.mp3"')
        out.close()
        playsound('output'+str(i)+'.mp3')
    except Exception as e:
        print(e)
    i += 1    
    
def isHangul(text):
    #들어온 문자열이 한글인지 아닌지 판별.
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0


def startReco():
    #일정 DB이상일때 녹음가능하도록 만들어줌
    import pyaudio
    import numpy as np

    CHUNK = 2 ** 11
    RATE = 44100
    toStart = False
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    for i in range(int(10 * 44100 / 1024)):  # go for a few seconds
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        if (50*peak/2**16) > 0:
            toStart = True
            break
        bars = "#" * int(50 * peak / 2 ** 16)
        print("%04d %05d %s" % (i, peak, bars))

    stream.stop_stream()
    stream.close()
    p.terminate()
    return toStart

def main():
    #주 메서드.
    ends = False
    while True:
        if startReco():
            cmd = voice_recognition('en-US')
            print('나: {}'.format(cmd))
            if 'hey' in cmd.lower():
                ends = True
                break
        
        if ends:
                break
    playsound(os.path.join(os.path.dirname(__file__), 'res','effect.wav'))        
    playsound(os.path.join(os.path.dirname(__file__), 'res','greeting.mp3'))
    cmd = voice_recognition('en-US')
    url = ''
        
    if "start" in cmd:
        if "record" in cmd:
            recorde(5)
            text = recognize()
            f = open(os.path.join(os.path.dirname(__file__), "녹음.txt"), "w")
            for result in text:
                f.write(result.alternatives[0].transcript)
            f.close()
    else:
        
        url = 'http://127.0.0.1:5000/request'
        params = {
        'serviceKey': 'hiseungmin',
        'content': cmd.lower()
        }
        response = requests.get(url, params=params)
        #print(response.text)
        
        data = json.loads(response.text)

        if ('content' in data and not data['content'] == 'None'):
            
        
            print(data['content'])

            if isHangul(data['content']):
                resp = TTS.synthesize_text_KR(data['content'].replace("Cafeteria", ""))
                play(resp)
            else:
                resp = TTS.synthesize_text(data['content'])
                play(resp)
        
        
            if data['status_code'] == '200':
                pass
            elif data['status_code'] == '789':
                cmd = voice_recognition('en-US')
                url = 'http://127.0.0.1:5000/answer'
                params = {
                'type': 'menu',
                'content': cmd.lower()
                }
            
                response = requests.get(url, params=params)
                #print(response.text)
                data = json.loads(response.text)
            
                print(data['content'])
            
                resp = TTS.synthesize_text_KR(data['content'])
                play(resp)
            
        else :
            resp = TTS.synthesize_text("sorry")
            play(resp)

    return

if __name__ == '__main__':
    global i
    i = 0
    playsound(os.path.join(os.path.dirname(__file__), 'res','start.mp3'))
    while True:
        main()
        
