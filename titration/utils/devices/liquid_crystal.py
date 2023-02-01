import time

import digitalio

from titration.utils import constants


class LiquidCrystal:
    """Sunfire LCD 20x04 Char Display Module"""

    def __init__(self, rs, backlight, enable, d4, d5, d6, d7, cols, rows):
        # Set up pins
        self.pin_RS = digitalio.DigitalInOut(rs)  # RS
        self.pin_E = digitalio.DigitalInOut(enable)  # E
        self.pin_D4 = digitalio.DigitalInOut(d4)  # DB4
        self.pin_D5 = digitalio.DigitalInOut(d5)  # DB5
        self.pin_D6 = digitalio.DigitalInOut(d6)  # DB6
        self.pin_D7 = digitalio.DigitalInOut(d7)  # DB7
        self.pin_ON = digitalio.DigitalInOut(backlight)  # Backlight enable

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
        # Clear the screen
        blank = ""
        blank = blank.ljust(constants.LCD_WIDTH, " ")

        self.__write(blank, constants.LCD_LINE_1)
        self.__write(blank, constants.LCD_LINE_2)
        self.__write(blank, constants.LCD_LINE_3)
        self.__write(blank, constants.LCD_LINE_4)

    def print(self, message, line, style=1):
        """
        Send string to display.
        Lines: LCD_LINE_X (1,2,3,4)
        styles (justification): X (1=left, 2=center, 3=right)
        """
        # Check if begin() has been run
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not be initialized with begin()")

        if style == 1:
            message = message.ljust(constants.LCD_WIDTH, " ")
        elif style == 2:
            message = message.center(constants.LCD_WIDTH, " ")
        elif style == 3:
            message = message.rjust(constants.LCD_WIDTH, " ")

        if line == 1:
            line = constants.LCD_LINE_1
        elif line == 2:
            line = constants.LCD_LINE_2
        elif line == 3:
            line = constants.LCD_LINE_3
        elif line == 4:
            line = constants.LCD_LINE_4

        self.__write(message, line)

    def lcd_backlight(self, flag):
        # Toggle backlight on-off-on
        self.pin_ON.value = flag

    def __write(self, message, line):
        """
        Prints a character to the LCD
        """
        # print(message, line)
        self.__lcd_byte(line, constants.LCD_CMD)

        for i in range(constants.LCD_WIDTH):
            self.__lcd_byte(ord(message[i]), constants.LCD_CHR)

    def __lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        self.pin_RS.value = mode  # RS

        # High bits
        self.pin_D4.value = bits & 0x10 == 0x10
        self.pin_D5.value = bits & 0x20 == 0x20
        self.pin_D6.value = bits & 0x40 == 0x40
        self.pin_D7.value = bits & 0x80 == 0x80

        # Toggle 'Enable' pin
        self.__lcd_toggle_enable()

        # Low bits
        self.pin_D4.value = bits & 0x01 == 0x01
        self.pin_D5.value = bits & 0x02 == 0x02
        self.pin_D6.value = bits & 0x04 == 0x04
        self.pin_D7.value = bits & 0x08 == 0x08

        # Toggle 'Enable' pin
        self.__lcd_toggle_enable()

    def __lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(constants.E_DELAY)
        self.pin_E.value = True
        time.sleep(constants.E_PULSE)
        self.pin_E.value = False
        time.sleep(constants.E_DELAY)

    def display_list(self, dict_to_display):
        """
        Display a list of options from a dictionary. Only the first four
        options will be displayed due to only four screen rows.
        :param list_to_display: list to be displayed on LCD screen
        """
        self.clear()
        keys = list(dict_to_display.keys())
        values = list(dict_to_display.values())
        lines = [1, 2, 3, 4]

        for i in range(min(len(keys), 4)):
            self.print(str(keys[i]) + ". " + values[i], lines[i])

        # Original method, slow due to screen scrolling
        # for key, value in list_to_display.items():
        #   print(str(key) + '. ' + value)
