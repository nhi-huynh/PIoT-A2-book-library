#!/usr/bin/env python3

from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
from class_.Validator import Validator

# import numpy as np
# import sys


class QR:
    """
    A class used to represent the QR return system

    Attributes
    ----------
    foundISBN : string
        the isbn decoded from the QR code
    validator : Validator
        the link to the validator script
    vstream : VideoStream
        the camera used to capture the QR code
    found : set
        the set of QR codes found
    """

    def __init__(self):
        self.foundISBN = ""
        self.validator = Validator()
        # self.vstream = VideoStream(usePiCamera=True).start()
        self.vstream = VideoStream(src=0).start()
        self.found = set()
        # allow the camera to warm up
        time.sleep(5.0)

    def readQR(self):
        """
        A function created to read/capture the qr code from the camera

        Returns:
            the decoded isbn
        """
        found = False
        while(found is False):
            frame = self.vstream.read()
            frame = imutils.resize(frame, width=400)

            qrcodes = pyzbar.decode(frame)

            for qr in qrcodes:
                qrcodeData = qr.data.decode("utf-8")
                if qrcodeData not in self.found:
                    print("[FOUND] Data: {}".format(qrcodeData))
                    self.found.add(qrcodeData)
                    if self.validator.validateISBN(qrcodeData) is True:
                        self.foundISBN = qrcodeData
                        self.stop()
                        found = True
                        break
            time.sleep(2.0)

        return self.foundISBN

    def stop(self):
        self.vstream.stop()
        return
