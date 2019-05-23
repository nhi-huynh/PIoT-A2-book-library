""" vim: set et sw=4 ts=4 sts=4:

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

class Auth:
    """
    A class used to handle authentication and authorisation

    Attributes
    ----------
    __dbi : database interface
        Database interface from DBInterface
    """

    @staticmethod
    def encrypt_passwd(passwd):
        """
        A fuction created to encrypt a password

        Args:
            passwd: password to encrypt

        Returns:
            bytes: salt(base64 encoded) + cipher

        Raises:
            Exception if invalid password format received
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
        """
        A fuction created to verify a password

        Args:
            passwd: password to verify
            cipher: password encrypted using Auth.encrypt_passwd()

        Returns:
            True on sucsess
            False on fail

        Raises:
            Exception if invalid password format received
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
            return decrypted_passwd == passwd
        except:
            return False

    @staticmethod
    def __get_fernet(passwd, salt):
        """
        A fuction created to symmetrically encrypt

        Args:
            passwd: password to verify
            salt: random data used as additional input for hashing

        Returns:
            the key
        """

        backend = default_backend()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=300000,
            backend=backend
        )

        key = kdf.derive(passwd)

        key = urlsafe_b64encode(key)

        return Fernet(key)
