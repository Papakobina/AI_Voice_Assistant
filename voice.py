import openai
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
import pygame
load_dotenv()



# Function to generate speech from text
def generate_speech(text, voice='shimmer'):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )

    speech_file_path = "audio/AI_speech.mp3"
    response.stream_to_file(speech_file_path)
    return speech_file_path

def play_audio(file_path):
    pygame.mixer.init(buffer=1024)  # Increase the buffer size if needed
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
        pygame.time.Clock().tick(10)
    
    
def speak(text):
    speech_file_path = generate_speech(text)
    play_audio(speech_file_path)
    
    
if __name__ == "__main__":
    speak("Hello, I am from poland but speak french")

