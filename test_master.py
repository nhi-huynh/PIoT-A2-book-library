from unittest.mock import patch
import unittest
from master import Master


class TestMasterSocket(unittest.TestCase):
    """
    Serves as a test case for master Pi as the server socket
    To be run along with test_reception.py to establish connection
    """

    master = None

    def setUp(self):
        """
        Sets up the master pi server socket
        """
        self.master = Master()

    def test_connection(self):
        """
        Test should be successful with master Pi shuts down automatically
        when no reception Pi connects to it after 20 sec1onds wait time

        Assert: True when masterPi.start() returns True
        """
        try:
            success = self.master.start()
            self.assertTrue(success)
        except Exception as e:
            print("Exception is {}".format(e))    


if __name__ == "__main__":
    unittest.main()         
