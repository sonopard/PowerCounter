#!/usr/bin/python3
import IOShield
import unittest

class TextLength(unittest.TestCase):
  shield = IOShield.IOShield(0x20, 0x21)
  def test_init_interrupts(self):
    self.shield.activate_interrupts()

if __name__ == '__main__':
    unittest.main()
