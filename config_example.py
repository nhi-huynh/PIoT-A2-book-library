# vim: set et sw=4 ts=4 sts=4:

CONFIG_RP = {
    'db': {
        # DB containing login data
        'host': 'localhost',
        'port': None,
        'user': 'db_username',
        'passwd': 'db_password',
        'database': 'db_name'
    },
    'socket': {
        # You need these options
        'method': 'auto', # manual or auto
        'port': 1234, # For connecting to MP
        'keyfile': 'keys/key-rp.pem',
        'mp-pubkey': 'keys/key-mp.pub',

        # Needed for method = manual
        'ip': '192.168.1.2', # MP ip

        # Needed for method = auto
        'sync_ip': '60.60.60.60',
        'sync_port': 4321,
        'sync-pubkey': 'keys/key-sync.pub'
    }
}

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
        # You need these
        'method': 'auto', # manual or auto
        'port': 1234, # For connecting to RP
        'rp-pubkey': 'keys/key-rp.pub'
        'keyfile': 'keys/key-mp.pem',

        # Needed for method = auto
        'sync_ip': '60.60.60.60',
        'sync_port': 4321,
    },
    'gc': {
        # Credentails and tokens for google calendar
        'credentials_path': 'gc_credentials.json',
        'token_path': 'gc_token.json'
    }
}

# Only needed if manual = auto for the other socket settings
CONFIG_SYNC = {
    'mp-pubkey': 'keys/key-mp.pub',
    'port': 4321
}
