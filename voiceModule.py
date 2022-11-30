import pyttsx3

engine = pyttsx3.init()
message_1 = '''Welcome to Math.Fun game where you will have fun while learning.
            Please enter ya level between easy medium or hard '''


def readTime(time):
    if not time:
        engine.say(f" Oops, time up")
        engine.runAndWait()
    else:
        engine.say(f" {time} ")
        engine.runAndWait()


