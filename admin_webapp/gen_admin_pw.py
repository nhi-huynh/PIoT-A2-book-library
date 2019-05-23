# vim: set et sw=4 ts=4 sts=4:

from class_.Auth import Auth
from getpass import getpass

cipher = None

while True:
    pw = getpass('Password: ')

    if not len(pw):
        print('No password entered, exiting')
        exit()

    cf = getpass('Confirm')

    if pw != cf:
        print('Passwords do not match, please try again')
        continue

    #try:
    cipher = Auth.encrypt_passwd(pw)
    #except:
    #    print('Invalid password format, please choose a different password')
    #    continue

    break

if cipher is None:
    print('Failed, please try again')
    exit()

print('Do NOT store this in config.py')
print('Store this in admin_webapp/instance/config.py')
print('Restart after ensuring you have the following lines:\n')
print('ADMIN_USERNAME = "your_username"')
print('ADMIN_PASSWORD = "encrypted_password"')
print(cipher)








