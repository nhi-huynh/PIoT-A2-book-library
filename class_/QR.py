from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
from class_.Validator import Validator


class QR:
    """
    A class used to represent the QR return system

    Attributes:
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
        print("Please hold your QR code up infront of the camera")
        while(found is False):
            frame = self.vstream.read()
            frame = imutils.resize(frame, width=400)
            qrcodes = pyzbar.decode(frame)

            for qr in qrcodes:
                qrcodeData = qr.data.decode("utf-8")
                if qrcodeData not in self.found:
                    self.found.add(qrcodeData)
                    if self.validator.validateISBN(qrcodeData) is True:
                        self.foundISBN = qrcodeData
                        self.stop()
                        found = True
                        break
            time.sleep(2.0)
        self.stop()
        return self.foundISBN

    def stop(self):
        """A function created to stop the camera from recording"""
        self.vstream.stop()
        return
