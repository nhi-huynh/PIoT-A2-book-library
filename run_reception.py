# vim: set et sw=4 ts=4 sts=4:

from config import CONFIG_RP
from class_.Auth import Auth
from class_.DBInterface import DBInterface
from class_.Reception import Reception
from class_.FaceRecognition import FaceRecognition

dbi = DBInterface(CONFIG_RP['db'])
auth = Auth(dbi)
fr = FaceRecognition()

reception_pi = Reception(config=CONFIG_RP, dbi=dbi, auth=auth, face_recognition=fr)

reception_pi.start()


