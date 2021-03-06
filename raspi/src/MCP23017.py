import time
import quick2wire.i2c as i2c
#from smbus import SMBus
import re
import logging
from threading import Lock
from RPi import GPIO


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
MAPPING = { 
  'NOBANK' : {
    'IODIR': 0X00,
    'IPOL': 0X02,
    'GPINTEN': 0X04,
    'DEFVAL': 0X06,
    'INTCON': 0X08,
    'IOCON': 0X0A,
    'GPPU': 0X0C,
    'INTF': 0X0E,
    'INTCAP': 0X10,
    'GPIO': 0X12,
    'OLAT': 0X14
  },
 'BANK': {
    'IODIR': 0X00,
    'IPOL': 0X01,
    'GPINTEN': 0X02,
    'DEFVAL': 0X03,
    'INTCON': 0X04,
   'IOCON': 0X05,
    'GPPU': 0X06,
    'INTF': 0X07,
    'INTCAP': 0X08,
    'GPIO': 0X09,
    'OLAT': 0X0A
  }
}
REGISTER = None

# mapping of pins inside icocon register
IOCON = {'BANK':0b10000000, 'MIRROR': 0b01000000, 'DISSLW': 0b00010000, 'HAEN': 0b00001000, 'ODR': 0b00000100, 'INTPOL': 0b00000010}


class PortManager:

  state = 0b00000000
  external_callback = None

  def __init__(self, address, prefix, interrupt_pin):
    self.lock = Lock()
    self.address = address
    self.prefix = prefix
    self.interrupt_pin = interrupt_pin
    log.debug("Initialize port 0x{0:x}".format(prefix))
    '''
    This method basically sets up the chip for further operations and 
    defines the electrical wiring as followes:
     - internal pullups are activated
     - connects to ground if power meter closes circuit
    '''
    BUS.transaction(
      #Set port to input pin
      i2c.writing_bytes(address,prefix|REGISTER['IODIR'],0xff),

      ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
      #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
      # WRITE Register configure Interrupt mode to compare on Value(INTCON)
      i2c.writing_bytes(address,prefix|REGISTER['INTCON'], 0xff),
      # WRITE Register set compare Value 
      i2c.writing_bytes(address,prefix|REGISTER['DEFVAL'], 0xff),
      # reflect opposite polarity of pins in GPIO register
      i2c.writing_bytes(address,prefix|REGISTER['IPOL'], 0x00),
      # WRITE Register activate internal pullups
      i2c.writing_bytes(address,prefix|REGISTER['GPPU'], 0xff),
      # WRITE Register Interrupt activate (GPINTEN)
      i2c.writing_bytes(address,prefix|REGISTER['GPINTEN'],0xff),
    )
    log.debug("Initialize Interrupt "+name+" for GPIO pin "+ str(interrupt_pin))
    GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


  def set_callback(self, callback):
    log.debug("Set callback "+str(callback))
    self.state = BUS.transaction(
      #Set port to input pin
      i2c.writing_bytes(self.address,self.prefix|REGISTER['GPIO']),
      i2c.reading(self.address, 1))[0][0] ^ 0b11111111
    log.debug("Re-Setting initial state of port is now 0b{0:b}".format(self.state))
    self.external_callback = callback
    if self.external_callback is None:
      log.debug("first call of set_callback: enabling RPi interrupt")
      GPIO.add_event_detect(self.interrupt_pin, GPIO.RISING, callback = self.callback)

  def callback(self, channel):
    log.info("Interrupt detected on address 0x{0:x} with prefix 0x{1:x}; channel {2}".format(self.address, self.prefix, channel))
    self.lock.acquire()
    log.debug("Lock aquired!")
    log.debug("Before State is 0b{0:b}".format(self.state))
    erg = BUS.transaction(
      #READ INTF TO FIND OUT INITIATING PIN
      i2c.writing_bytes(self.address,self.prefix|REGISTER['INTF']),
      i2c.reading(self.address,1),
      #READ GPIO TO GET CURRENTLY ACTIVATED PINS | RESETS THE INTERRUPT
      i2c.writing_bytes(self.address,self.prefix|REGISTER['GPIO']),
      i2c.reading(self.address,1),
    )

    intf = erg[0][0]
    log.debug("INTF was 0b{0:b}".format(intf))
    gpio = (erg[1][0] ^ 0b11111111)
    log.debug("GPIO was 0b{0:b}".format(gpio))
    current = intf | gpio
    
        
    #calculate only changes
    changes = (self.state ^ 0b11111111) & current

    #set new state
    self.state = gpio
    log.debug("After State is 0b{0:b}".format(self.state))

    self.lock.release()
    log.debug("Lock released!")

    #call callback after lock release
    log.info("Sending changes 0b{0:b} to callback method".format(changes))
    self.external_callback(changes, self.prefix, self.address)

class MCP23017:
  ADDRESS = 0x21
  PORTS = {}
  INTERRUPTS = None

  def __init__(self, address, bank):
    log.info("Initialize MCP23017 on 0x{0:x}".format(address))
    #self._lock = Lock()
    self.ADDRESS = address

    #Set bank state for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero - some magic to write bit on both settings
    if bank == 1: #assume has been bank=0 before
      BUS.transaction( 
        i2c.writing_bytes(self.ADDRESS,0x14, IOCON['BANK']),
        i2c.writing_bytes(self.ADDRESS,0x0A, IOCON['BANK']))
      REGISTER = MAPPING['BANK']
    elif bank == 0:
      BUS.transaction( 
        i2c.writing_bytes(self.ADDRESS,0x14, 0 ),
        i2c.writing_bytes(self.ADDRESS,0x0A, 0 ))
      REGISTER = MAPPING['NOBANK']

  #initialize ports and set them for interrupts
  def initialize_ports(self, interrupts):

    #!important! Initialize Ports after bank has been set to 1
    self.PORTS = { 'A': PortManager(self.ADDRESS, 0x00, interrupts['A']), 
                   'B': PortManager(self.ADDRESS, 0x10, interrupts['B'])}


  def activate_mirror(self):
    # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
    self.set_config(IOCON['MIRROR'])


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
              i2c.writing_bytes(self.ADDRESS, REGISTER['IOCON']),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before 0b{0:b}".format(iocon[0][0]))
      BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, REGISTER['IOCON'], iocon[0][0] & ~ config))
      log.debug("IOCON after 0b{0:b}".format(iocon[0][0] & ~ config))

  def set_interrupt_handler(self, callback_method):
    for name, portmanager in self.PORTS.items():
      log.info("Add callback to GPIO {0} (Interrupt {1}) on address 0x{2:x}".format(gpio_pin,name, self.ADDRESS))
      port_manager = self.PORTS[name]
      port_manager.set_callback(callback_method)



  def read(self, register):
    byte = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, register),
              i2c.reading(self.ADDRESS, 1))
    log.debug("Reading from address 0x{0:x} register 0x{1:x} value 0b{2:b}".format(self.ADDRESS, register, byte[0][0]))
    return byte[0][0]
  
  def write(self, register, value):
    log.debug("Writing to address 0x{0:x} register 0x{1:x} value 0b{2:b}".format(self.ADDRESS, register, byte[0][0]))
    BUS.transaction(
      i2c.writing_bytes(self.ADDRESS, register ,value),
    )
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
