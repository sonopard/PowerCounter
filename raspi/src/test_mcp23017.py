#!/usr/bin/python3
import MCP23017
import unittest

class ChipTest(unittest.TestCase):
  chip1 = MCP23017.MCP23017(0x20)
  chip2 = MCP23017.MCP23017(0x20)
  def test_enable_interrupts(self):
    chip1.activate_interrupts()
    chip2.activate_interrupts()
    chip1.activate_mirror()
    chip2.activate_mirror()

if __name__ == '__main__':
    unittest.main()
