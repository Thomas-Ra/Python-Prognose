#!/usr/bin/env python3
# Created by ...
__version__ = 0.01

import logging 
from configparser import ConfigParser
import os
import gui.gui
from finance.finance import make_plot

def MarketPrediction():
    print('Market Prediction is starting up...')
    logging.info('Market Prediction started')
    make_plot("TSLA")
    gui()

#CONFIG
config = ConfigParser()
config.read(os.getcwd() + "\config.ini")


    
#DB

#Logging
SERVERCONFIG = config["SERVERCONFIG"]
logging.basicConfig(filename=SERVERCONFIG["LOGGING_LOCATION"], encoding='utf-8', level=SERVERCONFIG["LOGGING_LEVEL"])

#GUI

if __name__ == '__main__':
    MarketPrediction()
