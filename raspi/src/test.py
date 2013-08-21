#!/usr/bin/python3
import PC4004B
import unittest

class TextLength(unittest.TestCase):
  display = PC4004B.PC4004B()
  def test_too_long(self):
    # prevent errors on texts larger 40 chars
     self.assertRaises(ValueError, self.display.send_text, "1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_1_2_3_4_5_6_7_8_9_+", 1)

if __name__ == '__main__':
    unittest.main()
