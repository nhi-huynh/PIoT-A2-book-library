import speech_recognition as sr
import MySQLdb
import subprocess

HOST = "35.189.60.60"
USER = "root"
PASSWORD = "piot"
DATABASE = "Library"       # Database name

MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"


class VoiceSearchUtils:
    def voiceSearch(self):
        # To test searching without the microphone uncomment this line of code
        # return input("Enter the first name to search for: ")

        # Set the device ID of the mic that we
        # specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(
                                    sr.Microphone.list_microphone_names()):
            if(microphone_name == MIC_NAME):
                device_id = i
                break

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone(device_index=device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print("Say something to search for books: ")
            try:
                audio = r.listen(source, timeout=1.5)
            except sr.WaitTimeoutError:
                return None

        # recognize speech using Google Speech Recognition
        translation = None
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(
            # audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            translation = r.recognize_google(audio)
        except(sr.UnknownValueError, sr.RequestError):
            pass
        finally:
            return translation
