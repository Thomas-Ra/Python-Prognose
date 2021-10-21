#!/usr/bin/env python3.10
# Created by ...
__version__ = 0.01

import logging 
from configparser import ConfigParser

def MarketPrediction():
    print('Market Prediction is starting up...')
    logging.info('Market Prediction started')

#CONFIG
config = ConfigParser()
config.read("../config.ini")

    
#DB

#Logging
SERVERCONFIG = config["SERVERCONFIG"]
logging.basicConfig(filename='SERVERCONFIG,["LOGGING_LOCATION"]', encoding='utf-8', level=logging.SERVERCONFIG,["LOGGING_LEVEL"])
print (SERVERCONFIG)

#GUI

if __name__ == '__main__':
    MarketPrediction()
