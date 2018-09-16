import pyaudio
import wave
import os


def play_file(fname):
    # create an audio object
    audio = wave.open(fname, 'rb')
    chunk = 1024

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                    channels=audio.getnchannels(),
                    rate=audio.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = audio.readframes(chunk)

    while data:
        stream.write(data)
        data = audio.readframes(chunk)
    stream.stop_stream()
    stream.close()

def getStacks(number):
    stack = []
    while number != 0:
        stack.append(number % 10)
        number = int(number/10)
    while len(stack) % 3 != 0:
        stack.append(0)
    return stack


def sayThird(thousand, tens, digit, needMagic = False):
    if tens == 1:
        digit = digit+10
        tens = 0
    t = os.path.join(os.path.dirname(__file__), "festival/"+str(thousand*100)+".wav")
    if thousand > 0:
        play_file(t)
    if tens > 0:
        t = os.path.join(os.path.dirname(__file__), "festival/" + str(tens * 10) + ".wav")
        play_file(t)
    if digit > 0 and digit < 20 and not needMagic:
        t = os.path.join(os.path.dirname(__file__), "festival/" + str(digit) + ".wav")
        play_file(t)
    if digit > 0 and digit < 20 and needMagic:
        if digit in [1, 2]:
            t = os.path.join(os.path.dirname(__file__), "festival/" + str(digit) + "h.wav")
            play_file(t)
        else:
            t = os.path.join(os.path.dirname(__file__), "festival/" + str(digit) + ".wav")
            play_file(t)

def sayEnd(tens, digit, length):
    # тысячи
    if length > 3 and length <= 6:
        if tens != 1 and digit == 1:
            t = os.path.join(os.path.dirname(__file__), "festival/1000.wav")
            play_file(t)
        elif tens != 1 and digit in [2, 3, 4]:
            t = os.path.join(os.path.dirname(__file__), "festival/1000i.wav")
            play_file(t)
        else:
            t = os.path.join(os.path.dirname(__file__), "festival/1000h.wav")
            play_file(t)
    if length > 6 and length <=9:
        if digit == 1:
            t = os.path.join(os.path.dirname(__file__), "festival/1000000.wav")
            play_file(t)
        elif tens != 1 and digit in [2, 3, 4]:
            t = os.path.join(os.path.dirname(__file__), "festival/1000000a.wav")
            play_file(t)
        else:
            t = os.path.join(os.path.dirname(__file__), "festival/1000000v.wav")
            play_file(t)

def sayNumber(number):
    stack = getStacks(number)
    notNull = any(item != 0 for item in stack)
    if not notNull:
        t = os.path.join(os.path.dirname(__file__), "festival/0.wav")
        play_file(t)
    while len(stack) > 0:
        length = len(stack)
        thousands = stack.pop()
        tens = stack.pop()
        digits = stack.pop()
        if thousands == 0:
            length -= 1
        if tens == 0 and thousands == 0:
            length-=1
        sayThird(thousands, tens, digits, length > 3 and length <= 6)
        if thousands != 0 or digits != 0 or tens != 0:
            sayEnd(tens, digits, length)


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    while True:
        try:
            inp = int(input('Number:'))
            if inp < 0:
                t = os.path.join(os.path.dirname(__file__), "festival/minus.wav")
                play_file(t)
                inp = -inp

        except:
            inp = 0
            print('Not int')
            break
        sayNumber(inp)
    p.terminate()
