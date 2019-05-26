from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class CalendarUtils:
    """
    A class used to represent different functions for the google calendar

    Attributes:
        SCOPES : string
            website for
        store : JSON file
            token json file; stores the users access and refresh tokens
        creds : dictionary
            read in from store
    """

    def __init__(
                self, connection=None, credentials_path=None, token_path=None):
        if credentials_path is None or token_path is None:
            raise Exception('Credentials and token paths required')

        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets(credentials_path, SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))

    def removeCalendarEvent(self, ISBN, username):
        """
        A function created to remove a specific google calendar event

        Args:
            ISBN: the ISBN of the book due back the day of the event
            username: the username of the person who borrowed the book
        """
        e_id = ISBN + username.lower()
        event = self.service.events().delete(
            calendarId="primary", eventId=e_id).execute()

    def createCalendarEvent(self, ISBN, username):
        """
        A function created to add a google calendar event at a specific date

        Args:
            ISBN: the ISBN of the book due back the day of the event
            username: the username of the person who borrowed the book

        Returns:
            eventID string
        """

        date = datetime.now()
        dueDate = (date + timedelta(days=7)).strftime("%Y-%m-%d")
        time_start = "{}T09:00:00+10:00".format(dueDate)
        time_end = "{}T10:00:00+10:00".format(dueDate)
        eventID = ISBN+username.lower()

        event = {
            "summary": ISBN,
            "id": eventID,
            "location": "RMIT Building 14",
            "description": "Book Due to be Returned",
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": "kevin@scare.you"},
                {"email": "shekhar@wake.you"},
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 5},
                    {"method": "popup", "minutes": 10},
                ],
            }
        }

        event = self.service.events().insert(
            calendarId="primary", body=event).execute()
        return event['id']
