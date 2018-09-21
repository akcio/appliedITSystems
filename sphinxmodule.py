import time, pyaudio, wave, os, urllib,pycurl,sys,string
from ctypes import *
import speech_recognition as sr
from functools import partial
from queryloader import QueryLoader

def record(file = "/tmp/output.wav"):
    global p
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = file

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Done recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def recognizeNow():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        try:
            res = r.recognize_google(audio, language="RU-ru")
        except sr.UnknownValueError:
            res = ''
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            res = ''
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return res

def recognize(file = "/tmp/output.wav"):
    global sr
    # use the audio file as the audio source
    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
       res = r.recognize_google(audio, language="RU-ru")
    except sr.UnknownValueError:
        res = ''
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        res = ''
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return res

def talk(text):
    import subprocess
    subprocess.call("espeak -vru -s 60 '" + text + "'", shell=True)

def wikiMode(queryLoader = None):
    global currentMode
    if queryLoader == None:
        talk("Не подключен модуль для работы с википедией")
        return
    talk('Что хотите найти? Для выхода скажи отмена')
    # record()
    text = recognizeNow()
    print('--' + text)
    if text.strip() == '':
        talk('Плохо слышно, попробуйте ещё')
        wikiMode(queryLoader)
        return
    if text.strip().lower() == 'отмена':
        currentMode = ''
        return
    talk(queryLoader.searchQuery(text))

def sayNumberMode():
    from random import randint
    cifer = randint(-999999999, 999999999)

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    queryLoader = QueryLoader()
    currentMode = None
    r = sr.Recognizer()
    while True:
        if currentMode != None or currentMode != '':
            if currentMode == 'wiki':
                wikiMode(queryLoader)
                continue

        talk('Выбери режим')
        # record()
        text = recognizeNow()
        print(text)
        if text.strip().lower() == 'вики':
            talk('Включен режим поиска в википедии')
            currentMode = 'wiki'
            continue
        if text.strip().lower() == 'выход':
            talk('Завершаю работу')
            break


    p.terminate()
    from time import sleep
    sleep(0.1)

