#!/usr/bin/env python3

from class_.TCP import MasterConnection
from class_.MasterApplication import MasterApplication


class Master():
    """
    A class used to manage the connection to the reception pi

    Attributes
    ----------
    cfg : file
        file that contains the ip address and port numbers
    socketConfig : dict
        contains the ip address and port numbers
    port : int
        port number to connect to
    host : string
        ip address
    """

    def __init__(self, config=None):
        """
        Instantiates the master Pi class

        :type config: dict
        :param config: Config for connection

        """
        if config is None:
            raise Exception('Config required')


        print('Waiting for Reception Pi')
        self.conn = MasterConnection(config)

        print('Connecting to Reception Pi')
        self.conn.connect()

    def start(self):
        """A fuction created to connect to the reception pi
        and to run the menu class"""

        """
        TODO: add menu class functionality in while loop
        """

        while True:
            username = self.conn.receive()

            if not username:
                print('Connection lost, attempting to reconnect')

                self.conn.connect()

                msg = self.conn.receive()

                if msg == b'exit':
                    print('Exiting')
                    self.conn.disconnect()
                    return True


                if not username:
                    print('Failed to reconnect')
                    return False

            ma = MasterApplication(username)
            ma.showMenu()

            print('Logging out')
            conn.send_all('logout')
