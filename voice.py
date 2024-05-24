from dotenv import load_dotenv
load_dotenv()

import speech_recognition as sr
import openai
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

# Function to generate speech from text
def generate_speech(text, voice='shimmer'):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )

    speech_file_path = "speggech.mp3"
    response.stream_to_file(speech_file_path)
    play_audio("C:\Users\Papak\Documents\lanchain\virtual_assitant\speggech.mp3")
    return speech_file_path

def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

def listen_for_activation():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        if "Phoenix" in r.recognize_whisper(audio, language="english"):
            print("You said: Hi Phoenix")
            listen_for_prompt()
        else:
            print("You said: " + r.recognize_whisper(audio, language="english"))
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

def listen_for_prompt():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            intro = "What would you like me to do?"
            print(intro)
            speech_file_path = generate_speech(intro)
            print(speech_file_path)
            play_audio(speech_file_path)

            audio = r.listen(source)
            try:
                user_input = r.recognize_whisper(audio, language="english")
                print("You said: " + user_input)

                if "Bye Phoenix" in user_input:
                    print("Ending conversation.")
                    break

                # Process the user's request here (e.g., query the LLM)
                # response = process_request(user_input)
                # response_speech_path = generate_speech(response)
                # play_audio(response_speech_path)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

if __name__ == "__main__":
    listen_for_activation()
