#please use python version 3.7 or lower
_version__ = 1.0

import logging 
import os
from configparser import ConfigParser

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

#MAIN
if __name__ == '__main__':
    init_config()
    server_start()
    display()