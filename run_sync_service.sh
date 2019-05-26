#!/bin/python3

import os, sys

dir = os.path.dirname(os.path.abspath(__file__))

from config import CONFIG_SYNC
from class_.TCP import SyncConnection

fpath = CONFIG_SYNC['mp-pubkey']

if fpath[0] != '/':
    CONFIG_SYNC['mp-pubkey'] = os.path.join(dir, fpath)

sconn = SyncConnection(CONFIG_SYNC)
