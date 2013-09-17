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

# Register Mapping for Bank=1 and Bank=0 mode
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

  state = [0b00000000, 0b00000000]
  external_callback = None

  def __init__(self, address):
    self.lock = Lock()
    self.address = address
    log.debug("Initialize port 0x{0:x}".format(address))
    '''
    This method basically sets up the chip for further operations and 
    defines the electrical wiring as followes:
     - internal pullups are activated
     - connects to ground if power meter closes circuit
    '''
    BUS.transaction(
      #Set port to input pin
      i2c.writing_bytes(address,REGISTER_IODIR,0xff, 0xff),

      ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
      #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
      # WRITE Register configure Interrupt mode to compare on Value(INTCON)
      i2c.writing_bytes(address,REGISTER_INTCON, 0xff, 0xff),
      # WRITE Register set compare Value 
      i2c.writing_bytes(address,REGISTER_DEFVAL, 0xff, 0xff),
      # reflect opposite polarity of pins in GPIO register
      i2c.writing_bytes(address,REGISTER_IPOL, 0x00, 0x00),
      # WRITE Register activate internal pullups
      i2c.writing_bytes(address,REGISTER_GPPU, 0xff, 0xff),
      # WRITE Register Interruptactivate (GPINTEN)
      i2c.writing_bytes(address,REGISTER_GPINTEN,0xff, 0xff),
    )


  def set_callback(self, callback):
    log.debug("Set callback "+str(callback))
    state = BUS.transaction(
      #Set port to input pin
      i2c.writing_bytes(self.address,REGISTER_GPIO),
      i2c.reading(self.address, 2))
    self.state[0] = state[0][0] ^ 0b11111111
    self.state[1] = state[0][1] ^ 0b11111111
    log.debug("Re-Setting initial state of port is now 0b{0:b}".format(self.state))
    self.external_callback = callback

  def callback(self, channel):
    log.info("Interrupt detected on address 0x{0:x} with prefix channel {1}".format(self.address, channel))
    self.lock.acquire()
    log.debug("Lock aquired!")
    log.debug("Before State is 0b{0:b}".format(self.state))
    erg = BUS.transaction(
      #READ INTF TO FIND OUT INITIATING PIN
      i2c.writing_bytes(self.address,REGISTER_INTF),
      i2c.reading(self.address,2),
      #READ GPIO TO GET CURRENTLY ACTIVATED PINS | RESETS THE INTERRUPT
      i2c.writing_bytes(self.address,REGISTER_GPIO),
      i2c.reading(self.address,2),
    )

    intf[0] = erg[0][0]
    intf[1] = erg[0][1]
    log.debug("INTF was 0b{0:b}".format(intf))
    gpio[0] = (erg[1][0] ^ 0b11111111)
    gpio[1] = (erg[1][1] ^ 0b11111111)
    log.debug("GPIO was 0b{0:b}".format(gpio))
    current[0] = intf[0] | gpio[0]
    current[1] = intf[1] | gpio[1]
        
    #calculate only changes
    changes[0] = (self.state[0] ^ 0b11111111) & current[0]
    changes[1] = (self.state[1] ^ 0b11111111) & current[1]

    #set new state
    self.state[1] = gpio[1]
    log.debug("After State is 0b{0:b}".format(self.state))

    self.lock.release()
    log.debug("Lock released!")

    #call callback after lock release
    log.info("Sending changes 0b{0:b} to callback method".format(changes))
    self.external_callback(changes[0], self.address)

class MCP23017:
  ADDRESS = 0x21
  PORT = None
  INTERRUPT = None

  def __init__(self, address, bank):
    log.info("Initialize MCP23017 on 0x{0:x}".format(address))
    #self._lock = Lock()
    self.ADDRESS = address


    #Set bank state for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero
    if bank == 1: #assume has been bank=0 before
      BUS.transaction( 
        i2c.writing_bytes(self.ADDRESS,0x14, IOCON['BANK']),
        i2c.writing_bytes(self.ADDRESS,0x15, IOCON['BANK']))
      REGISTER = MAPPING['BANK']
    elif bank == 0:
      BUS.transaction( 
        i2c.writing_bytes(self.ADDRESS,0x14, 0 ),
        i2c.writing_bytes(self.ADDRESS,0x15, 0 ))
      REGISTER = MAPPING['NOBANK']

  def init_interrupts(self, interrupt):
    self.INTERRUPT = interrupt
    GPIO.setup(self.INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  #initialize ports and set them for interrupts
  def initialize_ports(self):
    #!important! Initialize Ports after bank has been set to 1
    self.PORT = PortManager(self.ADDRESS)


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
    log.info("Add callback to GPIO {0} on address 0x{1:x}".format(self.INTERRUPT, self.ADDRESS))
    port_manager = self.PORT
    port_manager.set_callback(callback_method)
    GPIO.add_event_detect(self.INTERRUPT, GPIO.RISING, callback = port_manager.callback)


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
