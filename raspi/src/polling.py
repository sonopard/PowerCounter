#!/usr/bin/python3
from MCP23017 import MCP23017
import logging
logging.basicConfig()
logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )

chips = [MCP23017(0x20, 1),
          MCP23017(0x21, 1)]

while 1:
  for chip in chips:
    for i in range(0x1B):
      byte = chip.read(i)
