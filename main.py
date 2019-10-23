#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import RFM69_POCSAG
from RFM69_POCSAGregisters import *
import datetime
from threading import Timer
import time
from ConfigParser import SafeConfigParser
import pika
import os
import json

config = SafeConfigParser()
config.read('config.ini')
if not config.has_section('main'):
    config.add_section('main')
    config.set('main', 'amqpURI', 'amqp://user:pw@host:port')
try:
	with open('config.ini', 'w') as f:
	    config.write(f)
except Exception:
	pass
rfmModule = RFM69_POCSAG.RFM69_POCSAG(RF69_433MHZ, pocsagBaudRate=1200, isRFM69HW = True)
#rfmModule.shutdown()

print "Performing rcCalibration"

freqHz = 434790000
freqHz /= 61.03515625 # divide down by FSTEP to get FRF
freqHz = int(freqHz) + 35 # offset per chip (you may have to calibrate)
rfmModule.setFreqeuncy(freqHz)

rfmModule.rcCalibration()
rfmModule.setHighPower(True)


os.system("echo heartbeat | sudo tee /sys/class/leds/led0/trigger")

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


from pocsag import encodeTXBatch

inputQueue = []
txQueue = []
def batchFinal():
    global t
    global inputQueue
    global txQueue
    #print(" [x] Batch Final")
    txQueue = inputQueue
    inputQueue = []
    #print(txQueue)
    if len(txQueue) > 0:
        os.system("echo timer | sudo tee /sys/class/leds/led0/trigger")
        data = encodeTXBatch(txQueue, repeatNum=2)
        rfmModule.sendBuffer(data)
        os.system("echo heartbeat | sudo tee /sys/class/leds/led0/trigger")
    resetTimer()
t = Timer(.5, batchFinal)
t.start()
def resetTimer():
    global t
    if t.is_alive():
        t.cancel()
    t = Timer(.5, batchFinal)
    t.start()
def msgCallback(ch, method, properties, body):
    global inputQueue
    msg = byteify(json.loads(body))
    print(msg)
    address = '13370' + msg[0]
    message = msg[1]
    """.encode('ascii', 'ignore')

    message = message.replace("Ä", '[')
    message = message.replace("Ü", '[')
    message = message.replace("Ö", '\\')

    message = message.replace("ä", '{')
    message = message.replace("ö", '|')
    message = message.replace("ü", '}')
    message = message.replace("ß", '~')

    message = str(message.encode('ascii', 'ignore'))
    #message = message.replace(/(\r\n|\n|\r)/gm, '')
    """
    print(" [x] Received", address, message)
    inputQueue.append([False, address, message])
    #resetting timer
    resetTimer()
while True:
    try:
        print(' [*] Connecting')
        connection = pika.BlockingConnection(pika.URLParameters( config.get('main', 'amqpURI') ))
        channel = connection.channel()
        queue = channel.queue_declare(queue='input', durable=True)
        queue_ttl60 = channel.queue_declare(queue='input_ttl60', durable=True, arguments={ "x-message-ttl": 60000 })
        channel.basic_consume(queue='input',
                            auto_ack=True,
                            on_message_callback=msgCallback)
        channel.basic_consume(queue='input_ttl60',
                            auto_ack=True,
                            on_message_callback=msgCallback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        break
    except pika.exceptions.ConnectionClosed:
        print 'oops. lost connection. trying to reconnect.'
        # avoid rapid reconnection on longer RMQ server outage
        time.sleep(0.5)
    except Exception:
        print 'oops. fail.'
        # avoid rapid reconnection on longer RMQ server outage
        time.sleep(0.5) 

"""
msgs = []
msgs.append([False, "133722", 'Zeile 1\nZeile 2\nZeile 3\nZeile 4'])
msgs.append([False, "133742", '1234567890^12w3e4rt5zu<yxcvf1qwerdftgzhj123we4rwt5dezghqwertwe6456e5n6er6n45w6n456n45'])
msgs.append([True, "133782", "1234567890U-()"])
"""
#msgs.append([False, "133702", my_random_string(80)])

#time.sleep(2000)
#rfmModule.shutdown()
