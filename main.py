#!/usr/bin/env python2

import RFM69_POCSAG
from RFM69_POCSAGregisters import *
import datetime
import time
from ConfigParser import SafeConfigParser

config = SafeConfigParser()

rfmModule = RFM69_POCSAG.RFM69_POCSAG(RF69_433MHZ, pocsagBaudRate=1200, isRFM69HW = True)
#rfmModule.shutdown()

print "Performing rcCalibration"

freqHz = 434790000
freqHz /= 61.03515625 # divide down by FSTEP to get FRF
freqHz = int(freqHz) + 35 # offset per chip (you may have to calibrate)
rfmModule.setFreqeuncy(freqHz)

rfmModule.rcCalibration()
rfmModule.setHighPower(True)

import uuid
def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

from pocsag import encodeTXBatch
msgs = []
"""
msgs.append([False, "133722", 'Zeile 1\nZeile 2\nZeile 3\nZeile 4'])
msgs.append([False, "133742", '1234567890^12w3e4rt5zu<yxcvf1qwerdftgzhj123we4rwt5dezghqwertwe6456e5n6er6n45w6n456n45'])
msgs.append([True, "133782", "1234567890U-()"])
"""
msgs.append([False, "133702", my_random_string(80)])

data = encodeTXBatch(msgs)
rfmModule.sendBuffer(data)
time.sleep(2000)
#rfmModule.shutdown()