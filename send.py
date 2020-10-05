


"""
'temp_humidity.py'
==================================
Example of sending analog sensor
values to an Adafruit IO feed.

Author(s): Brent Rubell

Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity

Dependencies:
    - Adafruit IO Python Client
        (https://github.com/adafruit/io-client-python)
    - Adafruit_Python_DHT
        (https://github.com/adafruit/Adafruit_Python_DHT)
"""

# import standard python modules.
import time


# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '403d235a5abb43bc8f72041a8e524d52'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = 'Bagasbudhi'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
micron_feed = aio.feeds('micron')


data = '580'
data_speed = [10,2]

micron_feed = aio.feeds('micron')
print('5'.format(data))
aio.send(micron_feed.key, int(data))
