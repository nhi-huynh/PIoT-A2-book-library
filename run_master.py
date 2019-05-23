# vim: set et sw=4 ts=4 sts=4:

from config import CONFIG_RP, CONFIG_MP
from class_.Master import Master

master_pi = Master(config=CONFIG_MP['socket'])
master_pi.start()
