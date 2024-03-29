"""
The file for mocking the LiquidCrystal class for testing purposes
"""

# pylint: disable = unused-argument

LCD_WIDTH = 20
LCD_HEIGHT = 4


class LiquidCrystal:
    """
    The class for the mock of the Sunfire LCD 20x04 Char Display
    """

    def __init__(self):
        """
        The function to initialize the gui lcd
        """
        self.cols = LCD_WIDTH
        self.rows = LCD_HEIGHT

        self.lcd_lines = [None, None, None, None]
        self.lcd_line_styles = [None, None, None, None]

    def print(self, message, line, style="left"):
        """
        The function to send a string to the GUI LCD
        """
        if style == "left":
            style = "w"
        elif style == "right":
            style = "e"

        if line == 1:
            self.lcd_lines[0] = message
            self.lcd_line_styles[0] = style
        elif line == 2:
            self.lcd_lines[1] = message
            self.lcd_line_styles[1] = style
        elif line == 3:
            self.lcd_lines[2] = message
            self.lcd_line_styles[2] = style
        elif line == 4:
            self.lcd_lines[3] = message
            self.lcd_line_styles[3] = style

    def get_line(self, line):
        """
        The function to get the lcd line message
        """
        if line == 1:
            return self.lcd_lines[0]
        if line == 2:
            return self.lcd_lines[1]
        if line == 3:
            return self.lcd_lines[2]
        if line == 4:
            return self.lcd_lines[3]
        return "ERROR"

    def get_style(self, line):
        """
        The function to get the lcd line message
        """
        if line == 1:
            return self.lcd_line_styles[0]
        if line == 2:
            return self.lcd_line_styles[1]
        if line == 3:
            return self.lcd_line_styles[2]
        if line == 4:
            return self.lcd_line_styles[3]
        return "ERROR"
