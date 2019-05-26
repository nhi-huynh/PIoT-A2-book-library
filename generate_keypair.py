from class_.RSA import RSA
import os

if not os.path.isdir('keys'):
    try:
        os.mkdir('keys')
    except:
        print('Failed to create directory for keys')
        pass

fname = input('Enter file name for keys (e.g. "master_pi": ')

if os.path.isfile(fname):
    print('Files already exist, aborting')
    exit()

rsa = RSA()
rsa.generate_key()
rsa.export_private_key('keys/' + fname + '.pem')
rsa.export_public_key('keys/' + fname + '.pub')

