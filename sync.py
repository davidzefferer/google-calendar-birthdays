import datetime

from google_client import GoogleClient
from birthday import Birthday

from typing import List, Dict

def determine_actions(state_actual: List[Birthday], state_target: List[Birthday]) -> Dict:
    to_create = []
    to_delete = []

    for birthday_target in state_target:
        should_be_created = True
        for birthday_actual in state_actual:
            if birthday_target.is_considered_same_birthday(birthday_actual):
                should_be_created = False
                break
        if should_be_created:
            to_create.append(birthday_target)

    for birthday_actual in state_actual:
        should_be_deleted = True
        for birthday_target in state_target:
            if birthday_actual.is_considered_same_birthday(birthday_target):
                should_be_deleted = False
                break
        if should_be_deleted:
            to_delete.append(birthday_actual)

    return {
        'to_create': to_create,
        'to_delete': to_delete,
    }

def create_birthdays(client: GoogleClient, birthdays: List[Birthday]):
    for birthday in birthdays:
        client.create_birthday_event(birthday)
    print(f'Created {len(birthdays)} birthday events')

def delete_birthdays(client: GoogleClient, birthdays: List[Birthday]):
    for birthday in birthdays:
        if not birthday.event_id:
            raise Exception("Trying to delete a birthday without known event id")
        client.delete_event(birthday.event_id)
    
    print(f'Deleted {len(birthdays)} birthday events')

if __name__ == "__main__":
    print("Started")
    client = GoogleClient()
    state_actual = client.get_birthdays_from_calendar(2025)
    state_target = client.get_birthdays_from_contacts()
    # state_actual = [Birthday("Test1", None, 2000, 1, 1), Birthday("Test2", None, 2025, 1, 2)]
    # state_target = [Birthday("Test2", None, 1990, 1, 2), Birthday("Test3", None, 2000, 1, 1)]
    actions = determine_actions(state_actual, state_target)
    create_birthdays(client, actions['to_create'])
    delete_birthdays(client, actions['to_delete'])
    print("Done")

