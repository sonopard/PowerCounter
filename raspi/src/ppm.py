import requests
import json
from queue import Queue, Empty
import time
import datetime
import threading
#from SMBus import smbus

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

serviceurl = "http://192.168.2.109:8080/powercounter/tick"
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# pin, bank, chip
ticksqueue = Queue()

def jsonconsumer():
  while True:
    try:
      tick = ticksqueue.get(block=False)
    except Empty:
      time.sleep(1)
      continue
    try:
      data = {'pin': tick[0], 'bank': tick[1], 'address': tick[2], 'occurence': tick[3]}
      r = requests.post(serviceurl, data=json.dumps(data), headers=headers)
      print(r)
      print(r.text)
    except:
      ticksqueue.put(tick)
      print("retry")
      time.sleep(2)
      continue

def gpioproducer():
  while True:
    ticksqueue.put((7,0,23,int(unix_time_millis(datetime.datetime.utcnow()))))
    time.sleep(5)

threading.Thread(target = jsonconsumer).start()
threading.Thread(target = gpioproducer).start()

while 1:
  pass