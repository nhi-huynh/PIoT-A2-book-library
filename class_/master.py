#!/usr/bin/env python3

import socket
import select
from Config import Config


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

    Methods
    -------
    start():
        A fuction created to connect to the reception pi
        and to run the menu class
    """

    def __init__(self):
        """
        Instantiates the master Pi class

        """
        cfg = Config()
        socketConfig = cfg.get_socket_config()
        port = socketConfig["port"]
        host = socketConfig["reception_ip"]
        self.ADDRESS = (host, port)

    def start(self):
        """A fuction created to connect to the reception pi
        and to run the menu class"""

        """
        TODO: add menu class functionality in while loop
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            print("master Pi currently listening...")
            s.listen()

            while True:
                # wait up 30 seconds for receiver Pi to connect
                newReceiver, _, _ = select.select([s], [], [], 30)
                if not(newReceiver):
                    print("master pi automatically shuts down")
                    return True
                print("Listening on receiver Pi({})...".format(self.ADDRESS))
                conn, addr = s.accept()
                with conn:
                    username = conn.recv(4096)
                    print("Login successfully by {username}"
                          .format(username=username.decode()))
                    while True:
                        # shows booking menu
                        # will run break when booking menu function returns
                        # any value
                        # terminate = bookingClass.showBookingMenu()
                        # if (terminate):
                        #     break
                        message = input("Please select option: ")
                        if(not message):
                            conn.sendall("Logout successfully".encode())
                            break
                        print("Input chosen is {} ".format(message))

                    print("Disconnecting from receiver Pi")

masterPi = Master()
masterPi.start()
