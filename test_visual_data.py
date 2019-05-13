import unittest
import os
import requests
import json
from datetime import datetime, date, timedelta
import calendar
from generate_visual import GenerateVisual


class TestVisualData(unittest.TestCase):

    borrows = []
    testGenerator = None

    def setUp(self):
        data1 = {
            "borrowID": 1,
            "ISBN": 1,
            "username": "adam",
            "borrowDate": date(2019, 5, 12),
            "dueDate": date(2019, 5, 12) + timedelta(days=7),
            "returnDate": date(2019, 5, 12)
        }
        data2 = {
            "borrowID": 2,
            "ISBN": 2,
            "username": "claire",
            "borrowDate": date(2019, 5, 12),
            "dueDate": date(2019, 5, 12) + timedelta(days=7),
            "returnDate": None
        }
        data3 = {
            "borrowID": 3,
            "ISBN": 2,
            "username": "graeme",
            "borrowDate": date.today(),
            "dueDate": date.today() + timedelta(days=7),
            "returnDate": None
        }
        
        self.borrows.append(data1)
        self.borrows.append(data2)
        self.borrows.append(data3)

        self.testGenerator = GenerateVisual()

    def test_weekly_graph(self):
        self.assertTrue(self.testGenerator.graph_weekly_data(self.borrows))

    def test_daily_graph(self):
        self.assertTrue(self.testGenerator.graph_daily_data(self.borrows))

if __name__ == "__main__":
    unittest.main()
