""" vim: set et sw=4 ts=4 sts=4:

Handles authentication and authorisation

EXAMPLES

Encrypting new user password:

    auth = Auth()
    passwd = 'user_password'
    cipher = auth.encrypt_passwd(passwd)
    # Store cipher in db


Authenticating user using password:

    auth = Auth()
    passwd = 'entered_password'
    cipher = 'cipher_from_db_for_relevant_user'
    success = auth.verify_passwd(passwd, cipher)

"""

# Imports
try:
    from os import urandom
except:
    raise Exception('Failed to import os module')

try:
    from base64 import urlsafe_b64encode, urlsafe_b64decode
except:
    raise Exception('Failed to import base64 module')

try:
    import time
except:
    raise Exception('Failed to import time module')

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet
except:
    raise Exception('cryptography module missing')

try:
    from class_.User import User
except:
    raise Exception('User.py missing')

try:
    import re
except:
    raise Exception('Failed to import regex module')
    


class Auth:
    __dbi = None


    def __init__(self, dbi):
        """
        Args:
            dbi: Database interface from DBInterface
        """
        if dbi is None:
            raise Exception('Database interface missing')
        self.__dbi = dbi
        
    def login(self, username=None, email=None, password=None):
        if password is None or (username is None and email is None):
            raise Exception('Missing arguments to Auth.login')

        if len(password) < 1:
            raise LoginException('Missing password')

            
        
        value = email if email is not None else username

        if len(value) < 1:
            raise LoginException('Username or email required')

        time_start = time.time()

        res = self.__load_user(username=username, email=email)

        if not res or not Auth.verify_passwd(password, res['passwd']):
            # Consistent check time on fail
            time.sleep(3.0 - (time.time() - time_start))
            raise Exception('Invalid login credentials')

        return User(**{x:y for x,y in res.items() if x in User.get_field_names()})

    def register(
            self,
            username=None,
            first_name=None,
            surname=None,
            email=None,
            password=None):

        """ Return User
        attempts to register user with provided info
        raises RegisterException with appropriate if anything goes wrong
        """

        data = {
            'username': username,
            'first_name': first_name,
            'surname': surname,
            'email': email,
            'password': password
        }

        missing = []

        for field, val in data.items():
            if val is None or len(val) < 1:
                missing.append(field)

        if len(missing) > 0:
            raise RegisterException('Missing fields: {}.'.format(', '.join(missing)))

        invalid = []

        if not self.__validate_username(username):
            invalid.append('username must be between 5 and 25 characters long')

        if not self.__validate_email(email):
            invalid.append('invalid email address')

        if len(first_name) > 50:
            invalid.append('First name must be at most 50 characters long')

        if len(surname) > 50:
            invalid.append('Surname must be at most 50 characters long')

        if len(password) < 6:
            invalid.append('Password must be at least 6 characters long')

        if len(password) > 110:
            invalid.append('password cannot be more than 110 characters long')

        if len(invalid) > 0:
            msg = 'Please fix the following issues:\n{}'.format('\n'.join(invalid))
            raise RegisterException(msg)

        
        existing = self.__search_for_user(username=username, email=email)

        if existing:

            taken = []

            for x in existing:
                if x['username'] == username:
                    taken.append('username')
                if x['email'] == email:
                    taken.append('email')

            msg = 'Account(s) already exist with the entered {}'.format(' and '.join(taken))
            raise RegsiterException(msg)
        
        enc_passwd = Auth.encrypt_passwd(password)

        if len(enc_passwd) > 255:
            # Just in case
            raise RegisterException('Password too long')

        sql = """
            INSERT INTO u_user (username, email, first_name, surname, `passwd`)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (username, email, first_name, surname, enc_passwd)

        res = self.__dbi.run(sql, values)

        if not res:
            raise RegisterException('Failed to create user (1)')
        
        user = self.__load_user(username=username)

        if not user:
            raise RegisterException('Failed to create user (3)')

        return User(**{x:y for x,y in user.items() if x in User.get_field_names()})

    @staticmethod
    def __validate_username(uname):
        if not (4 < len(uname) < 26):
            return False
        
        return bool(re.match(r'^[a-z][a-z0-9-_]+[a-z0-9]$', uname, re.IGNORECASE))
        
    @staticmethod
    def __validate_email(email):
        if len(email) > 255:
            # Greater than db 255 char limit
            return False

        return bool(re.match(r'^[a-z0-9.+%]+@[a-z0-9-.]+\.[a-z0-9-.]+$', email, re.IGNORECASE))

    def __load_user(self, username=None, email=None):
        if username is None and email is None:
            return False

        if email is not None:
            field = 'email'
            value = email
        else:
            field = 'username'
            value = username

        sql = """
            SELECT *
            FROM u_user
            WHERE {} = %s
        """.format(field)

        return self.__dbi.view_single(sql, value)

    def __search_for_user(self, username=None, email=None):
        fields = []
        values = []

        if username is not None:
            fields.append('username = %s')
            values.append(username)

        if email is not None:
            fields.append('email = %s')
            values.append(email)

        if len(fields) < 1:
            return False

        sql = "SELECT * FROM u_user WHERE " + ' AND '.join(fields)

        return self.__dbi.view(sql, tuple(values))

    @staticmethod
    def encrypt_passwd(passwd):
        """ Return bytes
        return is salt + cipher
        salt is base64 encoded

        Raises Exception if invalid password format received

        Args:
            passwd: password to encrypt
        """

        if not isinstance(passwd, bytes):
            try:
                passwd = passwd.encode()
            except:
                raise Exception('Invalid password format')

        salt = urandom(16)

        f = Auth.__get_fernet(passwd, salt)

        cipher = f.encrypt(passwd)

        encoded_salt = urlsafe_b64encode(salt)

        return encoded_salt + cipher

    @staticmethod
    def verify_passwd(passwd, cipher):
        """ Return bool
        True/False for success/fail

        Args:
            passwd: password to verify
            cipher: password encrypted using Auth.encrypt_passwd()
        """

        if not isinstance(passwd, bytes):
            try:
                passwd = passwd.encode()
            except:
                raise Exception('Invalid password format')

        if not isinstance(cipher, bytes):
            try:
                cipher = cipher.encode()
            except:
                raise Exception('Invalid password format')

        salt = cipher[:24:]
        cipher = cipher[24::]

        salt = urlsafe_b64decode(salt)

        f = Auth.__get_fernet(passwd, salt)

        try:
            decrypted_passwd = f.decrypt(cipher)
            return True
        except:
            return False

    @staticmethod
    def __get_fernet(passwd, salt):
        backend = default_backend()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )

        key = kdf.derive(passwd)

        key = urlsafe_b64encode(key)

        return Fernet(key)

class LoginException(Exception):
    pass

class RegisterException(Exception):
    pass
