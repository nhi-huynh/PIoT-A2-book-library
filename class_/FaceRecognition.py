""" vim: set et sw=4 ts=4 sts=4:

Register user:
    fr = FaceRecognition()
    res = fr.register(username)
    if res:
        succes()
    else:
        fail()

User login:
    fr = FaceRecognition()
    # This is a string of the username of the closest matching user.
    # If no users match close enough, this is false
    username = fr.login(username)
    if username:
        success(username)
    else:
        fail()
"""

# Imports
try:
    import sys
except:
    print('Failed to import sys')
    exit()

try:
    import os
except:
    print('Failed to import os')
    exit()

try:
    import time
except:
    print('Failed to import time module')
    exit()

try:
    import pickle
except:
    print('Failed to import pickle module')
    exit()

try:
    import numpy
except:
    print('Failed to import numpy')
    exit()

try:
    import cv2
except:
    print('Failed to import cv2')
    exit()

try:
    import face_recognition
except:
    print('Failed to import face_recognition')
    exit()

try:
    import imutils
except:
    print('Failed to import imutils')
    exit()

try:
    from imutils.video import VideoStream
except:
    print('Failed to import imutils')
    exit()


class FaceRecognition:
    """
    A class used to handle the Facial Recognition in the reception pi

    Attributes
    ----------
    __tolerance : float
        the tolerance value
    __data_file : string
        the pickle file name
    __user_faces : list
        the list containing all saved faces
    __face_detector : cv2
        the camera used to detect faces
    __made_user_changes : bool
        weather the user has made changes
    fpath : string
        the file path for the camera setup
    """

    __tolerance = 0.6
    __data_file = 'resources/face_data.pickle'
    __user_faces = {}
    __face_detector = None
    __made_user_changes = False
    """{ username: (face_data_1, face_data_2), ... }"""

    def __init__(self, save_file='face_data.pickle'):
        fpath = 'resources/haarcascade_frontalface_default.xml'
        self.__face_detector = cv2.CascadeClassifier(fpath)

        if not os.path.isfile(self.__data_file):
            return

        with open(self.__data_file, 'rb') as df:
            try:
                self.__user_faces = pickle.load(df)
            except:
                pass

    def __del__(self):
        """ Destructor. Saves facial data if changes were made """
        cv2.destroyAllWindows()
        if not self.__made_user_changes:
            return

        if not self.__made_user_changes:
            # Don't pickle if no changes were made
            return

        with open(self.__data_file, 'wb') as df:
            pickle.dump(self.__user_faces, df)

    def register(self, username):
        """
        A fuction created to get a user to register a facial scan

        Args:
            username: the users who is doing the facial scan

        Returns:
            True if facial scan sucessful
            False if face scan fails
        """

        print('Please position your face 30-50cm from the camera')
        input('Press the Enter key when ready')

        faces = self.__register_capture_faces(show_messages=True)

        if len(faces) < 1:
            return False

        encodings = self.__encode_faces(faces)

        if len(encodings) < 1:
            return False

        self.__user_faces[username] = encodings
        self.__made_user_changes = True

        return True

    def login(self, timeout=60, show_messages=True, capture_delay=1):
        """
        A fuction created to get a user to login using facial detection

        Args:
            timeout: time, if reached any faces found so far are returned
            show_messages: bool to show messages or not
            capture_delay: time to wait between detection attempts

        Returns:
            username of best found match
            False if face detection failes or no close enough match found
        """

        encodings = self.__capture_login_encodings(
            timeout=timeout,
            show_messages=show_messages,
            capture_delay=capture_delay
        )

        if not encodings:
            return False

        user_totals = {}

        for username, user_data in self.__user_faces.items():
            match_count = 0

            for encoding in encodings:
                # matches = face_recognition.compare_faces(
                # user_data, encoding, self.__tolerance)
                matches = face_recognition.compare_faces(user_data, encoding)
                match_count += sum(matches)

            if match_count:
                user_totals[username] = match_count

        if not len(user_totals):
            # No users matched
            return False

        return max(user_totals, key=user_totals.get)

    def __capture_login_encodings(
                            self,
                            timeout=60,
                            show_messages=True,
                            capture_delay=1):
        """
        A fuction created to register a captured login encodings

        Args:
            timeout: time, if reached any faces found so far are returned
            show_messages: bool to show messages or not
            capture_delay: time to wait between detection attempts

        Returns:
            list of encodings for single face detection if face found
            False if process not completed within 'timeout' seconds
        """

        if timeout <= 0:
            timeout = 999999

        try:
            vs = VideoStream(src=0)
            vs.start()
        except:
            raise Exception('Failed to start webcam stream')

        deadline = time.time() + timeout

        while time.time() < deadline:
            try:
                frame = vs.read()
            except:
                vs.stop()
                raise Exception('Failed to get image')

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = imutils.resize(image, 750)

            boxes = face_recognition.face_locations(image, model='hog')

            if len(boxes) == 0:
                if show_messages:
                    print('No faces found')
                time.sleep(capture_delay)
                continue

            if len(boxes) > 1:
                if show_messages:
                    print('Multiple faces found. One at a time please.')
                time.sleep(capture_delay)
                continue

            vs.stop()
            return face_recognition.face_encodings(image, boxes)

        vs.stop()
        return False

    def __register_capture_faces(
                            self,
                            timeout=60,
                            count=3,
                            capture_delay=0.1,
                            show_messages=False):
        """
        A fuction created to register a captured users face

        Args:
            timeout: time, if reached any faces found so far are returned
            count: the number of faces to capture
            capture_delay: time to wait between captures
            show_messages: bool to show messages or not

        Returns:
            list of all faces
        """

        try:
            vs = VideoStream(src=0)
            vs.start()
        except:
            raise Exception('Failed to start webcam stream')

        if timeout <= 0:
            timeout = 999999

        deadline = time.time() + timeout
        faces = []

        while len(faces) < count:
            time.sleep(capture_delay)

            if time.time() >= deadline:
                break

            frame = vs.read()

            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            found = self.__face_detector.detectMultiScale(grey, 1.3, 5)

            if len(found) == 0:
                if show_messages:
                    msg = '\n\nNo face detected\n'
                    msg += 'Ensure you are 30-50cm in front of the camera.'

                    print(msg)

                continue

            if len(found) > 1:
                if show_messages:
                    msg = '\n\nMultiple faces detected\n'
                    msg += 'Ensure you are the only one in front of the camera'

                    print(msg)

                continue

            x, y, w, h = found[0]

            faces.append(frame[y:y+h, x:x+w])
            if show_messages:
                print('\n\n{}/{} images captured'.format(len(faces), count))

        if len(faces) < count and show_messages:
            print('\n\nTimeout reached, {}/{} images captured'.format(
                len(faces), count))

        vs.stop()
        return faces

    def __encode_faces(self, faces):
        """
        A fuction created to encode the captured face

        Args:
            faces: the capture of the users face

        Returns:
            list of all encodings for all faces
        """
        all_encodings = []

        for face in faces:
            img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            """
            cnn is more accurate than hog, but slower.
            This is part of an authentication system so
            accuracy is more important
            """
            boxes = face_recognition.face_locations(img, model='hog')

            encodings = face_recognition.face_encodings(img, boxes)

            if len(encodings):
                all_encodings.append(encodings[0])

        return all_encodings

    def set_tolerance(self, val):
        """
        A fuction created to set the tolerance value

        Args:
            val: float to be assigned to tolerance

        Raises:
            Exception if val is outside the range or the wrong type
        """

        if isinstance(val, float):
            raise Exception('Invalid type for tolerance. Float required')

        if not (0 < val <= 1):
            raise Exception('Invalid tolerance value. Valid range: (0,1]')

        self.__tolerance = val
