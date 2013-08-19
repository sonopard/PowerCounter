import requests
import json
from queue import Queue, Empty
import time

#from SMBus import smbus

serviceurl = "http://192.168.2.109:8080/powercounter/tick"
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# pin, bank, chip
ticksqueue = Queue()
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))
ticksqueue.put((7,0,23))

while True:
  try:
    tick = ticksqueue.get(block=False)
    print(tick)
  except Empty:
    print("empty")
    time.sleep(1)
    continue
  try:
    data = {'pin': tick[0], 'bank': tick[1], 'address': tick[2]}
    r = requests.post(serviceurl, data=json.dumps(data), headers=headers)
    print(r.text)
  except:
    ticksqueue.put(tick)
    continue
