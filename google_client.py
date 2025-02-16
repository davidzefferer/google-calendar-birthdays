# See https://developers.google.com/calendar/api/quickstart/python

import datetime
import os.path

from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import List

from birthday import Birthday

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/contacts.readonly"
    ]

class GoogleClient:
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        try:
            self.calendar = build("calendar", "v3", credentials=creds)
            self.people = build("people", "v1", credentials=creds)

        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_calendar_id(self, name: str) -> str:
        page_token = None
        found_id = None
        while True:
            calendar_list = self.calendar.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == name:
                    found_id = calendar_list_entry['id']
                    break
            page_token = calendar_list.get('nextPageToken')
            if not page_token or found_id:
                break
        
        if not found_id:
            raise Exception(f'No calendar with the name {name} found')

        return found_id

    def create_birthday_event(self, birthday: Birthday):
        # See https://developers.google.com/calendar/api/guides/event-types#birthday
        # Would have loved to include the link to the contact, see birthday.contact
        date = birthday.as_date()
        date_formatted = date.strftime('%Y-%m-%d')

        recurrence_rule = f'RRULE:FREQ=YEARLY'
        if(date.month == 2 and date.day == 29):
            recurrence_rule = f'RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=2;BYMONTHDAY=-1'
    
        event = {
            'summary': f'{birthday.name}',
            'eventType': 'birthday',
            'visibility': 'private',
            'transparency': 'transparent',
            'start': {
                'date': date_formatted,
            },
            'end': {
                'date': date_formatted,
            },
            'recurrence': [
                recurrence_rule
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {
                        'method': 'popup', 
                        'minutes': 6 * 60,
                    },
                ],
            },
        }

        created_event = self.calendar.events().insert(calendarId='primary', body=event).execute()
        return created_event

    def does_birthday_exist(self, birthday: Birthday) -> bool:
        date = birthday.as_date()

        # TODO: Replace UTC time zone Z with actual time zone

        min = f'{(date - timedelta(days=1)).isoformat()}Z'
        max = f'{(date + timedelta(days=1)).isoformat()}Z'

        page_token = None
        while True:
            events = self.calendar.events().list(
                calendarId='primary',
                eventTypes='birthday',
                timeMin=min,
                timeMax=max,
                pageToken=page_token).execute()
            
            for event in events['items']:
                if 'summary' in event and event['summary'] == birthday.name:
                    return True
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return False
    
    def get_birthdays_from_contacts(self) -> List[Birthday]:
        # TODO: Multiple pages for more than 500 contacts?
        result = self.people.people().connections().list(
            resourceName='people/me',
            pageSize=500,
            personFields='metadata,names,birthdays'
        ).execute()

        contacts_with_birthday = []

        for contact in result['connections']:
            if 'birthdays' in contact and len(contact['birthdays']) > 0 and 'date' in contact['birthdays'][0]:
                name = contact['names'][0]['displayName']
                birthday = contact['birthdays'][0]['date']
                year = None
                if 'year' in birthday:
                    year = birthday['year']
                contacts_with_birthday.append(Birthday(
                    name,
                    contact['resourceName'],
                    year,
                    birthday['month'],
                    birthday['day']
                ))
        return contacts_with_birthday
