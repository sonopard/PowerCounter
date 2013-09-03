import time
from dummy_smbus import SMBus
#from smbus import SMBus
import re

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
  BUS = None
  BANK = {0:0x00, 1:0x10}

  INTERRUPT_HANDLER = {}

  # Register Mapping for Bank=1 mode
  REGISTER_IODIR = 0X00
  REGISTER_IPOL = 0X01
  REGISTER_GPINTEN = 0X02
  REGISTER_DEFVAL = 0X03
  REGISTER_INTCON = 0X04
  REGISTER_IOCON = 0X05
  REGISTER_GPPU = 0X06
  REGISTER_INTF = 0X07
  REGISTER_INTCAP = 0X08
  REGISTER_GPIO = 0X09
  REGISTER_OLAT = 0X0A

  # mapping of pins inside icocon register
  IOCON = {'BANK':0b10000000, 'MIRROR': 0b01000000, 'DISSLW': 0b00010000, 'HAEN': 0b00001000, 'ODR': 0b00000100, 'INTPOL': 0b00000010}


  def __init__(self, address_chip1, address_chip2):
    #self._lock = Lock()

    '''
    guess the correct configuration for revision of raspberry pi
    '''
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
        else:
          i2c_bus = 0 #fallback
 
    self.BUS = SMBus(i2c_bus)
    self.ADDRESS[1] = address_chip1
    self.ADDRESS[2] = address_chip2

    self.init_shield(self.ADDRESS[1])
    self.init_shield(self.ADDRESS[2])

  def init_shield(self, chip):
    #Set BANK = 1 for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero
    self.BUS.write_byte_data(chip,0x08, self.IOCON['BANK'])

  '''
  This method basically sets up the chip for further operations and 
  defines the electrical wiring as followes:
   - internal pullups are activated
   - connects to ground if power meter closes circuit
  '''
  def activate_interrupts(self):
    for chip in self.ADDRESS:
      for bank in self.BANK:
        #Set both banks to input pin
        self.BUS.write_byte_data(chip,bank|self.REGISTER_IODIR,0xff)

        # WRITE Register Interrupt activate (GPINTEN)
        self.BUS.write_byte_data(chip,bank|self.REGISTER_GPINTEN,0xff)
        ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
        #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
        # WRITE Register configure Interrupt mode to compare on Value(INTCON)
        self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0xff)
        # WRITE Register set compare Value 
        self.BUS.write_byte_data(chip,bank|self.REGISTER_DEFCON, 0xff)
        # WRITE Register activate internal pullups
        self.BUS.write_byte_data(chip,bank|self.REGISTER_GPPU, 0xff)
        # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
        self.set_config(self.IOCON['MIRROR'])


  def set_config(self, config):
    for chip in self.ADDRESS:
      iocon = self.BUS.read_byte_data(chip,self.REGISTER_IOCON)
      self.BUS.write_byte_data(chip,self.REGISTER_IOCON, iocon | config)

  def unset_config(self, config):
    for chip in self.ADDRESS:
      iocon = self.BUS.read_byte_data(chip,self.REGISTER_IOCON)
      self.BUS.write_byte_data(chip,self.REGISTER_IOCON, iocon & ~ config)

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
