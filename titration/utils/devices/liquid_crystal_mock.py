"""
Module for mocking the liquid_crystal.py class for testing purposes
"""
from os import name, system

# pylint: disable = W0613, R0913


class LiquidCrystal:
    """
    The class for the Liquid Crystal Display
    """

    def __init__(
        self, r_s, backlight, enable, d_four, d_five, d_six, d_seven, cols, rows
    ):
        """
        The constructor for the LiquidCrystal class
        """
        self.cols = cols
        self.rows = rows

        self.strings = []
        self.clear_flag = True

        self.backlight = True

        # Clear any existing rows
        self.strings.clear()

        # Create empty arrays for strings
        for _ in range(0, rows):
            self.strings.append("".ljust(cols))

        # Draw mock display
        self.__draw()

    def clear(self):
        """
        The function to clear the LCD screen
        """
        for i in enumerate(self.strings):
            self.strings[i[0]] = "".ljust(self.cols, " ")
        self.__draw()

    def print(self, message, line, style=1):
        """
        The function to print to the LCD screen
        """
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not be initialized with begin()")

        if style == 1:
            message = message.ljust(self.cols, " ")
        elif style == 2:
            message = message.center(self.cols, " ")
        elif style == 3:
            message = message.rjust(self.cols, " ")

        self.strings[line - 1] = message[0 : self.cols]

        self.__draw()

    def lcd_backlight(self, flag):
        """
        The function to enable / disable mock LCD
        """
        self.backlight = flag

    def __draw(self):
        """
        Draws the mock display
        """
        if self.clear_flag:
            if name == "nt":
                _ = system("cls")
            else:
                _ = system("clear")

        for i in range(-1, self.rows + 1):
            if i in (-1, self.rows):
                print("*", "".ljust(self.cols, "="), "*", sep="")
            else:
                print("|", self.strings[i], "|", sep="")

    def mock_disable_clear(self):
        """
        The function to disable the mock clear
        """
        self.clear_flag = False

    def mock_enable_clear(self):
        """
        The function to enable the mock clear
        """
        self.clear_flag = True

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
