"""
Module for mocking the lcd.py class for testing purposes
"""
#import pytest

class test_LCD:
  def __init__(self):
    self.cols = -1
    self.rows = -1

    self.strings = []

  def begin(self, cols, rows):
    self.cols = cols
    self.rows = rows
    
    # Create empty arrays for strings
    for i in range(0, rows):
      self.strings.append("".ljust(cols))

    # Draw mock display
    self.__draw()

  def clear(self):
    for i in range(len(self.strings)):
      self.strings[i] = "".ljust(self.cols," ")
    self.__draw()


  def print(self, message, line, style=1):
    if style==1:
      message = message.ljust(self.cols," ")
    elif style==2:
      message = message.center(self.cols," ")
    elif style==3:
      message = message.rjust(self.cols," ")

    self.strings[line-1] = message

    self.__draw()

  def lcd_backlight(self, flag):
    pass

  def __draw(self):
    """
    Draws the mock display
    """
    for i in range(-1, self.rows + 1):
      if i == -1 or i == self.rows:
        print('*',''.ljust(self.cols,'='),'*', sep='')
      else:
        print('|',self.strings[i],'|', sep='')

if __name__ == "__main__":
  try:
    lcd = test_LCD()
    lcd.begin(20,4)
    lcd.print("Open Acidification",1,2)
    lcd.print("Project",2,2)
    lcd.print("Alkalinity",3,2)
    lcd.print("Titrator",4,2)
    lcd.clear()

  except:
    pass