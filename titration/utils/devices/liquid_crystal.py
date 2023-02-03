"""
The file for the Sunfire LCD 20x04 Char Display, LiquidCrystal Class
"""
import time
import digitalio
from titration.utils import constants


class LiquidCrystal:
    """
    The class for the Sunfire LCD 20x04 Char Display
    """

    def __init__(self, rs, backlight, enable, d4, d5, d6, d7, cols, rows):
        """
        The constructor for the mock LiquidCrystal class.
        The parameters are the board pins that the LCD uses
        """

        self.pin_RS = digitalio.DigitalInOut(rs)
        self.pin_E = digitalio.DigitalInOut(enable)
        self.pin_D4 = digitalio.DigitalInOut(d4)
        self.pin_D5 = digitalio.DigitalInOut(d5)
        self.pin_D6 = digitalio.DigitalInOut(d6)
        self.pin_D7 = digitalio.DigitalInOut(d7)
        self.pin_ON = digitalio.DigitalInOut(backlight)

        self.pin_E.direction = digitalio.Direction.OUTPUT
        self.pin_RS.direction = digitalio.Direction.OUTPUT
        self.pin_D4.direction = digitalio.Direction.OUTPUT
        self.pin_D5.direction = digitalio.Direction.OUTPUT
        self.pin_D6.direction = digitalio.Direction.OUTPUT
        self.pin_D7.direction = digitalio.Direction.OUTPUT
        self.pin_ON.direction = digitalio.Direction.OUTPUT

        self.cols = cols
        self.rows = rows

        # Initialise display
        self.__lcd_byte(0x33, constants.LCD_CMD)  # 110011 Initialise
        self.__lcd_byte(0x32, constants.LCD_CMD)  # 110010 Initialise
        self.__lcd_byte(0x06, constants.LCD_CMD)  # 000110 Cursor move direction
        self.__lcd_byte(
            0x0C, constants.LCD_CMD
        )  # 001100 Display On,Cursor Off, Blink Off
        self.__lcd_byte(
            0x28, constants.LCD_CMD
        )  # 101000 Data length, number of lines, font size
        self.__lcd_byte(0x01, constants.LCD_CMD)  # 000001 Clear display
        time.sleep(constants.E_DELAY)

        # Toggle backlight on-off-on
        self.lcd_backlight(True)
        time.sleep(0.5)
        self.lcd_backlight(False)
        time.sleep(0.5)
        self.lcd_backlight(True)
        time.sleep(0.5)

    def clear(self):
        """
        The function to clear the LCD
        """
        blank = "".ljust(self.cols, " ")

        self.__write(blank, constants.LCD_LINE_1)
        self.__write(blank, constants.LCD_LINE_2)
        self.__write(blank, constants.LCD_LINE_3)
        self.__write(blank, constants.LCD_LINE_4)

    def print(self, message, line, style=1):
        """
        The function to send a string to the LCD on a given line and type

        Parameters:
            message (string): the message to be displayed on the screen
            line (int): the line to display the message on
            styles (int): 1=left centered, 2=centered , 3=right centered
        """
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not be initialized with begin()")

        if style == 1:
            message = message.ljust(self.cols, " ")
        elif style == 2:
            message = message.center(self.cols, " ")
        elif style == 3:
            message = message.rjust(self.cols, " ")

        if line == 1:
            line = constants.LCD_LINE_1
        elif line == 2:
            line = constants.LCD_LINE_2
        elif line == 3:
            line = constants.LCD_LINE_3
        elif line == 4:
            line = constants.LCD_LINE_4

        self.__write(message, line)

    def lcd_backlight(self, enable):
        """
        The function to turn the LCD backlight on or off

        Parameters:
            enable (bool): enable is whether the lcd_backlight is on or off
        """
        self.pin_ON.value = enable

    def __write(self, message, line):
        """
        The function to write characters to the LCD

        Parameters:
            message (string): the message to be displayed on the screen
            line (int): the line to display the message on
        """
        self.__lcd_byte(line, constants.LCD_CMD)

        for i in range(self.rows):
            self.__lcd_byte(ord(message[i]), constants.LCD_CHR)

    def __lcd_byte(self, bits, mode):
        """
        The function to send the initialization bits to the LCD pins

        Parameters:
            bits (hex): the bits to be sent on the pin
            mode (bool): True for character, False for command
        """
        self.pin_RS.value = mode

        # High bits
        self.pin_D4.value = bits & 0x10 == 0x10
        self.pin_D5.value = bits & 0x20 == 0x20
        self.pin_D6.value = bits & 0x40 == 0x40
        self.pin_D7.value = bits & 0x80 == 0x80

        self.__lcd_toggle_enable()

        # Low bits
        self.pin_D4.value = bits & 0x01 == 0x01
        self.pin_D5.value = bits & 0x02 == 0x02
        self.pin_D6.value = bits & 0x04 == 0x04
        self.pin_D7.value = bits & 0x08 == 0x08

        self.__lcd_toggle_enable()

    def __lcd_toggle_enable(self):
        """
        The function to toggle the LCD enable pin
        """
        time.sleep(constants.E_DELAY)
        self.pin_E.value = True
        time.sleep(constants.E_PULSE)
        self.pin_E.value = False
        time.sleep(constants.E_DELAY)

    def display_list(self, dict_to_display):
        """
        The function to display a list of options from a dictionary.
        Only the first four options will be displayed due to only four screen rows.

        Parameters:
            dict_to_display (dict): list to be displayed on LCD screen
        """
        self.clear()
        keys = list(dict_to_display.keys())
        values = list(dict_to_display.values())
        lines = [1, 2, 3, 4]

        for i in range(min(len(keys), 4)):
            self.print(str(keys[i]) + ". " + values[i], lines[i])
