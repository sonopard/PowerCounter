#!/usr/bin/python3
import logging
import MCP23017

logging.basicConfig()
logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )

chip1 = MCP23017.MCP23017(0x20, {'A': 17})#, 'B': 0x00})
chip2 = MCP23017.MCP23017(0x21, {'A': 27})#, 'B': 0x00})

#Simply write a small callback that takes a byte reflecting the ticks on pins
def myCallback(ticklist): 
  log.info(ticklist)

self.chip1.set_interrupt_handler(myCallback)
