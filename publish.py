
from Adafruit_IO import Client,Feed
import sys
import time
import os
import random
import numpy as np

ADAFRUIT_IO_KEY = '403d235a5abb43bc8f72041a8e524d52'


ADAFRUIT_IO_USERNAME = 'Bagasbudhi'

aio = Client (ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

micron_feed=aio.feeds('temperature')
micron2_feed=aio.feeds('humidity')
micron3_feed=aio.feeds('air-pressure')
micron4_feed=aio.feeds('ph')
micron5_feed=aio.feeds('pump')

while True:
    kappa1=random.randint(20,50)
    kappa2=random.randint(0,100)
    kappa3=random.randint(0,50)
    kappa4=random.randint(0.0,7.0)
    #kappa5=random.randint(0,100)
    aio.send(micron_feed.key, str(kappa1))
    aio.send(micron2_feed.key, str(kappa2))
    aio.send(micron3_feed.key, str(kappa3))
    aio.send(micron4_feed.key, str(kappa4))
    #aio.send(micron5_feed.key, str(kappa5))
    print('Publishing {0} {1} {2} '.format(kappa1,kappa2,kappa3))
    #print('Publishing {0} '.format(kappa2))
    time.sleep(5)
    
    #value=aio.receive(micron_feed.key).value
    #print(value)