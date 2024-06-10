from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import datetime
from dateutil.parser import isoparse

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_calendar_service():
    creds = None
    token_path = 'calendar_token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def list_upcoming_events(query=None, max_results=10):
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    if not events:
        return "No upcoming events found."
    
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date_time = isoparse(start)
        formatted_time = date_time.strftime("%A, %B %d at %I:%M %p")
        event_list.append(f"On {formatted_time}, you have {event['summary']}.")
    
    return " ".join(event_list)

if __name__ == '__main__':
    print(list_upcoming_events())
