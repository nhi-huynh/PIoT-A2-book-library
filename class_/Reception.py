# vim: set et sw=4 ts=4 sts=4:

import socket
import re
from getpass import getpass
from class_.FaceRecognition import FaceRecognition
from class_.TCP import ReceptionConnection


class Reception():
    """The receiver Pi class as a client socket

    Attributes:
        config : dict
            Config for connection
        dbi : DBinterface
            interface used to access the db
        auth : Auth
            used for user authentication
        face_rec : face_recognition
            used for facial recognition
        self.ip : string
            ip address from the config file
        self.port : string
            port from the config file
        self.address : string
            address from the ip address and the port
    """

    dbi = None
    auth = None

    def __init__(
            self, config=None, dbi=None, auth=None, face_recognition=None):
        """Instantiates the receiver Pi class"""

        if config is None:
            raise Exception('Config required')

        if dbi is None:
            raise Exception('Database interface required')

        if auth is None:
            raise Exception('Auth object required')

        if face_recognition is None:
            raise Exception('Face recognition object required')

        self.dbi = dbi
        self.auth = auth

        print('Waiting for Master Pi')
        self.tcp = ReceptionConnection(config['socket'])

        print('Connecting to Master Pi')
        self.tcp.connect()

        self.fr = face_recognition

    def start(self):
        """
        A function created to show the main menu for the receiver pi

        Returns:
            to function when the user selects exit
        """

        end = False

        while True:
            print("Options:\n[1] Register new user")
            print("[2] Login by username and password")
            print("[3] Login by face recognition")

            option = input('\nEnter option("exit" to quit): ')
            option = option.lower()

            if option == 'exit':
                return

            elif option == '1':
                self.register()

            elif option == '2':
                self.login()

            elif option == '3':
                self.login_fr()

            elif not len(option):
                print('\n\nPlease select one of the following')

            else:
                print("""\n\nInvalid option,
                        please enter a valid number or "exit" to end""")

    def __start_session(self, username):
        """
        A function created to start a session

        Args:
            username: username of person logged in
        """

        res = self.tcp.send_all(username)

        if not res and not self.__reconnect():
                print('Cancelling')
                return False

        resp = self.tcp.receive()

        if not resp and not self.__reconnect():
            print('Cancelling')
            return False

        print('session start response:', resp)

    def __reconnect(self):
        """
        A function created to reconnect to the master pi

        Returns:
            True if reconnected
            False if else
        """

        print('Connection to Master Pi lost, attempting to reconnect')

        if self.tcp.connect():
            print('Successfully reconnected')
            return True

        print('Failed to reconnect')
        return False

    def login(self):
        """A function created to prompt user input for login"""

        user = None

        while True:

            username = input('Username ("exit" to cancel): ')

            if username == 'exit':
                print('Cancelling')
                return

            if len(username) < 1:
                print('Password required')
                continue

            password = getpass('Password: ')

            if password == 'exit':
                print('Cancelling')
                return

            if len(password) < 1:
                print('Password required')
                continue

            user = self.auth.login(username=username, password=password)

            if user:
                break

        # Just in case
        if not user:
            return

        self.__start_session(user.get_info('username'))

    def register(self):
        """A function created to register a user

        Returns:
            False if exception
        """

        first_name = self.get_validated_input(
            'First name: ', minlen=1, maxlen=50)

        if not first_name:
            return

        surname = self.get_validated_input('Surname: ', minlen=1, maxlen=50)

        if not surname:
            return

        uname_invalid_msg = """Invalid username.
                            Must be between 5 and 25 characters (inclusive)"""
        uname_invalid_msg += """, start and end with a letter,
                            and can only contain letters"""
        uname_invalid_msg += ', numbers, -, and _'

        uname = None

        while True:

            uname = self.get_validated_input(
                'Username: ',
                val_func=self.auth.validate_username,
                val_func_msg=uname_invalid_msg
            )

            if not uname:
                return

            if self.auth.username_available(uname):
                break

            print('Username taken, please choose something different.')

        email = None
        invalid_email_msg = """Invalid email,
                            please ensure you are entering a valid email"""

        while True:
            email = self.get_validated_input(
                'Email: ',
                val_func=self.auth.validate_email,
                val_func_msg=invalid_email_msg
            )

            if self.auth.username_available(email):
                break

            print('Email already registered, please register a new email')

        password = None

        password = self.get_validated_input(
            'Password: ',
            minlen=8,
            maxlen=110,
            reg=r'.*[0-9].*',
            reg_msg='Must contain at least one number',
            hide_input=True,
            confirm=True
        )

        try:
            self.auth.register(
                username=uname,
                first_name=first_name,
                surname=surname,
                email=email,
                password=password
            )
        except:
            return False

        print('\n\nRegistration successful')

        while True:

            i = input('Would you like to enable face recognition?\nYes/No')

            i = i.lower()

            if i[0] == 'y':
                self.register_face(uname)
                break
            elif i[0] == 'n':
                break
            else:
                print('Invalid option')

        print('Loggin in')
        self.__start_session(uname)

    def register_face(self, uname):
        """A function created to register a new face"""

        while True:
            if self.fr.register(uname):
                print('Successfully enabled face recognition')
                break

            print('Failed to register')

            retry = False

            while True:

                i = input('Try again?\nYes/No')

                i = i.lower()

                if i[0] == 'y':
                    retry = True
                    break
                elif i[0] == 'n':
                    break
                else:
                    print('Invalid option')

            if not retry:
                print('Cancelled')
                break

        self.__start_session(uname)

    @staticmethod
    def get_validated_input(
            msg,
            fname=None,
            minlen=None,
            maxlen=None,
            reg=None,
            reg_msg=None,
            hide_input=False,
            confirm=False,
            val_func=None,
            val_func_msg=None):

        """
        A function created to get validate input

        Args:
            msg: the string you want to validate
            fname:
            minlen: the minimum length the string can be
            maxlen: the maximum length the string can be
            reg:
            reg_msg:
            hide_input: to show or hide the input (eg hide passwords)
            confirm:
            val_func: a function to validate with
            val_func_msg: the message to display if invalid

        Returns:
            False if user enter exit
            else return user input
        """

        while True:
            print('type exit to cancel')

            if hide_input:
                uinput = getpass(msg)
            else:
                uinput = input(msg)

            i_len = len(uinput)

            if uinput == 'exit':
                return False

            if minlen is not None and i_len < minlen:
                print('Must be at least {} characters long'.format(minlen))
                continue

            if maxlen is not None and i_len > maxlen:
                print('Too long, must be at most {} characters'.format(maxlen))
                continue

            if reg is not None and not re.match(reg, uinput):
                print(reg_msg if reg_msg is not None else 'Invalid format')
                continue

            if val_func is not None and not val_func(uinput):
                if val_func_msg is None:
                    print('Invalid format')
                else:
                    print(val_func_msg)

                continue

            if not confirm:
                return uinput

            cfrm = getpass('Type again to confirm')

            if cfrm == 'exit':
                return False

            if uinput == cfrm:
                return uinput

            print('Inputs do not match, please try again')

    def login_fr(self):
        """A function created to login using facial recognition"""

        username = self.fr.login(timeout=20)

        if not username:
            print('Could not recognise you, please try again')
            return

        print('Welcome, {}'.format(username))
        self.__start_session(username)
