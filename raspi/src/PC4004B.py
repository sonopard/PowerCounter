import time
import RPi.GPIO as GPIO

# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# Zuordnung der GPIO Pins (ggf. anpassen)

class PC4004B:
  DISPLAY_RS = 7 # Register Select selects data (DISPLAY_CHR) or command (DISPLAY_CMD) mode
  DISPLAY_E  = 8 # chip enable 1
  DISPLAY_E2 = 11 # chip enable 2
  DISPLAY_DATA4 = 25
  DISPLAY_DATA5 = 24
  DISPLAY_DATA6 = 23
  DISPLAY_DATA7 = 18

  DISPLAY_WIDTH = 40   # Zeichen je Zeile
  DISPLAY_LINE_1 = 0x80   # Adresse der ersten Display Zeile
  DISPLAY_LINE_2 = 0xC0   # Adresse der zweiten Display Zeile
  DISPLAY_CHR = True
  DISPLAY_CMD = False
  E_PULSE = 0.00005 
  E_DELAY = 0.00005

  def __init__(self):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.DISPLAY_E, GPIO.OUT)
    GPIO.setup(self.DISPLAY_RS, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(self.DISPLAY_DATA7, GPIO.OUT)
    GPIO.setup(self.DISPLAY_E2, GPIO.OUT)
    self.display_init(self.DISPLAY_E)
    self.display_init(self.DISPLAY_E2)

  def send_text(self, text, line, chip):
    if line==2:
      _line = self.DISPLAY_LINE_2
    else:
      _line = self.DISPLAY_LINE_1
    if chip==2:
      _chip = self.DISPLAY_E2
    else:
      _chip = self.DISPLAY_E
    
    self.lcd_byte(_line, self.DISPLAY_CMD, _chip)
    self.lcd_string(text, _chip)
  
  def __del__(self):
    GPIO.cleanup()

  def display_init(self, enable):
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

