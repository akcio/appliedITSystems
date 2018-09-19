import os
from pocketsphinx import LiveSpeech, get_model_path
#
model_path = get_model_path()
print(model_path)

speech = LiveSpeech(
    verbose=False,
    sampling_rate=8000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    remove_noise = True,
    hmm=os.path.join(model_path, 'ru_cd_cont4000'),
    lm=os.path.join(model_path, 'ru.lm'),
    dic=os.path.join(model_path, 'ru.dic')
)

print("Say")

from queryloader import QueryLoader
from SpeakerModule import Speaker

qL = QueryLoader()
s = Speaker()


for phrase in speech:
    print('Get phrase: ' + str(phrase))
    if str(phrase).lower().__contains__('постой'):
        text = str(phrase).lower().split(" ")
        if text[0].__contains__('постой'):
            a = ' '
            a = a.join(text[1:])
            print(a)
            s.AddToQueue(qL.searchQuery(a))

print(1)

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