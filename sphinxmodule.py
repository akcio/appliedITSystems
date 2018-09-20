import time, pyaudio, wave, os, urllib,pycurl,sys,string
from ctypes import *

def Record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

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

# Record()

Record()

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = 'output.wav'
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio, language="russian"))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language="RU-ru"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))



# import os
# from pocketsphinx import LiveSpeech, get_model_path
# #
# model_path = get_model_path()
# print(model_path)
#
# speech = LiveSpeech(
#     verbose=False,
#     sampling_rate=8000,
#     buffer_size=2048,
#     no_search=False,
#     full_utt=False,
#     remove_noise = True,
#     hmm=os.path.join(model_path, 'ru_cd_cont4000'),
#     lm=os.path.join(model_path, 'ru.lm'),
#     dic=os.path.join(model_path, 'ru.dic')
# )
#
# print("Say")
#
# from queryloader import QueryLoader
# from SpeakerModule import Speaker
#
# qL = QueryLoader()
# s = Speaker()
#
#
# for phrase in speech:
#     print('Get phrase: ' + str(phrase))
#     if str(phrase).lower().__contains__('постой'):
#         text = str(phrase).lower().split(" ")
#         if text[0].__contains__('постой'):
#             a = ' '
#             a = a.join(text[1:])
#             print(a)
#             s.AddToQueue(qL.searchQuery(a))
#
# print(1)

# #!/usr/bin/env python
# from os import environ, path
#
# from pocketsphinx.pocketsphinx import Decoder
# from sphinxbase.sphinxbase import *
#
# MODELDIR = model_path
# DATADIR = "/home/ileaban/PycharmProjects/lab1/ssml/"
#
# # Create a decoder with certain model
# config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'ru_cd_cont4000'))
# config.set_string('-lm', path.join(MODELDIR, 'ru.lm'))
# config.set_string('-dict', path.join(MODELDIR, 'ru.dic'))
# decoder = Decoder(config)
#
# # Decode streaming data.
# decoder = Decoder(config)
# decoder.start_utt()
# stream = open(path.join(DATADIR, 'output.wav'), 'rb')
# while True:
#   buf = stream.read(1024)
#   if buf:
#     decoder.process_raw(buf, False, False)
#   else:
#     break
# decoder.end_utt()
# print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])