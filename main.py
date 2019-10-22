#!/usr/bin/env python2

import RFM69
from RFM69registers import *
import datetime
import time

rfmModule = RFM69.RFM69(RF69_433MHZ, 1, 1, True)
rfmModule.shutdown()

print "class initialized"
print "reading all registers"
results = rfmModule.readAllRegs()
for result in results:
    print result
print "Performing rcCalibration"

rfmModule.writeReg(REG_FDEVMSB, 0x00)
rfmModule.writeReg(REG_FDEVLSB, 0x4a)

freqHz = 434790000
freqHz /= 61.03515625 # divide down by FSTEP to get FRF
freqHz = int(freqHz) + 35
rfmModule.writeReg(REG_FRFMSB, freqHz >> 16)
rfmModule.writeReg(REG_FRFMID, freqHz >> 8)
rfmModule.writeReg(REG_FRFLSB, freqHz)

rfmModule.writeReg(REG_OPMODE, RF_OPMODE_SEQUENCER_ON | RF_OPMODE_LISTEN_OFF | RF_OPMODE_TRANSMITTER)
rfmModule.writeReg(REG_DATAMODUL, RF_DATAMODUL_DATAMODE_PACKET | RF_DATAMODUL_MODULATIONSHAPING_00)
#rfmModule.writeReg(REG_BITRATEMSB, 0xF4)
#rfmModule.writeReg(REG_BITRATELSB, 0xF4)
rfmModule.writeReg(REG_BITRATEMSB, RF_BITRATEMSB_1200)
rfmModule.writeReg(REG_BITRATELSB, RF_BITRATELSB_1200)
#rfmModule.writeReg(REG_BITRATEMSB, 0xFF)
#rfmModule.writeReg(REG_BITRATELSB, 0xFF)

rfmModule.writeReg(REG_DIOMAPPING1, RF_DIOMAPPING1_DIO0_00)
rfmModule.writeReg(REG_DIOMAPPING2, RF_DIOMAPPING2_CLKOUT_OFF)

rfmModule.writeReg(REG_PACKETCONFIG1, RF_PACKET1_FORMAT_FIXED | RF_PACKET1_DCFREE_OFF | RF_PACKET1_CRC_OFF | RF_PACKET1_CRCAUTOCLEAR_ON | RF_PACKET1_ADRSFILTERING_OFF)
rfmModule.writeReg(REG_PAYLOADLENGTH, 0x00)
rfmModule.writeReg(REG_FIFOTHRESH, RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY | RF_FIFOTHRESH_VALUE)
rfmModule.writeReg(REG_PREAMBLELSB, 0x00)
rfmModule.writeReg(REG_IRQFLAGS2, RF_IRQFLAGS2_FIFOOVERRUN)
rfmModule.rcCalibration()
print "setting high power"
rfmModule.setHighPower(True)

print "Checking temperature"
print rfmModule.readTemperature(0)
# print "setting encryption"
# rfmModule.encrypt("1234567891011121")
print "sending blah to 2"
rfmModule.setMode(RF69_MODE_SYNTH)
#wait for modeReady
time.sleep(10)
while (rfmModule.readReg(REG_IRQFLAGS1) & RF_IRQFLAGS1_MODEREADY) == 0x00:
    pass


import uuid

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.





from pocsag import encodeTXBatch

msgs = []
#msgs.append([True, "133709", "1234567890U[]-"])
"""
msgs.append([False, "133722", 'Zeile 1\nZeile 2\nZeile 3\nZeile 4'])
msgs.append([False, "133742", '1234567890^12w3e4rt5zu<yxcvf1qwerdftgzhj123we4rwt5dezghqwertwe6456e5n6er6n45w6n456n45'])
msgs.append([True, "133782", "1234567890U-()"])
"""
for i in range(1):
    msgs.append([False, "133702", my_random_string(80)])

data = encodeTXBatch(msgs)
rfmModule.sendBuffer(data)

rfmModule.shutdown()
