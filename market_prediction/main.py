#please use python version 3.7 or lower
_version__ = 1.0

import logging 
import sys
import os
from configparser import ConfigParser

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

#start the webserver
def server_start():
    from webserver import server
    server.start_in_thread()
    logging.info('Webserver started')
    

#Call GUI Class
def display():
    import gui.gui
    logging.info('GUI started')

#Logging
def init_config():
    config = ConfigParser()
    config.read(os.getcwd() + "\config.ini")
    SERVERCONFIG = config["SERVERCONFIG"]
    logging.basicConfig(filename=SERVERCONFIG["LOGGING_LOCATION"], level=SERVERCONFIG["LOGGING_LEVEL"])
    logging.info('Config initialized')
    #redirect sysout to logger
    log = logging.getLogger('System')
    sys.stdout = StreamToLogger(log,logging.DEBUG)
    sys.stderr = StreamToLogger(log,logging.ERROR)

#MAIN
if __name__ == '__main__':
    init_config()
    server_start()
    display()