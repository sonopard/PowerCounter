import time
import quick2wire.i2c as i2c
#from smbus import SMBus
import re
import logging
from threading import Lock
import RPi.GPIO as GPIO


# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# for a pinout and pinmap see the accompanying documentation directory

# usage
# shield = IOShield()
# display.send_text("Up up in the butt", 1, 2) # line, chip - this will display the text in the 3rd line

log = logging.getLogger("MCP23017")
BUS = i2c.I2CMaster()

GPIO.setmode(GPIO.BCM)

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


class PortManager:

  state = [0,0,0,0,0,0,0,0]
  callback = None

  def __init__(self, address, prefix):
    self.lock = Lock()
    self.address = address
    self.prefix = prefix
    log.debug("Configuring port 0x{0:x}".format(prefix))
    '''
    This method basically sets up the chip for further operations and 
    defines the electrical wiring as followes:
     - internal pullups are activated
     - connects to ground if power meter closes circuit
    '''
    BUS.transaction(
      #Set port to input pin
      i2c.writing_bytes(address,prefix|REGISTER_IODIR,0xff),

      ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
      #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
      # WRITE Register configure Interrupt mode to compare on Value(INTCON)
      i2c.writing_bytes(address,prefix|REGISTER_INTCON, 0xff),
      # WRITE Register set compare Value 
      i2c.writing_bytes(address,prefix|REGISTER_DEFVAL, 0xff),
      # WRITE Register activate internal pullups
      i2c.writing_bytes(address,prefix|REGISTER_GPPU, 0xff),
      # WRITE Register Interrupt activate (GPINTEN)
      i2c.writing_bytes(address,prefix|REGISTER_GPINTEN,0xff),
    )

  def set_callback(self, callback):
    self.callback = callback

  def callback(self):
    log.info("Interrupt detected on address 0x{0:x} with prefix 0x{1:x}".format(self.address, self.prefix))
    self.lock.acquire()
    log.debug("Lock aquired!")
    log.debug("Before State is 0b{0:b}".format(state))
    erg = BUS.transaction(
      #READ INTF TO FIND OUT INITIATING PIN
      i2c.writing_bytes(self.address,self.prefix|REGISTER_INTF),
      i2c.reading(self.address,1),
      #READ GPIO TO GET CURRENTLY ACTIVATED PINS | RESETS THE INTERRUPT
      i2c.writing_bytes(self.address,self.prefix|REGISTER_GPIO),
      i2c.reading(self.address,1),
    )

    intf = erg[0][0]
    log.debug("INTF was 0b{0:b}".format(intf))
    gpio = erg[0][1]
    log.debug("GPIO was 0b{0:b}".format(gpio))
    current = intf | gpio
    
        
    #calculate only changes
    changes = ~state & current
    state = current
    log.debug("After State is 0b{0:b}".format(state))

    self.lock.release()
    log.debug("Lock released!")

    #call callback after lock release
    log.info("Sending changes 0b{0:b} to callback method".format(state))
    self.callback(changes)

class MCP23017:
  ADDRESS = 0x21
  PORTS = {}
  INTERRUPTS = None

  # mapping of pins inside icocon register
  IOCON = {'BANK':0b10000000, 'MIRROR': 0b01000000, 'DISSLW': 0b00010000, 'HAEN': 0b00001000, 'ODR': 0b00000100, 'INTPOL': 0b00000010}


  def __init__(self, address, interrupts):
    log.debug("Initialize MCP23017 on 0x{0:x}".format(address))
    #self._lock = Lock()
    self.ADDRESS = address
    self.INTERRUPTS = interrupts
    for name, gpio_pin in self.INTERRUPTS.items():
      log.debug("Initialize Interrupt "+name)
      GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #Set BANK = 1 for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero
    BUS.transaction( 
      i2c.writing_bytes(self.ADDRESS,0x0A, self.IOCON['BANK']))

    #!important! Initialize Ports after bank has been set to 1
    self.PORTS = { 'A': PortManager(address, 0x00), 
                   'B': PortManager(address, 0x10)}


  def activate_mirror(self):
    # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
    self.set_config(self.IOCON['MIRROR'])


  def set_config(self, config):
      log.info("Register Access IOCON, adding: 0b{0:b}".format(config))
      iocon = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before 0b{0:b}".format(iocon[0][0]))
      BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, REGISTER_IOCON, iocon[0][0] | config))
      log.debug("IOCON after 0b{0:b}".format(iocon[0][0] | config))

  def unset_config(self, config):
      log.info("Register Access IOCON, removing: 0b{0:b}".format(config))
      iocon = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before 0b{0:b}".format(iocon[0][0]))
      BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, REGISTER_IOCON, iocon[0][0] & ~ config))
      log.debug("IOCON after 0b{0:b}".format(iocon[0][0] & ~ config))

  def set_interrupt_handler(self, callback_method):
    for name, gpio_pin in self.INTERRUPTS.items():
      port_manager = self.PORTS[name]
      port_manager.set_callback(callback_method)
      GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback = port_manager.callback)


  def read(self, register):
    byte = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, register),
              i2c.reading(self.ADDRESS, 1))
    log.debug("Reading from address 0x{0:x} register 0x{1:x} value 0b{2:b}".format(self.ADDRESS, register, byte[0][0]))
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
