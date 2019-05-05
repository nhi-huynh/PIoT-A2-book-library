#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def removeCalendarEvent(string eventid):
    event = service.events().delete(
        calendarId="primary", eventId='eventid').execute()


def createCalendarEvent(datetime Duedate, string ISBN, string username):
    date = Duedate
    time_start = "T06:00:00+10:00"
    time_end = "T07:00:00+10:00"
    event = {
        "summary": "ISBN: {}".format(ISBN),
        "location": "RMIT Building 14",
        "description": "borrowed by:{}, due date:{}".format(username, Duedate),
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

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event['id']
