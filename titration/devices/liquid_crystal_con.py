"""
The file for mocking the LiquidCrystal class for testing purposes
"""
from os import name, system

import digitalio

from titration.devices.library import board


class LiquidCrystal:
    """
    The class for the mock of the Sunfire LCD 20x04 Char Display
    """

    def __init__(self, cols, rows):
        """
        The constructor for the mock LiquidCrystal class.
        The parameters are the board pins that the LCD uses
        """

        self.pin_rs = board.D27
        self.pin_e = board.D22
        self.pin_d4 = board.D18
        self.pin_d5 = board.D23
        self.pin_d6 = board.D24
        self.pin_d7 = board.D25
        self.pin_on = board.D15

        self.pin_rs.direction = digitalio.Direction.OUTPUT
        self.pin_e.direction = digitalio.Direction.OUTPUT
        self.pin_d4.direction = digitalio.Direction.OUTPUT
        self.pin_d5.direction = digitalio.Direction.OUTPUT
        self.pin_d6.direction = digitalio.Direction.OUTPUT
        self.pin_d7.direction = digitalio.Direction.OUTPUT
        self.pin_on.direction = digitalio.Direction.OUTPUT

        self.pin_on.value = True

        self.cols = cols
        self.rows = rows

        self.clear_flag = True

        self.strings = []
        self.blank = "".ljust(self.cols)
        for _ in range(0, self.rows):
            self.strings.append(self.blank)

        self.clear()

    def clear(self):
        """
        The function to clear the mock LCD
        """
        self.__clear_sys_out()

        if self.pin_on.value is True:
            for i in range(-1, self.rows + 1):
                if i in (-1, self.rows):
                    print("*", "".ljust(self.cols, "="), "*", sep="")
                else:
                    print("|", self.blank, "|", sep="")

    def print(self, message, line, style="left"):
        """
        The function to send a string to the LCD on a given line and type
        Parameters:
            message (string): the message to be displayed on the screen
            line (int): the line to display the message on
            styles (int): 1=left centered, 2=centered , 3=right centered
        """
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not be initialized with begin()")

        if style == "left":
            message = message.ljust(self.cols, " ")
        elif style == "center":
            message = message.center(self.cols, " ")
        elif style == "right":
            message = message.rjust(self.cols, " ")

        self.__write(message, line)

    def lcd_backlight(self, enable):
        """
        The function to turn the mock LCD backlight on or off
        Parameters:
            enable (bool): enable is whether the lcd_backlight is on or off
        """
        self.pin_on.value = enable

    def __write(self, message, line):
        """
        The function to write characters to the mock LCD
        Parameters:
            message (string): the message to be displayed on the screen
            line (int): the line to display the message on
        """
        self.__clear_sys_out()

        self.strings[line - 1] = message[0 : self.cols]

        if self.pin_on.value is True:
            for i in range(-1, self.rows + 1):
                if i in (-1, self.rows):
                    print("*", "".ljust(self.cols, "="), "*", sep="")
                else:
                    print("|", self.strings[i], "|", sep="")

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

    def mock_disable_clear(self):
        """
        The function to disable the system clear call.
        This function is only used for testing
        """
        self.clear_flag = False

    def __clear_sys_out(self):
        """
        The function to clear the console output
        """
        if self.clear_flag:
            if name == "nt":
                system("cls")
            else:
                system("clear")
