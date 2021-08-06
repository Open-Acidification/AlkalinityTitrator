"""
Module for mocking the lcd.py class for testing purposes
"""
from os import name, system

class LCD:
    def __init__(self, rs, backlight, enable, d4, d5, d6, d7):
        self.cols = -1
        self.rows = -1

        self.strings = []

    def begin(self, cols, rows):
        self.cols = cols
        self.rows = rows

        # Clear any existing rows
        self.strings.clear()

        # Create empty arrays for strings
        for i in range(0, rows):
            self.strings.append("".ljust(cols))

        # Draw mock display
        self.__draw()

    def clear(self):
        for i in range(len(self.strings)):
            self.strings[i] = "".ljust(self.cols, " ")
        self.__draw()

    def print(self, message, line, style=1):
        # Check if begin() has been run
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not be initialized with begin()")

        if style == 1:
            message = message.ljust(self.cols, " ")
        elif style == 2:
            message = message.center(self.cols, " ")
        elif style == 3:
            message = message.rjust(self.cols, " ")

        self.strings[line - 1] = message

        self.__draw()

    def lcd_backlight(self, flag):
        pass

    def __draw(self):
        """
        Draws the mock display
        """
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

        for i in range(-1, self.rows + 1):
            if i == -1 or i == self.rows:
                print("*", "".ljust(self.cols, "="), "*", sep="")
            else:
                print("|", self.strings[i], "|", sep="")


if __name__ == "__main__":
    try:
        lcd = LCD()
        lcd.begin(20, 4)
        lcd.print("Open Acidification", 1, 2)
        lcd.print("Project", 2, 2)
        lcd.print("Alkalinity", 3, 2)
        lcd.print("Titrator", 4, 2)
        lcd.clear()

    except:
        pass
