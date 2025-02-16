from typing import List

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from birthday import Birthday

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/contacts.readonly",
]


class GoogleClient:
    def __init__(self):
        # See https://developers.google.com/calendar/api/quickstart/python
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

    def create_birthday_event(self, birthday: Birthday):
        # See https://developers.google.com/calendar/api/guides/event-types#birthday
        # Would have loved to include the link to the contact, see birthday.contact
        date = birthday.as_date()
        date_formatted = date.strftime("%Y-%m-%d")

        recurrence_rule = f"RRULE:FREQ=YEARLY"
        if date.month == 2 and date.day == 29:
            recurrence_rule = f"RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=-1"

        event = {
            "summary": f"{birthday.name}",
            "eventType": "birthday",
            "visibility": "private",
            "transparency": "transparent",
            "start": {
                "date": date_formatted,
            },
            "end": {
                "date": date_formatted,
            },
            "recurrence": [recurrence_rule],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "popup",
                        "minutes": 6 * 60,
                    },
                ],
            },
        }

        created_event = (
            self.calendar.events().insert(calendarId="primary", body=event).execute()
        )
        return created_event

    def delete_event(self, event_id: str):
        self.calendar.events().delete(calendarId="primary", eventId=event_id).execute()

    def get_birthdays_from_calendar(self, year: int) -> List[Birthday]:
        min = f"{year}-01-01T00:00:00Z"
        max = f"{year}-12-31T23:59:59Z"

        birthdays = []

        page_token = None
        while True:
            events = (
                self.calendar.events()
                .list(
                    calendarId="primary",
                    eventTypes="birthday",
                    timeMin=min,
                    timeMax=max,
                    pageToken=page_token,
                )
                .execute()
            )

            for event in events["items"]:
                if event["birthdayProperties"]["type"] == "self":
                    continue

                date = event["start"]["date"]
                year = int(date[:4])
                month = int(date[5:7])
                day = int(date[8:])

                recurrence_rule = event["recurrence"][0]
                if (
                    "BYMONTH=2" in recurrence_rule
                    and "BYMONTHDAY=-1" in recurrence_rule
                ):
                    month = 2
                    day = 29

                birthdays.append(
                    Birthday(
                        event["summary"],
                        year,
                        month,
                        day,
                        contact=None,
                        event_id=event["id"],
                    )
                )

            page_token = events.get("nextPageToken")
            if not page_token:
                break

        return birthdays

    def get_birthdays_from_contacts(self) -> List[Birthday]:
        # TODO: Multiple pages for more than 500 contacts?
        result = (
            self.people.people()
            .connections()
            .list(
                resourceName="people/me",
                pageSize=500,
                personFields="metadata,names,birthdays",
            )
            .execute()
        )

        contacts_with_birthday = []

        for contact in result["connections"]:
            if (
                "birthdays" in contact
                and len(contact["birthdays"]) > 0
                and "date" in contact["birthdays"][0]
            ):
                name = contact["names"][0]["displayName"]
                birthday = contact["birthdays"][0]["date"]
                year = None
                if "year" in birthday:
                    year = birthday["year"]
                contacts_with_birthday.append(
                    Birthday(
                        name,
                        year,
                        birthday["month"],
                        birthday["day"],
                        contact=contact["resourceName"],
                        event_id=None,
                    )
                )
        return contacts_with_birthday
