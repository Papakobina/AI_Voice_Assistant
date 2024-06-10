from dotenv import load_dotenv
load_dotenv()

import speech_recognition as sr
import openai
from pathlib import Path
from llm_model import answer_query  # Ensure this is the correct import path
from voice import speak

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
    conversation_history = []  # Initialize conversation history
    while True:
        with sr.Microphone() as source:
            intro = "What would you like me to do?"
            speak(intro)
            conversation_history.append(intro)  # Add system prompt to history

            audio = r.listen(source)
            try:
                user_input = r.recognize_whisper(audio, language="english")
                conversation_history.append(user_input)  # Add user input to history
                response = answer_query(user_input, conversation_history)
                speak(response)
                conversation_history.append(response)  # Add system response to history

                if "Bye Phoenix" in user_input:
                    print("Ending conversation.")
                    break
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

if __name__ == "__main__":
    listen_for_prompt()
