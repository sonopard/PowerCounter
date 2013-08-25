import time
#import RPi.GPIO as GPIO
import GPIOdummy as GPIO
from smbus import SMBus

# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# for a pinout and pinmap see the accompanying documentation directory

# usage
# shield = IOShield()
# display.send_text("Up up in the butt", 1, 2) # line, chip - this will display the text in the 3rd line

class IOShield:
  ADDRESS = {}
  BANK = {0:0x00, 1:0x10}
  INTERRUPT_HANDLER = {}

  # mapping of pins inside icocon register
  IOCON = {BANK:0x80, MIRROR: 0x40}


  for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
      (name, value) = (m.group(1), m.group(2))
      if name == "Revision":
        if value [-4:] in ('0002', '0003'):
          i2c_bus = 0
        else:
          i2c_bus = 1
          break
  BUS = SMBus(i2c_bus)

  def __init__(self, address_chip1, address_chip2):
    self._lock = Lock()
    self.ADDRESS[1] = address_chip1
    self.ADDRESS[2] = address_chip2
	

    self.init_shield(self.ADDRESS[1])
    self.init_shield(self.ADDRESS[2])

  def init_shield(self, chip):
    #Set BANK = 1 for easier Addressing of banks (IOCON register)
    self.BUS.write_byte_data(chip,bank|0x05, self.IOCON.BANK)
    #Set both banks to output pin
    for bank in self.BANK:
      self.BUS.write_byte_data(chip,bank|0x00,0xff)


  def activate_interrupts(self):
    for chip in self.ADDRESS:
      for bank in self.BANK:
        # WRITE Register Interrupt-on-change activate (GPINTEN)
        self.BUS.write_byte_data(chip,bank|0x02,0xff)
        # WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
        self.BUS.write_byte_data(chip,bank|0x04, 0x00)
        # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
        self.BUS.write_byte_data(chip,bank|0x05, self.IOCON.MIRROR)

  def add_interrupt_handler(self, callback_method, gpio_pin):
    GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback = callback_method, bouncetime = 200)

  def read(self):
    byte = {}
    i=0
    for chip in self.ADDRESS:
      for bank in self.BANK:
        byte[i] = bus.read_byte_data(chip,bank|0x09)
        i+=1
    return byte
