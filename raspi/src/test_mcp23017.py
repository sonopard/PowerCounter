#!/usr/bin/python3
import MCP23017
import unittest
import logging

log = logging.getLogger("Test.MCP23017")

class ChipTest(unittest.TestCase):
  chip1 = MCP23017.MCP23017(0x20, {'A': 17})#, 'B': 0x00})
  chip2 = MCP23017.MCP23017(0x21, {'A': 27})#, 'B': 0x00})
  def test_enable_interrupts(self):
    self.chip1.activate_interrupts()
    self.chip1.activate_mirror()

  def test_read_registers(self):
    for i in range(0,0x1A):
      byte = self.chip1.read(i)

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )
    log.setLevel(logging.DEBUG)
    unittest.main()
