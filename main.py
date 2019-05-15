# vim: set et sw=4 ts=4 sts=4:

from config import CONFIG
from class_.User import User
from class_.Auth import Auth
from class_.DBInterface import DBInterface
from class_.Reception import Reception

dbi = DBInterface(CONFIG['db'])
auth = Auth(dbi)

reception_pi = Reception(dbi=dbi, auth=auth)

reception_pi.start()


