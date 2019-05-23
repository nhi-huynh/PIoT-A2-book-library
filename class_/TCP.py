# vim: set et sw=4 ts=4 sts=4:

from class_.RSA import RSA
from random import randint
import socket
import time

class MasterConnection():
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

            rnd = str(randint(100000,99999999))

            msg = self.__conn.receive()

            if msg != 'hello':
                time.sleep(attempt_interval)
                continue

            challenge = self.__rsa_rp.public_encrypt(rnd)

            res = self.__conn.send_all(challenge)

            if res == False:
                time.sleep(attempt_interval)
                continue

            resp = self.__conn.receive()

            if resp == rnd:
                self.__conn.send_all('success')
                return True

            self.__conn.send_all('fail')
            time.sleep(attempt_interval)

    def __get_self_lan_ip(self):
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
        return self.__conn.send_all(msg)

    def receive(self, msg):
        return self.__conn.receive()

    def disconnect(self):
        self.__conn.disconnect()

class ReceptionConnection:
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

            if chal == False:
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
        return self.__conn.send_all(msg)

    def receive(self, msg):
        return self.__conn.receive()

    def disconnect(self):
        self.__conn.disconnect()

class SyncConnection:
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

            if msg not in ['get','put']:
                continue

            if msg == 'get':
                self.handle_get()
            else:   
                self.handle_put()

    def handle_get(self):
        if self.__latest_ip is None:
            self.__conn.send_all('wait')
            return

        self.__conn.send_all(self.__latest_ip)

    def handle_put(self):

        rnd = str(randint(100000,9999999))

        cipher = self.__rsa_mp.public_encrypt(rnd)
        
        self.__conn.send_all(cipher)

        resp = self.__conn.receive()

        if resp != rnd:
            self.__conn.send_all('bye')
            return

        self.__conn.send_all('ready')

        resp = self.__conn.receive()

        if resp == False:
            return

        self.__latest_ip = resp

        self.__conn.send_all('bye')

class TCP:
    def __init__(self):
        self.__sock = None
        self.__conn = None
        self.__bound = False
        self.__bind_addr = None

    def __del__(self):
        self.disconnect()

    def connect(self, addr, port):
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
        if self.__bound and (addr, port) == self.__bind_addr:
            return self.renew_listen()


        self.__sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            # Resuse addr if reconnecting, otherwise it can't be connected to
            # until TIME_WAIT state expires for original connection
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
        if not self.__bound:
            return False

        try:
            self.__conn.close()
        except:
            pass

        return self.__begin_listen_accept()

    def __begin_listen_accept(self):

        try:
            self.__sock.listen()
            self.__conn, self.__remote_addr = self.__sock.accept()
            return True
        except:
            return False


    def disconnect(self):
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
