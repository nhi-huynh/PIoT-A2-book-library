from unittest.mock import patch
import unittest
from reception import Reception


class TestMasterSocket(unittest.TestCase):
    """
    Serves as a test case for reception Pi as the client socket
    To be run along with test_master.py to establish connection
    """

    reception = None

    def setUp(self):
        """
        Sets up the reception Pi server socket
        """
        self.reception = Reception()

    def test_connection(self):
        """
        Test is successful with following sequence scenario:
        1. Successful login connects to master Pi
        2. On hold while master Pi is currently busy then available
        3. Close option menu with blank input

        Asserts: True when option menu closes
        """
        try:
            success = self.reception.start()
            self.assertTrue(success)
        except Exception as e:
            print("Exception is {}".format(e))    


if __name__ == "__main__":
    unittest.main()         
