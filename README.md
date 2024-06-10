# AI Voice Assistant with Speech and Google Integration

## Overview
This project is a virtual assistant application capable of recognizing voice commands, fetching emails and calendar events from Google services, and responding with synthesized speech. The assistant is designed to help users interact with their Gmail and Google Calendar through voice commands, providing a seamless and hands-free experience.

## Features
- **Voice Recognition:** Listens for activation and command phrases.
- **Gmail Integration:** Fetches recent emails and reads them out loud.
- **Google Calendar Integration:** Fetches upcoming events and reads them out loud.
- **Text-to-Speech:** Converts text responses into speech using OpenAI's TTS model.
- **Conversation Memory:** Maintains context across multiple interactions.

## Technologies Used
- **Python:** Main programming language.
- **SpeechRecognition:** For recognizing voice commands.
- **Whisper:** For converting speech to text.
- **Pydub and Pygame:** For audio playback.
- **Google API Client:** To interact with Gmail and Google Calendar APIs.
- **OpenAI API:** For text-to-speech functionality.
- **LangChain:** To create agents and tools for handling various commands.
- **dotenv:** For managing environment variables.

## Main Components
### `main.py`
The entry point for the application. It listens for activation commands and processes voice commands.

### `handle_gmail.py`
Handles interactions with the Gmail API to fetch recent emails.

### `handle_calendar.py`
Handles interactions with the Google Calendar API to fetch upcoming events.

### `voice.py`
Handles text-to-speech conversion and audio playback.

### `llm_model.py`
Integrates all functionalities using LangChain to create a unified agent capable of handling various commands.

## Technical Explanation
### Voice Recognition
The application uses the `speech_recognition` library and the Whisper model to listen for voice commands and convert speech to text accurately. When the user says "Phoenix," the assistant starts listening for further commands.

### Google API Integration
#### Gmail
- **Service Setup:** Uses OAuth 2.0 for authentication.
- **Fetching Emails:** Fetches the latest emails from the user's inbox and formats them for speech output.

#### Google Calendar
- **Service Setup:** Uses OAuth 2.0 for authentication.
- **Fetching Events:** Fetches upcoming events from the user's primary calendar and formats them for speech output.

### Text-to-Speech
- **OpenAI API:** Utilizes OpenAI's text-to-speech model to convert text responses into speech.
- **Audio Playback:** Uses Pydub and Pygame for audio playback to ensure cross-platform compatibility.

### LangChain Integration
LangChain is used to create agents that handle different tools (Gmail, Google Calendar, General Knowledge). The agents use conversation memory to maintain context across multiple interactions.

### Conversation Memory
The assistant uses `ConversationBufferMemory` from LangChain to keep track of conversation history. This allows the assistant to provide context-aware responses and maintain a coherent conversation flow.

## Future Enhancements
- **Enhanced Error Handling:** Improve robustness by handling various edge cases and errors.
- **Additional Integrations:** Add more functionalities such as weather updates, news briefings, and task management.
- **Customization:** Allow users to customize the activation phrase and response voices.
