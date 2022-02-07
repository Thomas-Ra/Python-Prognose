#!/usr/bin/env python3
# Created by [WS21-Group C] 
__version__ = 1.0

import logging 
import os
import gui.gui
from configparser import ConfigParser
from webserver import server


def MarketPrediction():
    print('Market Prediction is starting up...')

#Call GUI Class
    logging.info('GUI started')
    #gui()

#Call Wevserver Class
    webserver = server.handler()
    webserver.mainloop()
    logging.info('Webserver started')

    logging.info('Market Prediction started')

#CONFIG
config = ConfigParser()
config.read(os.getcwd() + "\config.ini")

#Logging
SERVERCONFIG = config["SERVERCONFIG"]
logging.basicConfig(filename=SERVERCONFIG["LOGGING_LOCATION"], encoding='utf-8', level=SERVERCONFIG["LOGGING_LEVEL"])

#MAIN
if __name__ == '__main__':
    MarketPrediction()
