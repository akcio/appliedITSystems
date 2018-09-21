from queryloader import QueryLoader
from sphinxmodule import talk
import pyaudio

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    queryLoader = QueryLoader()
    while True:
        text = input("Что хотите найти:")
        talk(queryLoader.searchQuery(text))

    p.terminate()