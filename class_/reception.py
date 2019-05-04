#!/usr/bin/env/ python3

import socket


class Reception():
    """
    The receiver Pi class as a client socket
    """

    def __init__(self, HOST="127.0.0.1", PORT=12345):
        """
        Instantiates the receiver Pi class

        :type HOST: string
        :param HOST: The server's(master Pi) IP address

        :type PORT: int
        :param PORT: The port used by the server
        """
        self.ADDRESS = (HOST, PORT)

    def start(self):
        """
        Shows main menu for receiver Pi
        Option 1 for register new user
        Option 2 for login
        """
        while True:
            print("Options:\n1.Register\n2.Login")
            option = input("Enter option(blank space to quit): ")
            if (not option):
                print("Goodbye!")
                return True
            elif(option == "1"):
                # register new user
                print("Sorry, function yet implemented")
            elif(option == "2"):
                # login user
                self.login()
            else:
                print("Invalid option")
                    
    def login(self):
        """
        Prompt user input for login
        TODO: add login functionality based on local database

        Returns None after cancel login
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
                            break
                    # print("Disconnecting from master Pi")
                # print("Successfully logout")
            elif (not validation):
                break
            else:
                print("Invalid username")
        return

# receptionPi = Reception()
# receptionPi.start()
