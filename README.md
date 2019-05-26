# RMIT-PIOT
## Programming Internet of Things Assignment Two
This project has been created for the unit Programming Internet of Things(COSC2755) Assignment Two at RMIT

### Contributors
s3663435 - Claire Taylor-Cuthbertson

s3652578 - Nhi Huynh

s3662167 - Graeme Fitt

s3652122 - Adam Bin Anis

### About
The aim of assignment is to build a prototype for a Smart Library IoT Application. The application must be created for two types of users; library user and library admin

### Requirements
- Python 3.*
- Raspberry Pi 3+
- Raspberry Pi Sense Hat
- Raspberry Pi compatible Webcam

### Setting up

SETTING UP KEYS

    Run generate_keypair.py to create a new keypair

    This will create a 'keys' directory if it doesn't
    exist. Inside that directory it will create two
    new .pub and .pem keys.  .pem is private, .pub is
    public.  It will not create them if there there are
    already keys with that name

    Generate keys for reception pi and master pi

    The reception pi and master pi should have each
    other's public keys (but obviously not each other's
    private keys)

    Keys can be stored anywhere as long as it's reflected
    in the main config

    If using automatic connection:
        Generate another keypair for the device used
        for the sync service

        Make sure each device has each pub file


MAIN CONFIG
    Read through config_example.py


WEBAPP CONFIG
    Read through admin_webapp/instance/config_example.py


AUTOMATIC CONNECTION

    You will need a third device on a static ip.
    Make any required changes to config.py.

    It's recommended to run this as a systemd service.
    You may run it manually for testing

    Setting up the service:
        Open example.service and edit the ExecStart path
    to point to run_sync_service.sh

    Rename it (e.g. "ip.sync.service")

    copy it to /etc/systemd/system/ip.sync.service

    enable and start the service:
        "sudo systemctl enable ip.sync && sudo systemctl start ip.sync"

    Check to make sure it's working (Look for "Active: active(running)"):
        "sudo systemctl status ip.sync"


### Built With
* Sense Hat
* MySQLdb (DBInterface.py, voice_search.py)
* mysql.connector (DBInterface.py)
* flask
* googleapiclient (g_calendar.py)
* httplib2 (g_calendar.py)
* oauth2client (g_calendar.py)
* imutils (QR.py, FaceRecognition.py)
* imutils.video (QR.py, FaceRecognition.py)
* pyzbar (QR.py)
* cv2 (QR.py, FaceRecognition.py)
* numpy (FaceRecognition.py)
* face_recognition (FaceRecognition.py)
* cryptography.hazmat (Auth.py)
* cryptography.fernet (Auth.py)
* speech_recognition (voice_search.py)


### Acknowledgments
* COSC2755 Tutorial scripts and Lecutre example scripts
