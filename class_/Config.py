# vim: set expandtab sw=4 ts=4 sts=4:
import json


class Config:
    """
    Reads and gets configurations for the app from the config json file.
    Configuration includes:
    Socket
    Local database
    Cloud database 
    Cloud visual representation credentials
    """

    socket = None

    def __init__(self, file_path='config_main.json'):
        """
        Reads in config file and extract config values

        :type file_path : string
        :param file_path : config file
        """
        try:
            f = open(file_path, 'r')
        except:
            print("Unable to open config file")
            return

        cfg = json.load(f)

        f.close()       
        # get socket config
        if 'socket' in cfg:
            socket = cfg['socket']

            required = [
                'master_ip',
                'reception_ip',
                'port'
            ]           
            socket_valid = True

            for req in required:
                if req not in socket:
                    print("missing socket config: {}".format(req))
                    socket_valid = False   

            if socket_valid is True:
                self.socket = socket

    def get_socket_config(self):
        return self.socket
