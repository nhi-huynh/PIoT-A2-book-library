# vim: set et sw=4 ts=4 sts=4:

from config import CONFIG_MP, CONFIG_RP
from class_.Auth import Auth
from class_.DBInterface import DBInterface
from class_.Reception import Reception

dbi = DBInterface(CONFIG_RP['db'])
auth = Auth(dbi)

reception_pi = Reception(config=CONFIG_RP['socket'], dbi=dbi, auth=auth)

reception_pi.start()


