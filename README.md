# Sync Birthdays from Gooogle Contacts to Google Calendar

In Germany the birthdays maintained in [Google Contacts are no longer synced to the Google Calendar](https://support.google.com/calendar/community-guide/302081881/birthdays-from-contacts-no-longer-showing-in-google-calendar).

The script syncs birthdays from Google Contacts to the Google Calendar using the Google [Calendar API v3](https://developers.google.com/calendar/api/v3/reference) and the [People API v1](https://developers.google.com/people/api/rest).

## How to use

Follow the instructions at the [Google Quickstart](https://developers.google.com/calendar/api/quickstart/python).

1. Enable the [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
1. Enable the [Google People API](https://console.cloud.google.com/apis/library/people.googleapis.com).
1. Create an OAuth 2.0 client at [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) and at your account to `Audience`.
1. Download client credentials, rename the file to `credentials.json` and place it in the root directory of the repository.
1. Install dependencies `pip install -r requirements.txt`
1. Run `python sync.py`. The first time, a browser will open to grant your app access to your Google Calendar and Contacts, the token will be stored in `token.json`.
