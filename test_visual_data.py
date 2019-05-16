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
            "borrowDate": datetime(2019, 5, 15, 12, 30, 0),
            "dueDate": datetime(2019, 5, 15, 12, 30, 0) + timedelta(days=7),
            "returnDate": datetime(2019, 5, 15, 12, 30, 00),
            "book": {
                "Title": "My Hero Academia"
            }
        }
        data2 = {
            "borrowID": 2,
            "ISBN": 2,
            "username": "claire",
            "borrowDate": datetime(2019, 5, 15, 3, 0, 0),
            "dueDate": datetime(2019, 5, 15, 3, 0, 0) + timedelta(days=7),
            "returnDate": None,
            "book": {
                "Title": "Fairy Tail"
            }
        }
        data3 = {
            "borrowID": 3,
            "ISBN": 2,
            "username": "graeme",
            "borrowDate": datetime.now(),
            "dueDate": datetime.now() + timedelta(days=7),
            "returnDate": None,
            "book": {
                "Title": "Fairy Tail"
            }
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
