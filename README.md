# Sync Birthdays of Gooogle Contacts with Google Calendar

> As of 2024-10-15: The birthdays maintained for contacts in Google Contacts are in Germany no longer shown in the Google Calendar. See <https://support.google.com/calendar/community-guide/302081881/birthdays-from-contacts-no-longer-showing-in-google-calendar>.

The script allows syncing the birthdays from Google Contacts with birthdays maintained in the Google Calendar using the Google [Calendar API v3](https://developers.google.com/calendar/api/v3/reference) and the [People API v1](https://developers.google.com/people/api/rest).

## How to use

Follow the instructions at the [Google Quickstart](https://developers.google.com/calendar/api/quickstart/python) or the instructions following here:

1. Enable the APIs in the [Google Cloud Platform](https://console.cloud.google.com/apis):
    1. Enable the [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
    1. Enable the [Google People API](https://console.cloud.google.com/apis/library/people.googleapis.com).

1. Create client credentials.
    1. Create an OAuth 2.0 client at [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials). 
    1. Add your Google account to the clients audience.
    1. Download the client credentials, rename the file to `credentials.json` and place it in the root directory of the repository.

1. Install dependencies `pip install -r requirements.txt`

1. Run `python sync.py`. The first time, a browser will open to grant your app access to your Google Calendar and Contacts.
