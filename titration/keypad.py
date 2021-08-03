#import
import digitalio
import interfaces
from board import *
import constants

class Keypad():
  def __init__(self):
    
    self.pin_R0 = digitalio.DigitalInOut(D1) # Top Row
    self.pin_R1 = digitalio.DigitalInOut(D6)
    self.pin_R2 = digitalio.DigitalInOut(D5)
    self.pin_R3 = digitalio.DigitalInOut(D19) # Bottom Row
    self.pin_C0 = digitalio.DigitalInOut(D16) # Leftmost Column
    self.pin_C1 = digitalio.DigitalInOut(D26)
    self.pin_C2 = digitalio.DigitalInOut(D20)
    self.pin_C3 = digitalio.DigitalInOut(D21) # Rightmost Column
    
    self.rows = [
      self.pin_R0,
      self.pin_R1,
      self.pin_R2,
      self.pin_R3]
    self.cols = [
      self.pin_C0,
      self.pin_C1,
      self.pin_C2,
      self.pin_C3]    
    
    self.rows[0].direction = digitalio.Direction.OUTPUT
    self.rows[1].direction = digitalio.Direction.OUTPUT
    self.rows[2].direction = digitalio.Direction.OUTPUT
    self.rows[3].direction = digitalio.Direction.OUTPUT
    self.cols[0].direction = digitalio.Direction.INPUT
    self.cols[1].direction = digitalio.Direction.INPUT
    self.cols[2].direction = digitalio.Direction.INPUT
    self.cols[3].direction = digitalio.Direction.INPUT
    
    self.cols[0].pull = digitalio.Pull.DOWN
    self.cols[1].pull = digitalio.Pull.DOWN
    self.cols[2].pull = digitalio.Pull.DOWN
    self.cols[3].pull = digitalio.Pull.DOWN
    
  def keypad_poll(self):
    """
    polls the keypad and returns the button label (1,2,A,B,*,#, etc) 
    of the button pressed.
    """
    # Set each row high and check if a column went high as well
    for row in range(len(self.rows)):
      self.rows[row].value = True
      for col in range(len(self.cols)):
        if self.cols[col].value:
          self.rows[row].value = False
          #print("Button: ", row, " ", col)
          return constants.KEY_VALUES[row][col]
      self.rows[row].value = False

    # No buttons were pressed
    return None

  def keypad_poll_all(self):
    """
    polls the keypad and returns the button label (1,2,A,B,*,#, etc) 
    of the button pressed.
    """
    results = []
    # Set each row high and check if a column went high as well
    for row in range(len(self.rows)):
      self.rows[row].value = True
      for col in range(len(self.cols)):
        if self.cols[col].value:
          results.append('1')
        else:
          results.append('0')
      self.rows[row].value = False

    # No buttons were pressed
    return results

  def readRow(self,lcd, line, characters):
    """
    Reads a row and prints any pressed characters to the screen
    """
    self.rows[line].value = True

    if (constants.KEY_COL_0.value==1):
      ui_lcd.out(str(characters[0]),constants.LCD_LINE_1,1)
      print(characters[0])
    if (constants.KEY_COL_1.value==1):
      ui_lcd.out(str(characters[1]),constants.LCD_LINE_1,1)
      print(characters[0])
    if (constants.KEY_COL_2.value==1):
      ui_lcd.out(str(characters[2]),constants.LCD_LINE_1,1)
      print(characters[0])
    if (constants.KEY_COL_3.value==1):
      ui_lcd.out(str(characters[3]),constants.LCD_LINE_1,1)
      print(characters[0])
      
    self.rows[line].value = False
    
      
if __name__ == '__main__':
 
  try:
      # Main program block
    key = Keypad()

  except KeyboardInterrupt:
    pass

# WAIT STOP DON'T PUT A FUNCTION DOWN HERE
