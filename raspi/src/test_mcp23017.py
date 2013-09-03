#!/usr/bin/python3
import MCP23017
import unittest
import logging

class ChipTest(unittest.TestCase):
  chip1 = MCP23017.MCP23017(0x20, {'A': 17})#, 'B': 0x00})
  chip2 = MCP23017.MCP23017(0x21, {'A': 27})#, 'B': 0x00})
  def test_enable_interrupts(self):
    self.chip1.activate_interrupts()
    self.chip1.activate_mirror()

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )
    unittest.main()
