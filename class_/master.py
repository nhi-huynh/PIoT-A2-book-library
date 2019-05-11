#!/usr/bin/env python3

import socket
import select
from Config import Config


class Master():
    """
    The master Pi class as a server socket
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
        """
        Starts to listen and make connection with receiver Pi
        after successful login.
        Once connection is made, runs the menu class for borrowing books.

        TODO: add menu class functionality in while loop

        Returns None after master Pi automatically shuts down listening

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
