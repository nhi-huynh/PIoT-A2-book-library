# vim: set et sw=4 ts=4 sts=4:

import socket, re
from getpass import getpass
from class_.FaceRecognition import FaceRecognition
from class_.TCP import ReceptionConnection()


class Reception():
    """
    The receiver Pi class as a client socket
    """
    dbi = None
    auth = None

    def __init__(self, config=None, dbi=None, auth=None, face_recognition=None):
        """
        Instantiates the receiver Pi class

        :type config: dict
        :param config: Config for connection

        :type dbi: DBinterface
        :param dbi: interface used to access the db

        :type auth: Auth
        :param auth: used for user authentication
        """

        if config is None:
            raise Exception('Config required')

        if dbi is None:
            raise Exception('Database interface required')

        if auth is None:
            raise Exception('Auth object required')

       # if face_recognition is None:
           # raise Exception('Face recognition object required')

        self.dbi = dbi
        self.auth = auth

        print('Waiting for Master Pi')
        self.tcp = ReceptionConnection(config['socket'])

        print('Connecting to Master Pi')
        self.tcp.connect()

        self.face_rec = face_recognition

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
                print('\n\nInvalid option, please enter a valid number or "exit" to end')

    def __start_session(self, username):
        res = self.tcp.send_all(username)

        if not res:
            print('Connection to Master Pi lost, attempting to reconnect')
            self.tcp.connect()

            res = self.tcp.send_all(username)

            if not res:
                print('Failed to reconnect, returning to menu')
                return

        resp = self.tcp.receive()

    def login(self):
        """
        Prompt user input for login
        TODO: add login functionality based on local database

        Return: None
        """

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

        first_name = self.get_validated_input('First name: ', minlen=1, maxlen=50)

        if not first_name:
            return

        surname = self.get_validated_input('Surname: ', minlen=1, maxlen=50)

        if not surname:
            return

        uname_invalid_msg = 'Invalid username. Must be between 5 and 25 characters (inclusive)'
        uname_invalid_msg += ', start and end with a letter, and can only contain letters'
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
        invalid_email_msg = 'Invalid email, please ensure you are entering a valid email'

        while True:
            email = self.get_validated_input(
                'Email: ',
                val_func=self.auth.validate_email,
                val_func_msg=invalid_email_msg
            )

            if self.auth.username_available(email):
                break

            print('Email already registered, please log in or register a new email')

        password = None

        password = self.get_validated_input(
            'Password: ',
            minlen=8,
            maxlen=110,
            reg=r'.*[0-9].*',
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
                print('skipping confirm')
                return uinput
            print('confirming')

            cfrm = getpass('Type again to confirm')

            if cfrm == 'exit':
                return False

            if uinput == cfrm:
                return uinput

            print('Inputs do not match, please try again')

    def login_fr(self):
        username = self.face_rec.login(timeout=20)

        if not username:
            return

        self.__start_session(username)
