import digitalio
import interfaces
import time
from board import *
import constants

class LCD():
  """Sunfire LCD 2x16 Char Display Module"""
  def __init__(self):
    # Set up pins
    self.pin_RS  = digitalio.DigitalInOut(D27) # RS
    self.pin_E   = digitalio.DigitalInOut(D22) # E
    self.pin_D4  = digitalio.DigitalInOut(D18) # DB4
    self.pin_D5  = digitalio.DigitalInOut(D23) # DB5
    self.pin_D6  = digitalio.DigitalInOut(D24) # DB6
    self.pin_D7  = digitalio.DigitalInOut(D25) # DB7
    self.pin_ON = digitalio.DigitalInOut(D15) # Backlight enable

    self.pin_E.direction = digitalio.Direction.OUTPUT
    self.pin_RS.direction = digitalio.Direction.OUTPUT
    self.pin_D4.direction = digitalio.Direction.OUTPUT
    self.pin_D5.direction = digitalio.Direction.OUTPUT
    self.pin_D6.direction = digitalio.Direction.OUTPUT
    self.pin_D7.direction = digitalio.Direction.OUTPUT
    self.pin_ON.direction = digitalio.Direction.OUTPUT
    
    # Initialize line registers with splash screen
    self.reg_line_1 = "Open".center(constants.LCD_WIDTH," ")
    self.reg_line_2 = "Acidification".center(constants.LCD_WIDTH," ")
    self.reg_line_3 = "Project".center(constants.LCD_WIDTH," ")
    self.reg_line_4 = "Alkalinity Titrator".center(constants.LCD_WIDTH," ")
    
     # Initialise display
    self.__lcd_byte(0x33,constants.LCD_CMD) # 110011 Initialise
    self.__lcd_byte(0x32,constants.LCD_CMD) # 110010 Initialise
    self.__lcd_byte(0x06,constants.LCD_CMD) # 000110 Cursor move direction
    self.__lcd_byte(0x0C,constants.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    self.__lcd_byte(0x28,constants.LCD_CMD) # 101000 Data length, number of lines, font size
    self.__lcd_byte(0x01,constants.LCD_CMD) # 000001 Clear display
    time.sleep(constants.E_DELAY)
    
    # Toggle backlight on-off-on
    self.lcd_backlight(True)
    time.sleep(0.5)
    self.lcd_backlight(False)
    time.sleep(0.5)
    self.lcd_backlight(True)
    time.sleep(0.5)
    
    self.out_line(self.reg_line_1, constants.LCD_LINE_1,constants.LCD_CENT_JUST)
    self.out_line(self.reg_line_2, constants.LCD_LINE_2,constants.LCD_CENT_JUST)
    self.out_line(self.reg_line_3, constants.LCD_LINE_3,constants.LCD_CENT_JUST)
    self.out_line(self.reg_line_4, constants.LCD_LINE_4,constants.LCD_CENT_JUST)
    
    time.sleep(1)

  def __lcd_byte(self,bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
   
    self.pin_RS.value = mode # RS
   
    # High bits
    self.pin_D4.value = False
    self.pin_D5.value = False
    self.pin_D6.value = False
    self.pin_D7.value = False
    if bits&0x10==0x10:
      self.pin_D4.value = True
    if bits&0x20==0x20:
      self.pin_D5.value = True
    if bits&0x40==0x40:
      self.pin_D6.value = True
    if bits&0x80==0x80:
      self.pin_D7.value = True
   
    # Toggle 'Enable' pin
    self.__lcd_toggle_enable()
   
    # Low bits
    self.pin_D4.value = False
    self.pin_D5.value = False
    self.pin_D6.value = False
    self.pin_D7.value = False
    if bits&0x01==0x01:
      self.pin_D4.value = True
    if bits&0x02==0x02:
      self.pin_D5.value = True
    if bits&0x04==0x04:
      self.pin_D6.value = True
    if bits&0x08==0x08:
      self.pin_D7.value = True
   
    # Toggle 'Enable' pin
    self.__lcd_toggle_enable()
 
  def __lcd_toggle_enable(self):
    # Toggle enable
    time.sleep(constants.E_DELAY)
    self.pin_E.value = True
    time.sleep(constants.E_PULSE)
    self.pin_E.value = False
    time.sleep(constants.E_DELAY)

  def out(self,message, style=1):
    """
    Sends a string out to the bottom line of the display,
    shifting the previous lines up once
    """
    if style==1:
      message = message.ljust(constants.LCD_WIDTH," ")
    elif style==2:
      message = message.center(constants.LCD_WIDTH," ")
    elif style==3:
      message = message.rjust(constants.LCD_WIDTH," ")

    # Increment lines upward
    self.reg_line_1 = self.reg_line_2
    self.reg_line_2 = self.reg_line_3
    self.reg_line_3 = self.reg_line_4
    self.reg_line_4 = message

    self.__write_message(self.reg_line_1,constants.LCD_LINE_1)
    #time.sleep(0.5)
    self.__write_message(self.reg_line_2,constants.LCD_LINE_2)
    #time.sleep(0.5)
    self.__write_message(self.reg_line_3,constants.LCD_LINE_3)
    #time.sleep(0.5)
    self.__write_message(self.reg_line_4,constants.LCD_LINE_4)
    #time.sleep(0.5)

  def out_line(self,message,line,style=1):
    """
     Send string to display. 
     Lines: LCD_LINE_X (1,2,3,4) 
     styles (justification): X (1=left, 2=center, 3=right) 
    """
   
    if style==1:
      message = message.ljust(constants.LCD_WIDTH," ")
    elif style==2:
      message = message.center(constants.LCD_WIDTH," ")
    elif style==3:
      message = message.rjust(constants.LCD_WIDTH," ")
   
    if line==constants.LCD_LINE_1:
      self.reg_line_1 = message
    elif line == constants.LCD_LINE_2:
      self.reg_line_2 = message
    elif line == constants.LCD_LINE_3:
      self.reg_line_3 = message
    elif line == constants.LCD_LINE_4:
      self.reg_line_4 = message

    self.__write_message(message,line)
 
  def __write_message(self,message,line):
    #print(message, line)
    self.__lcd_byte(line, constants.LCD_CMD)
    
    for i in range(constants.LCD_WIDTH):
      self.__lcd_byte(ord(message[i]),constants.LCD_CHR)

  def lcd_backlight(self,flag):
    # Toggle backlight on-off-on
    self.pin_ON.value = flag

  def clear_screen(self):
    # Clear the screen
    blank = ""
    blank = blank.ljust(constants.LCD_WIDTH," ")
    
    self.reg_line_1 = blank
    self.reg_line_2 = blank
    self.reg_line_3 = blank
    self.reg_line_4 = blank
    
    self.__write_message(blank,constants.LCD_LINE_1)
    self.__write_message(blank,constants.LCD_LINE_2)
    self.__write_message(blank,constants.LCD_LINE_3)
    self.__write_message(blank,constants.LCD_LINE_4)
