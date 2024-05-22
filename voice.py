#https://stackoverflow.com/questions/76560926/can-i-use-the-python-speech-recognition-and-openais-whisper-libraries-together

import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        print("You said: " + r.recognize_whisper(audio, language="english"))
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        

if __name__ == "__main__":
    listen()
