from queryloader import QueryLoader
from SpeakerModule import Speaker

if __name__ == '__main__':
    queryLoader = QueryLoader()
    speaker = Speaker()
    while True:
        text = input("Что хотите найти:")
        speaker.AddToQueue(queryLoader.searchQuery(text))