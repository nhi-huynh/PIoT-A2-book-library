#!/usr/bin/env/ python3

import socket
from Config import Config


class Reception():
    """
    A class used to represent the receiver pi class as a client socket

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

    def __init__(self):
        """
        Instantiates the receiver Pi class
        """
        cfg = Config()
        socketConfig = cfg.get_socket_config()
        port = socketConfig["port"]
        host = socketConfig["master_ip"]
        self.ADDRESS = (host, port)

    def start(self):
        """
        A fuction created to show the main menu for logging in

        Returns:
            boolean: True is logging out/quit
        """

        while True:
            print("Options:\n1.Register new user")
            print("2.Login by username and password")
            print("3.Login by face recognition")
            option = input("\nEnter option(blank space to quit): ")
            if (not option):
                print("Goodbye!")
                return True
            elif(option == "1"):
                # register new user
                print("Sorry, function 1 yet implemented")
            elif(option == "2"):
                # login user
                self.login()
            elif(option == "3"):
                print("Sorry, function 3 yet implemented")
            else:
                print("Invalid option")

    def login(self):
        """
        A fuction created to prompt user for login information

        Returns:
            none
        """

        """
        TODO: add login functionality based on local database
        """
        while True:
            validation = input("Enter username(blank to cancel): ")
            if(validation == "test"):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print("Connecting to master Pi...")
                    s.connect(self.ADDRESS)
                    print("Successfully connected, awaiting for logout....")
                    s.sendall(validation.encode())
                    while True:
                        # waiting for master Pi to terminate
                        data = s.recv(4096)
                        if (data):
                            print(data.decode())
                            print()
                            break
            elif (not validation):
                break
            else:
                print("Invalid username")
        return

receptionPi = Reception()
receptionPi.start()
