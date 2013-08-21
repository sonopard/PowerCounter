#!/usr/bin/python3
# Implements a basic test of interfaces

# Setup
import requests
import json
from queue import Queue, Empty
import time
import datetime
import threading
import PC4004B

display = PC4004B.PC4004B()

# TEST prevent errors on texts larger 40 chars
display.send_text("1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_+", 1)
