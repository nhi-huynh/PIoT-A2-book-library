#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class CalendarUtils:
    """
    A class used to represent different functions for the google calendar

    Attributes
    ----------
    connection : string
        the _____

    """

    def __init__(self, connection=None):
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))

    #Variable service is not defined. 
    #This is a source of error.
    def removeCalendarEvent(self, eventid):
        """
        A function created to remove a specific google calendar event

        Args:
            eventid: the string that identifies the specific event
        """
        event = service.events().delete(
            calendarId="primary", eventId='eventid').execute()

    def createCalendarEvent(self, duedate, ISBN, username):
        """
        A function created to add a google calendar event at a specific date

        Args:
            Duedate: the date the event is to be created on
            ISBN: the ISBN of the book due back the day of the event
            username: the username of the person who borrowed the book

        Returns:
            eventID string
        """

        date = duedate
        time_start = "{}T09:00:00+10:00".format(date)
        time_end = "{}T10:00:00+10:00".format(date)
        event = {
            "summary": "ISBN: {}".format(ISBN),
            "location": "RMIT Building 14",
            "description": "borrowed by:{}, due date:{}".format(
                username, duedate),
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": "RMIT.PIOT.A2@gmail.com"},
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
        print(event['id'])
        return event['id']
