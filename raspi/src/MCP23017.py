import time
import quick2wire.i2c as i2c
#from smbus import SMBus
import re
import logging

# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# for a pinout and pinmap see the accompanying documentation directory

# usage
# shield = IOShield()
# display.send_text("Up up in the butt", 1, 2) # line, chip - this will display the text in the 3rd line

log = logging.getLogger("IOShield")

class MCP23017:
  ADDRESS = 0x21
  BUS = None
  PORTS = {0:0x00, 1:0x10}

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


  def __init__(self, address, interrupt_a, interrupt_b):
    #self._lock = Lock()
    self.ADDRESS = address
    self.BUS = i2c.I2CMaster()
    #Set BANK = 1 for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero
    self.BUS.write_byte_data(self.ADDRESS,0x08, self.IOCON['BANK'])

  '''
  This method basically sets up the chip for further operations and 
  defines the electrical wiring as followes:
   - internal pullups are activated
   - connects to ground if power meter closes circuit
  '''
  def activate_interrupts(self):
      for port in self.PORTS:
        log.info("Configuring port "+str(port))
        self.BUS.transaction(
          #Set port to input pin
          i2c.writing_bytes(self.ADDRESS,port|self.REGISTER_IODIR,0xff),

          # WRITE Register Interrupt activate (GPINTEN)
          i2c.writing_bytes(self.ADDRESS,port|self.REGISTER_GPINTEN,0xff),
          ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
          #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
          # WRITE Register configure Interrupt mode to compare on Value(INTCON)
          i2c.writing_bytes(self.ADDRESS,port|self.REGISTER_INTCON, 0xff),
          # WRITE Register set compare Value 
          i2c.writing_bytes(self.ADDRESS,port|self.REGISTER_DEFCON, 0xff),
          # WRITE Register activate internal pullups
          i2c.writing_bytes(self.ADDRESS,port|self.REGISTER_GPPU, 0xff)
          # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
        )
  def activate_mirror(self):
    self.set_config(self.IOCON['MIRROR'])


  def set_config(self, config):
      log.info("Register Access IOCON, adding: "+config)
      iocon = self.BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before "+ iocon[0][0])
      self.BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON, iocon[0][0] | config))
      log.debug("IOCON after "+ (iocon[0][0] | config))

  def unset_config(self, config):
      log.info("Register Access IOCON, removing: "+config)
      iocon = self.BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before "+ iocon)
      self.BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON, iocon[0][0] & ~ config))
      log.debug("IOCON after "+ (iocon & ~ config))

  def add_interrupt_handler(self, callback_method):
    for  gpio_pin in self.INTERRUPTS:
      GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback = callback_method, bouncetime = 200)

  def read(self, register):

    byte = self.BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, register),
              i2c.reading(self.ADDRESS, 1))
    return byte[0][0]

'''
  def write(self, register):
    bus.transaction(i2c.writing_bytes(address, expander_registers["gpinten"], 0xFF, 0xFF))
  except IOError as ex:
    try:
      bus.close()
    except:
      pass
    display_show_failure(str(ex))
    while True:
      time.sleep(1)
''' 
