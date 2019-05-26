# vim: set et sw=4 ts=4 sts=4:
from class_.RSA import RSA
from random import randint
import socket
import time


class MasterConnection():
    """
    A class used to represent the Master Connection

    Attributes:
        __config : string
            Connection config
        __conn : TCP
            Main TCP connection to reception pi
        __sync_conn : TCP
            temp connection during init for uploading our lan ip
        __rsa_mp : RSA
            RSA object for the master pi keypair
        __rsa_rp : RSA
            RSA object for reception pi public key
    """

    def __init__(self, config):
        self.__config = config
        self.__conn = TCP()
        self.__sync_conn = TCP()

        rsa_mp = RSA()
        rsa_mp.load_keys(config['keyfile'])

        rsa_rp = RSA()
        rsa_rp.load_public_key(config['rp-pubkey'])

        self.__rsa_mp = rsa_mp
        self.__rsa_rp = rsa_rp

        if config['method'] == 'manual':
            self.__config['remote_ip'] = config['ip']
            return

        lan_ip = self.__get_self_lan_ip()

        if lan_ip is None:
            raise Exception('Failed to find lan ip')

        self.__lan_ip = lan_ip

        while True:
            if self.__attempt_ip_sync():
                self.__sync_conn.disconnect()
                break

            time.sleep(4)

    def __attempt_ip_sync(self):
        """
        A function created to upload the lan ip in an encrypted format

        Returns:
            True if no errors or nulls
            False if there is
        """

        res = self.__sync_conn.connect(
            self.__config['sync_ip'],
            self.__config['sync_port']
        )

        if not res:
            return False

        self.__sync_conn.send_all('put')

        challenge = self.__sync_conn.receive()

        if not challenge:
            return False

        challenge = self.__rsa_mp.private_decrypt(challenge)

        if not challenge:
            return False

        self.__sync_conn.send_all(challenge)

        if self.__sync_conn.receive() != 'ready':
            return False

        self.__sync_conn.send_all(self.__rsa_rp.public_encrypt(self.__lan_ip))

        if self.__sync_conn.receive() != 'bye':
            return False

        return True

    def connect(self, wait=True, timeout=None, attempt_interval=5):
        """
        Listens for connections from the reception pi and verifies identity

        Args:
            wait: bool to wait
            timeout: time value to timeout
            attempt_interval: interval time value

        Returns:
            True if sucessful
            False if not
        """

        deadline = False

        if timeout is not None and timeout > 0:
            deadline = time.time() + timeout

        while True:
            if deadline and time.time() > deadline:
                return False

            res = self.__conn.listen('0.0.0.0', self.__config['port'])

            if not res:
                time.sleep(attempt_interval)
                continue

            rnd = str(randint(100000, 99999999))

            msg = self.__conn.receive()

            if msg != 'hello':
                time.sleep(attempt_interval)
                continue

            challenge = self.__rsa_rp.public_encrypt(rnd)

            res = self.__conn.send_all(challenge)

            if res is False:
                time.sleep(attempt_interval)
                continue

            resp = self.__conn.receive()

            if resp == rnd:
                self.__conn.send_all('success')
                return True

            self.__conn.send_all('fail')
            time.sleep(attempt_interval)

    def __get_self_lan_ip(self):
        """
        Finds the lan ip of this devices

        Returns:
            ip address
        """

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = None
        finally:
            s.close()

        return ip

    def send_all(self, msg):
        """
        Sends msg to connected partner

        Args:
            msg: message to be sent
        """
        return self.__conn.send_all(msg)

    def receive(self):
        """A function created to recieve"""
        return self.__conn.receive()

    def disconnect(self):
        """A function created to disconnect"""
        self.__conn.disconnect()


class ReceptionConnection:
    """
    A class used to represent the Reception Connection

    Attributes:
        __config : dict
            connection config
        __conn : TCP
            main TCP connection to master pi
        __sync_conn : TCP
            temp tcp connection to sync servic
        __rsa_mp : RSA
            RSA object for master pi public key
        __rsa_rp : RSA
            RSA object for reception pi keypair
    """

    def __init__(self, config):
        self.__conn = TCP()
        self.__config = config

        rsa_rp = RSA()
        rsa_rp.load_keys(config['keyfile'])

        rsa_mp = RSA()
        rsa_mp.load_public_key(config['mp-pubkey'])

        self.__rsa_rp = rsa_rp
        self.__rsa_mp = rsa_mp

        if config['method'] == 'manual':
            self.__config['remote_ip'] = config['ip']
            return

        sync_conn = TCP()

        while True:
            try:
                sync_conn.connect(config['sync_ip'], config['sync_port'])
                sync_conn.send_all('get')

                ciphertext = sync_conn.receive()
            except:
                time.sleep(5)
                continue

            if not ciphertext or ciphertext == 'wait':
                time.sleep(5)
                continue

            plaintext = rsa_rp.private_decrypt(ciphertext)

            if not plaintext:
                time.sleep(5)
                continue

            break

        sync_conn.disconnect()

        self.__config['remote_ip'] = plaintext

    def connect(self, wait=True, timeout=None, attempt_interval=5):
        """
        Attempts to connect to master pi

        Args:
            wait: whether to wait until connected
            timeout: max time to attempt to connect
            attempt_interval: Time to wait between attempts

        Returns:
            True if sucessful
            False if not
        """

        deadline = False

        if timeout is not None and timeout > 0:
            deadline = time.time() + timeout

        while True:
            if deadline and time.time() > deadline:
                return False

            res = self.__conn.connect(
                self.__config['remote_ip'],
                self.__config['port']
            )

            if not res:
                time.sleep(attempt_interval)
                continue

            if not self.__conn.send_all('hello'):
                time.sleep(attempt_interval)
                continue

            chal = self.__conn.receive()

            if chal is False:
                time.sleep(attempt_interval)
                continue

            ans = self.__rsa_rp.private_decrypt(chal)

            if not ans:
                time.sleep(attempt_interval)
                continue

            res = self.__conn.send_all(ans)

            if not res:
                time.sleep(attempt_interval)
                continue

            resp = self.__conn.receive()

            if resp == 'success':
                return True

            time.sleep(attempt_interval)

    def send_all(self, msg):
        """
        Sends msg to connection partner

        Args:
            msg: message to be sent
        """
        return self.__conn.send_all(msg)

    def receive(self):
        """Attempts to receive a message from connection partner"""
        return self.__conn.receive()

    def disconnect(self):
        """Disconnect from connection partner"""
        self.__conn.disconnect()


class SyncConnection:
    """
    A class to sync the master pi lan ip between the Master and Reception Pi's

    Attributes:
        __conn : TCP
            the link to the TCP script
        __rsa_mp : RSA
            the link to the RSA script
        __latest_ip : string
            the ip
    """

    def __init__(self, config):
        rsa_mp = RSA()
        rsa_mp.load_public_key(config['mp-pubkey'])
        self.__latest_ip = None

        self.__rsa_mp = rsa_mp

        self.__conn = TCP()

        while True:
            time.sleep(1)
            res = self.__conn.listen('0.0.0.0', config['port'])

            if not res:
                continue

            msg = self.__conn.receive()

            if msg not in ['get', 'put']:
                continue

            if msg == 'get':
                self.handle_get()
            else:
                self.handle_put()

    def handle_get(self):
        """Sends the encrypted ip. If there is none, sends 'wait' """
        if self.__latest_ip is None:
            self.__conn.send_all('wait')
            return

        self.__conn.send_all(self.__latest_ip)

    def handle_put(self):
        """ Verifies identity then, receives encrypted lan ip """

        rnd = str(randint(100000, 9999999))

        cipher = self.__rsa_mp.public_encrypt(rnd)

        self.__conn.send_all(cipher)

        resp = self.__conn.receive()

        if resp != rnd:
            self.__conn.send_all('bye')
            return

        self.__conn.send_all('ready')

        resp = self.__conn.receive()

        if resp is False:
            return

        self.__latest_ip = resp

        self.__conn.send_all('bye')


class TCP:
    """
    Wrapper for managing TCP socket communication

    Attributes:
        __sock : socket
            current socket
        __conn : socket
            Connection to peer
        __bound : bool
            Whether an address has been bound
        __bind_addr : tuple
            The current address, if bound
    """

    def __init__(self):
        self.__sock = None
        self.__conn = None
        self.__bound = False
        self.__bind_addr = None

    def __del__(self):
        """Destructor, cleans up"""
        self.disconnect()

    def connect(self, addr, port):
        """
        A function created to connect via the port and address supplied

        Args:
            addr: ip address to connect to
            port: port to connect to

        Returns:
            True if connection sucessful
            False if not
        """

        self.disconnect()

        self.__sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            self.__sock.connect((addr, port))
        except:
            return False

        self.__conn = self.__sock
        return True

    def listen(self, addr, port):
        """
        A function created to listen via the port and address supplied

        Args:
            addr: ip address to connect to
            port: port to connect to

        Returns:
            True if a peer connects
            False if anything fails
        """

        if self.__bound and (addr, port) == self.__bind_addr:
            return self.renew_listen()

        self.__sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__sock.bind((addr, port))
        except OSError as oerr:
            return False

        except:
            return False

        self.__bound = True
        self.__bind_addr = (addr, port)

        return self.__begin_listen_accept()

    def renew_listen(self):
        """
        Begin listening and wait for accept.
        Does not recreate the socket or rebind.
        Used if listening with the same ip/port.

        Returns:
            True if connection is successful
            False if error
        """

        if not self.__bound:
            return False

        try:
            self.__conn.close()
        except:
            pass

        return self.__begin_listen_accept()

    def __begin_listen_accept(self):
        """
        Begins listening and waits to accept a connection

        Returns:
            True if sucessful
            False if not
        """

        try:
            self.__sock.listen()
            self.__conn, self.__remote_addr = self.__sock.accept()
            return True
        except:
            return False

    def disconnect(self):
        """A function created to disconnect"""

        try:
            self.__conn.close()
        except:
            pass

        try:
            self.__sock.close()
        except:
            pass

        self.__bound = False

    def send_all(self, msg):
        """
        Sends a message to connected peer

        Args:
            msg: string message to send

        Returns:
            True if msg was sent
            False if error
        """

        if self.__conn is None:
            return False

        encoded = True

        if not isinstance(msg, bytes):
            msg = msg.encode()
            encoded = False

        msg_data = b'1' if encoded else b'0'
        msg_data += msg

        try:
            self.__conn.sendall(msg_data)
            return True
        except:
            return False

    def receive(self):
        """
        A function created to recieve a message

        Returns:
            string or bytes
            False if error
        """

        if self.__conn is None:
            return False

        try:
            data = self.__conn.recv(4096)
        except:
            return False

        if data[0:1:] == b'1':
            return data[1::]
        else:
            return data.decode()[1::]
