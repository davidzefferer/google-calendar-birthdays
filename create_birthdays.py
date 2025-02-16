import datetime

from google_client import GoogleClient
from birthday import Birthday


def create_bithdays_for_all_contacts(client: GoogleClient):
    birthdays = client.get_birthdays_from_contacts()
    created_counter = 0
    for birthday in birthdays:
        if not client.does_birthday_exist(birthday):
            client.create_birthday_event(birthday)
            created_counter += 1

    print(f'Created {created_counter} birthdays')


if __name__ == "__main__":
    # GoogleCalendarClient().test()
    client = GoogleClient()
    create_bithdays_for_all_contacts(client)
