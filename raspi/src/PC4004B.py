import time
import RPi.GPIO as GPIO

# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# for a pinout and pinmap see the accompanying documentation directory

# usage
# display = PC4004B()
# display.send_text("Up up in the butt", 1, 2) # line, chip - this will display the text in the 3rd line

class PC4004B:
  # lines
  DISPLAY_RS = 7 # register select selects data (DISPLAY_CHR) or command (DISPLAY_CMD) mode
  DISPLAY_E = {1:8, 2:11}
  DISPLAY_DATA4 = 25
  DISPLAY_DATA5 = 24
  DISPLAY_DATA6 = 23
  DISPLAY_DATA7 = 18
  
  # display constants
  DISPLAY_WIDTH = 40   # width in characters
  DISPLAY_CHR = True # RS high for characters
  DISPLAY_CMD = False # RS low for commands
  E_PULSE = 0.00005 # chip enable hold time
  E_DELAY = 0.00005 # chip enable delay applied before and after latching enable
  DISPLAY_LINE = {1:0x80,2:0xC0} # line 1 and line 2 data address

  def __init__(self):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.DISPLAY_E[1], GPIO.OUT)
    GPIO.setup(self.DISPLAY_RS, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA7, GPIO.OUT)
    GPIO.setup(self.DISPLAY_E[2], GPIO.OUT)
    self.display_init(self.DISPLAY_E[1])
    self.display_init(self.DISPLAY_E[2])
  
  '''
  This method displays a text of max 40 chars length
  '''
  def send_text(self, text, line):
    if(len(text) > self.DISPLAY_WIDTH):
      print("Error, text larger 40 chars")
      return

    # Calculate Chip parameters
    line = self.DISPLAY_LINE[line%2+1]
    chip = self.DISPLAY_E[1 if line<=2 else 2]

    self.lcd_byte(line, self.DISPLAY_CMD, chip) # select the output address
    self.lcd_string(text, chip)
  
  def __del__(self):
    GPIO.cleanup()

  def display_init(self, enable):
    # TODO figure out what this actually does
    self.lcd_byte(0b00110011,self.DISPLAY_CMD,enable) # cursor return wtf
    self.lcd_byte(0b00110010,self.DISPLAY_CMD,enable) # wtf
    self.lcd_byte(0b00101000,self.DISPLAY_CMD,enable) # ddram ad set: set ddram ad to 0b1000
    self.lcd_byte(0b00001100,self.DISPLAY_CMD,enable) # self.DISPLAY switch: on, cursor off, blink off
    self.lcd_byte(0b00000110,self.DISPLAY_CMD,enable) # entry mode set: increment (left-to-right), shift
    self.lcd_byte(0b00000001,self.DISPLAY_CMD,enable) # clear self.DISPLAY: clears entire self.DISPLAY and sets address counter to 0

  def lcd_string(self, message, enable):
    message = message.ljust(self.DISPLAY_WIDTH," ")  
    for i in range(self.DISPLAY_WIDTH):
      self.lcd_byte(ord(message[i]),self.DISPLAY_CHR,enable)

  def lcd_byte(self, bits, mode, enable):
    # in 4-bit mode, output high nibble first, latch, then output low nibble and latch again.
    GPIO.output(self.DISPLAY_RS, mode)
    GPIO.output(self.DISPLAY_DATA4, False)
    GPIO.output(self.DISPLAY_DATA5, False)
    GPIO.output(self.DISPLAY_DATA6, False)
    GPIO.output(self.DISPLAY_DATA7, False)
    if bits&0x10==0x10:
      GPIO.output(self.DISPLAY_DATA4, True)
    if bits&0x20==0x20:
      GPIO.output(self.DISPLAY_DATA5, True)
    if bits&0x40==0x40:
      GPIO.output(self.DISPLAY_DATA6, True)
    if bits&0x80==0x80:
      GPIO.output(self.DISPLAY_DATA7, True)
    time.sleep(self.E_DELAY)    
    GPIO.output(enable, True)  
    time.sleep(self.E_PULSE)
    GPIO.output(enable, False)  
    time.sleep(self.E_DELAY)      
    GPIO.output(self.DISPLAY_DATA4, False)
    GPIO.output(self.DISPLAY_DATA5, False)
    GPIO.output(self.DISPLAY_DATA6, False)
    GPIO.output(self.DISPLAY_DATA7, False)
    if bits&0x01==0x01:
      GPIO.output(self.DISPLAY_DATA4, True)
    if bits&0x02==0x02:
      GPIO.output(self.DISPLAY_DATA5, True)
    if bits&0x04==0x04:
      GPIO.output(self.DISPLAY_DATA6, True)
    if bits&0x08==0x08:
      GPIO.output(self.DISPLAY_DATA7, True)
    time.sleep(self.E_DELAY)    
    GPIO.output(enable, True)  
    time.sleep(self.E_PULSE)
    GPIO.output(enable, False)  
    time.sleep(self.E_DELAY)   

