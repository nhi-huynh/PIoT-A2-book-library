#!/usr/bin/env python3

import socket
import select
from class_.menu import MasterApplication


class Master():
    """
    A class used to represent the master pi class as a client socket

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

        self.ip = config['ip']
        self.port = config['port']
        self.address = (self.ip, self.port)

    def start(self):
        """A fuction created to connect to the reception pi
        and to run the menu class"""

        """
        TODO: add menu class functionality in while loop
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            print("master Pi currently listening...")
            s.listen()

            while True:
                # wait up 30 seconds for receiver Pi to connect
                newReceiver, _, _ = select.select([s], [], [], 30)
                if not(newReceiver):
                    print("master pi automatically shuts down")
                    return True
                print("Listening on receiver Pi({})...".format(self.address))
                conn, addr = s.accept()
                with conn:
                    username = conn.recv(4096).decode()
                    print("Login successfully by {username}"
                          .format(username=username))
                    # shows booking menu
                    # booking menu should call break to exit the menu
                    # once exit, master pi will end connection
                    # PLACEHOLDER CODE BELOW, TO BE DELETED AFTER INTEGRATION
                    # while True:
                    #     message = input("Please select option: ")
                    #     if(not message):
                    #         conn.sendall("Logout successfully".encode())
                    #         break
                    #     print("Input chosen is {} ".format(message))
                    ma = MasterApplication(username)
                    ma.showMenu()
                    conn.sendall("Successfully log out".encode())
                    print("Disconnecting from receiver Pi")
                    print("master Pi currently listening...")
