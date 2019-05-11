#!/usr/bin/env/ python3

import socket
from Config import Config


class Reception():
    """
    The receiver Pi class as a client socket
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
        Shows main menu for receiver Pi
        Option 1 for register new user
        Option 2 for login via console
        Option 3 for login via face recognition
        Blank input exits reception
        return: True
        rtype: boolean
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
        Prompt user input for login
        TODO: add login functionality based on local database

        Return: None
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
