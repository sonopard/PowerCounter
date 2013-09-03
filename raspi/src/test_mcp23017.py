#!/usr/bin/python3
import MCP23017
import unittest

class ChipTest(unittest.TestCase):
  chip1 = MCP23017.MCP23017(0x20, {'A': 0x14, 'B': 0x16})
  chip2 = MCP23017.MCP23017(0x20, {'A': 0x15, 'B': 0x17})
  def test_enable_interrupts(self):
    chip1.activate_interrupts()
    chip2.activate_interrupts()
    chip1.activate_mirror()
    chip2.activate_mirror()

if __name__ == '__main__':
    unittest.main()
