from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from emailstuff import send_email
from event import Event

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        #print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])  #if values associated with 'items' key is found, store the items in events. If no items are found, events is assigned to an empty list
        if not events:
            print('No upcoming events found.')
            return
        # print(events[0].get('summary'))
        print('Menu:\n'
            '1. Send test email with subject + body\n'
            '2. Add a test event to the calendar')
        userInput = input('-> ')
        while (userInput != '0'):
            if userInput == '1':
                send_email(events[0].get('summary'))
            if userInput == '2':
                event_info = Event()
                event = {
                    'summary': 'Google I/O 2015',
                    'location': '800 Howard St., San Francisco, CA 94103',
                    'description': 'A chance to hear more about Google\'s developer products.',
                    'start': {
                        'dateTime': '2023-06-24T09:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': '2023-06-24T17:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    }
                }
                event = service.events().insert(calendarId='primary', body=event).execute()
                print('Event was created')
            print('Menu:\n'
            '1. Send test email with subject + body\n'
            '2. Add a test event to the calendar')
            userInput = input('-> ')
        print("Exiting program...")
        #Prints the start and name of the next 10 events
        #for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()



