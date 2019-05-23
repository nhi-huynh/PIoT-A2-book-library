# vim: set et sw=4 ts=4 sts=4:

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat
from cryptography.hazmat.primitives.serialization import NoEncryption, load_pem_private_key, load_pem_public_key

class RSA:

    def __init__(self, private_key_file=None, public_key_file=None):
        self.__private = None
        self.__public = None

        if private_key_file is not None:
            self.load_keys(priate_key_file)

        if public_key_file is not None and self.__public is None:
            self.load_public_key(public_key_file)

    def generate_key(self):
        self.__private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        self.__public = self.__private.public_key()

    def export_private_key(self, fname):
        if self.__private is None:
            return False

        priv_bytes = self.__private.private_bytes(
            encoding = Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )

        with open(fname, 'wb') as f:
            f.write(priv_bytes)

    def export_public_key(self, fname):
        pub_bytes = self.__public.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        with open(fname, 'wb') as f:
            f.write(pub_bytes)

    def load_keys(self, fname):
        with open(fname, 'rb') as f:
            data = f.read()

            self.__private = load_pem_private_key(
                data,
                password=None,
                backend=default_backend()
            )

            self.__public = self.__private.public_key()

    def load_public_key(self, fname):
        with open(fname, 'rb') as f:
            data = f.read()

            self.__public = load_pem_public_key(
                data,
                backend=default_backend()
            )

    def public_encrypt(self, msg):
        if self.__public is None:
            return False

        if not isinstance(msg, bytes):
            msg = msg.encode()

        return self.__public.encrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def private_decrypt(self, cipher):
        if self.__private is None:
            return False

        try:
            plaintext =  self.__private.decrypt(
                cipher,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except:
            return False

        if isinstance(plaintext, bytes):
            return plaintext.decode()

        return plaintext
