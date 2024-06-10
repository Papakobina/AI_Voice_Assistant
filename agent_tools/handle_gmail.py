from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
import os
import pickle

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    token_path = 'token.pickle'
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
    
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_messages(service, user_id='me'):
    results = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        return "No messages found."
    else:
        snippets = []
        for message in messages[:5]:  # Get the first 5 messages
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            headers = msg['payload']['headers']
            
            # Extract useful headers
            from_header = next((header['value'] for header in headers if header['name'] == 'From'), 'N/A')
            subject_header = next((header['value'] for header in headers if header['name'] == 'Subject'), 'N/A')
            
            snippet = msg['snippet']
            snippets.append(f"From: {from_header}\nSubject: {subject_header}\nSnippet: {snippet}\n")
        
        return "\n".join(snippets)

            
def get_email_messages(query=None):
    service = get_gmail_service()
    return list_messages(service)
            
            
if __name__ == '__main__':
    get_email_messages()

