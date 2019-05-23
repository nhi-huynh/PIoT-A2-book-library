# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

# from __future__ import print_function
# from datetime import datetime
# from datetime import timedelta
# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools

# # If modifying these scopes, delete the file token.json.
# SCOPES = "https://www.googleapis.com/auth/calendar"
# store = file.Storage("token.json")
# creds = store.get()
# if(not creds or creds.invalid):
#     flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
#     creds = tools.run_flow(flow, store)
# service = build("calendar", "v3", http=creds.authorize(Http()))

# def main():
#     """
#     Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user"s calendar.
#     """

# def insert():
#     date = datetime.now()
#     selection = input("Select an isbn: ")
#     name = input("Select an name: ")
#     tomorrow = (date + timedelta(days = 7)).strftime("%Y-%m-%d")
#     time_start = "{}T06:00:00+10:00".format(tomorrow)
#     time_end = "{}T07:00:00+10:00".format(tomorrow)
#     event = {
#         "summary": "New Programmatic Event",
# 	"id": selection+name.lower(),
#         "location": "RMIT Building 14",
#         "description": "Adding new IoT event",
#         "start": {
#             "dateTime": time_start,
#             "timeZone": "Australia/Melbourne",
#         },
#         "end": {
#             "dateTime": time_end,
#             "timeZone": "Australia/Melbourne",
#         },
#         "attendees": [
#             { "email": "kevin@scare.you" },
#             { "email": "shekhar@wake.you" },
#         ],
#         "reminders": {
#             "useDefault": False,
#             "overrides": [
#                 { "method": "email", "minutes": 5 },
#                 { "method": "popup", "minutes": 10 },
#             ],
#         }
#     }

#     event = service.events().insert(calendarId = "primary", body = event).execute()
#     print (event["id"])
#     print("Event created: {}".format(event.get("htmlLink")))

# if __name__ == "__main__":
#     main()
#     insert()

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage("token.json")
creds = store.get()
if(not creds or creds.invalid):
    flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
    creds = tools.run_flow(flow, store)
service = build("calendar", "v3", http=creds.authorize(Http()))

def main():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user"s calendar.
    """

    # Call the Calendar API.
    now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time.
    print("Getting the upcoming 10 events.")
    events_result = service.events().list(calendarId = "primary", timeMin = now,
        maxResults = 10, singleEvents = True, orderBy = "startTime").execute()
    events = events_result.get("items", [])

    if(not events):
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

def insert():
    date = datetime.now()
    tomorrow = (date + timedelta(days = 1)).strftime("%Y-%m-%d")
    time_start = "{}T06:00:00+10:00".format(tomorrow)
    time_end = "{}T07:00:00+10:00".format(tomorrow)
    event = {
        "summary": "New Programmatic Event",
        "location": "RMIT Building 14",
        "description": "Adding new IoT event",
        "start": {
            "dateTime": time_start,
            "timeZone": "Australia/Melbourne",
        },
        "end": {
            "dateTime": time_end,
            "timeZone": "Australia/Melbourne",
        },
        "attendees": [
            { "email": "kevin@scare.you" },
            { "email": "shekhar@wake.you" },
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "email", "minutes": 5 },
                { "method": "popup", "minutes": 10 },
            ],
        }
    }

    event = service.events().insert(calendarId = "primary", body = event).execute()
    print("Event created: {}".format(event.get("htmlLink")))

if __name__ == "__main__":
    main()
    insert()