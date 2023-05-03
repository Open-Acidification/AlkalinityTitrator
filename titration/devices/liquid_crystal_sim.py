"""
The file for mocking the LiquidCrystal class for testing purposes
"""

# pylint: disable = unused-argument


class LiquidCrystal:
    """
    The class for the mock of the Sunfire LCD 20x04 Char Display
    """

    def __init__(self, cols, rows):
        """
        The function to initialize the gui lcd
        """
        self.cols = cols
        self.rows = rows

        self.lcd_line_one = None
        self.lcd_line_two = None
        self.lcd_line_three = None
        self.lcd_line_four = None

    def print(self, message, line, style="left"):
        """
        The function to send a string to the GUI LCD
        """
        if line == 1:
            self.lcd_line_one = message
        elif line == 2:
            self.lcd_line_two = message
        elif line == 3:
            self.lcd_line_three = message
        elif line == 4:
            self.lcd_line_four = message

    def get_line(self, line):
        """
        The function to get the lcd line message
        """
        if line == 1:
            return self.lcd_line_one
        elif line == 2:
            return self.lcd_line_two
        elif line == 3:
            return self.lcd_line_three
        elif line == 4:
            return self.lcd_line_four
        return "ERROR"
