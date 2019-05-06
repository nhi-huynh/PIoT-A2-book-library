#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class calendarUtils:
    """
    A class used to represent different functions for the google calendar

    Methods
    -------
    removeCalendarEvent(eventid):
        A fuction created to remove a specific google calendar event
    createCalendarEvent(Duedate, ISBN, username):
        A fuction created to add a google calendar event at a specific date
    """

    def removeCalendarEvent(self, eventid):
        """
        A fuction created to remove a specific google calendar event

        Args:
            eventid: the string that identifies the specific event
        """
        event = service.events().delete(
            calendarId="primary", eventId='eventid').execute()

    def createCalendarEvent(self, Duedate, ISBN, username):
        """
        A fuction created to add a google calendar event at a specific date

        Args:
            Duedate: the date the event is to be created on
            ISBN: the ISBN of the book due back the day of the event
            username: the username of the person who borrowed the book

        Returns:
            eventID string
        """

        date = Duedate
        time_start = "T06:00:00+10:00"
        time_end = "T07:00:00+10:00"
        event = {
            "summary": "ISBN: {}".format(ISBN),
            "location": "RMIT Building 14",
            "description": "borrowed by:{}, due date:{}".format(
                username, Duedate),
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": "RMIT.PIOT.A2@gmail.com},
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 5},
                    {"method": "popup", "minutes": 10},
                ],
            }
        }

        event = service.events().insert(
            calendarId="primary", body=event).execute()
        return event['id']
