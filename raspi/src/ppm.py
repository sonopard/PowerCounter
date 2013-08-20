#!/usr/bin/python3
import requests
import json
from queue import Queue, Empty
import time
import datetime
import threading
import PC4004B
#from SMBus import smbus

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

tick_service_url = "http://192.168.2.176:8080/powercounter/tick"
display_service_url = tick_service_url
service_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# pin, bank, chip
ticks_queue = Queue()

display = PC4004B.PC4004B()
display.send_text("Initializing...", 1)

def jsonconsumer():
  while True:
    try:
      tick = ticks_queue.get(block=False)
    except Empty:
      time.sleep(1)
      continue
    try:
      data = {'pin': tick[0], 'bank': tick[1], 'address': tick[2], 'occurence': tick[3]}
      r = requests.post(tick_service_url, data=json.dumps(data), headers=service_headers)
    except:
      ticks_queue.put(tick)
      print("retry")
      time.sleep(2)
      continue

def gpioproducer():
  while True:
    ticks_queue.put((7,0,23,int(unix_time_millis(datetime.datetime.utcnow()))))
    time.sleep(1)

def json_display_data_updater():
  while True:
    r = requests.get(display_service_url)
    display_data = r.json
    display.send_text(str(display_data['occurence']), 2) 
    time.sleep(10)    

threading.Thread(target = json_display_data_updater).start()
threading.Thread(target = jsonconsumer).start()
threading.Thread(target = gpioproducer).start()

while 1:
  pass
