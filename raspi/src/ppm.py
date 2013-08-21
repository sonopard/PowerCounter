#!/usr/bin/python3
import requests
import json
from queue import Queue, Empty
import time
import datetime
import threading
from PC4004B import PC4004B
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

ticks_queue = Queue()

display = PC4004B()
display.send_text("Initializing...", 1, 1)

def json_tick_consumer():
  while True:
    try:
      tick = ticks_queue.get(block=False)
    except Empty:
      time.sleep(1)
      continue
    try:
      data = {'pin': tick[0], 'bank': tick[1], 'address': tick[2], 'occurence': tick[3]}
      r = requests.post(tick_service_url, data=json.dumps(data), headers=service_headers)
    except Exception as ex:
      ticks_queue.put(tick)
      display_show_network_error(tick_service_url,str(ex))
      time.sleep(2)
      continue

def mock_tick_producer():
  while True:
    ticks_queue.put((7,0,23,int(unix_time_millis(datetime.datetime.utcnow()))))
    time.sleep(1)

def json_display_data_updater():
  linemap = {0: (1,1), 1: (1,2), 2: (2,1), 3:(2,2)}
  while True:
    try:
      r = requests.get(display_service_url)
      for display_line in r.json:
        display.send_text(r.json[display_line][:PC4004B.DISPLAY_WIDTH], linemap[display_line])
    except Exception as ex:
        display_show_network_error(display_service_url, str(ex))
    time.sleep(10)    

def display_show_network_error(url, message):
  display.send_text("Network down? Webserver down?", 1, 1)
  display.send_text("request failed:", 2, 1)
  display.send_text(url[:PC4004B.DISPLAY_WIDTH], 1, 1)
  display.send_text(message[:PC4004B.DISPLAY_WIDTH])

threading.Thread(target = json_display_data_updater).start()
threading.Thread(target = json_tick_consumer).start()
threading.Thread(target = mock_tick_producer).start()

while 1:
  pass
