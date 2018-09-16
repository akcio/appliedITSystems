#!/usr/bin/env python2
#encoding: UTF-8
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pyttsx3
# engine.say('Good morning.')
# engine.runAndWait()
from threading import Lock

class Speaker():
    
    def __init__(self):
        # self.engine = pyttsx3.init()
        self.messagePool = []
        self._lock = Lock()
        self.TimerSpeach()
    
    def TimerSpeach(self):
        import threading
        threading.Timer(2.0, self.TimerSpeach).start()
        if (self.messagePool != []):
            self.messagePool.reverse()
            self.SpeakTest(self.messagePool.pop())
            self.messagePool.reverse()

    def AddToQueue(self, text):
        self.messagePool.append(text)
    
    def SpeakTest(self, text):
        import subprocess
        with self._lock:
        # self.engine.say(text)
        # self.engine.runAndWait()
            speach = '"' + text + '" '
            print(speach)
            #text = '«Hello world» "
            subprocess.call ('espeak -vru -s 60 ' + speach, shell = True)

#s = Speaker()
#s.AddToQueue('123')
#s.AddToQueue('Василий')
#s.AddToQueue('Молодец')

