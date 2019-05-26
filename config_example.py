# vim: set et sw=4 ts=4 sts=4:

"""

Copy this file to config.py and edit as required


"""

# Only needed on the reception pi
CONFIG_RP = {
    'db': {
        # DB containing login data, run setup.sql to set up
        'host': 'localhost',
        'port': None,
        'user': 'db_username',
        'passwd': 'db_password',
        'database': 'db_name'
    },
    'socket': {
        # For connecting to the Master Pi

        # REQUIRED

        # Whether you'll input the Master Pi ip manually
        # or set up auto connection
        # valid options: 'manual' or 'auto'
        'method': 'auto',

        # INT, port number for connecting to Master Pi
        'port': 1234, 

        # Reception Pi private key
        # See the readme for setting up
        'keyfile': 'keys/key-rp.pem',

        # Master pu public key
        'mp-pubkey': 'keys/key-mp.pub',

        # /REQUIRED

        # If using method = manual
        'ip': '192.168.1.2', # Master Pi ip
        # /manual

        # If using method = auto

        # IP of the device being used to sync the address
        'sync_ip': '60.60.60.60',

        # INT, port of the same device
        'sync_port': 4321,

        # public key of the same device
        'sync-pubkey': 'keys/key-sync.pub'

        # /auto
    }
}


# Only needed on the Master Pi
CONFIG_MP = {
    'db': {
        # DB containing Library data
        'host': 'localhost',
        'port': None,
        'user': 'db_username',
        'passwd': 'db_password',
        'database': 'db_name'
    },
    'socket': {
        # REQUIRED

        # Must be set to the same value as in CONFIG_RP
        'method': 'auto',
        'port': 1234, # For connecting to RP
        'rp-pubkey': 'keys/key-rp.pub', # Reception Pi public key
        'keyfile': 'keys/key-mp.pem', # Master Pi private key

        # /REQUIRED

        # Needed for method = auto
        # Must be set to the same values as in CONFIG_RP
        'sync_ip': '60.60.60.60',
        'sync_port': 4321,
        # /auto
    },
    'gc': {
        # Credentails and tokens for google calendar
        'credentials_path': 'gc_credentials.json',
        'token_path': 'gc_token.json'
    }
}

# Only needed on the device hosting the sync service
# Only needed if method = auto
CONFIG_SYNC = {
    # Where the public key is stored
    'mp-pubkey': 'keys/key-mp.pub',
    # Port to listen on
    'port': 4321
}
