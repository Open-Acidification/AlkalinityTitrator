# import
import digitalio
import interfaces
import time
from board import *
import constants


class LCD:
    """Sunfire LCD 2x16 Char Display Module"""

    def __init__(self):
        # Set up pins
        self.pin_RS = digitalio.DigitalInOut(D27)  # RS
        self.pin_E = digitalio.DigitalInOut(D22)  # E
        self.pin_D4 = digitalio.DigitalInOut(D18)  # DB4
        self.pin_D5 = digitalio.DigitalInOut(D23)  # DB5
        self.pin_D6 = digitalio.DigitalInOut(D24)  # DB6
        self.pin_D7 = digitalio.DigitalInOut(D25)  # DB7
        self.pin_ON = digitalio.DigitalInOut(D15)  # Backlight enable

        self.pin_E.direction = digitalio.Direction.OUTPUT
        self.pin_RS.direction = digitalio.Direction.OUTPUT
        self.pin_D4.direction = digitalio.Direction.OUTPUT
        self.pin_D5.direction = digitalio.Direction.OUTPUT
        self.pin_D6.direction = digitalio.Direction.OUTPUT
        self.pin_D7.direction = digitalio.Direction.OUTPUT
        self.pin_ON.direction = digitalio.Direction.OUTPUT

        # Initialize line registers with splash screen
        self.reg_line_1 = "Open".center(constants.LCD_WIDTH, " ")
        self.reg_line_2 = "Acidification".center(constants.LCD_WIDTH, " ")
        self.reg_line_3 = "Project".center(constants.LCD_WIDTH, " ")
        self.reg_line_4 = "Alkalinity Titrator".center(constants.LCD_WIDTH, " ")

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

        self.out_line(self.reg_line_1, constants.LCD_LINE_1, constants.LCD_CENT_JUST)
        self.out_line(self.reg_line_2, constants.LCD_LINE_2, constants.LCD_CENT_JUST)
        self.out_line(self.reg_line_3, constants.LCD_LINE_3, constants.LCD_CENT_JUST)
        self.out_line(self.reg_line_4, constants.LCD_LINE_4, constants.LCD_CENT_JUST)

        time.sleep(1)

    def __lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        self.pin_RS.value = mode  # RS

        # High bits
        self.pin_D4.value = False
        self.pin_D5.value = False
        self.pin_D6.value = False
        self.pin_D7.value = False
        if bits & 0x10 == 0x10:
            self.pin_D4.value = True
        if bits & 0x20 == 0x20:
            self.pin_D5.value = True
        if bits & 0x40 == 0x40:
            self.pin_D6.value = True
        if bits & 0x80 == 0x80:
            self.pin_D7.value = True

        # Toggle 'Enable' pin
        self.__lcd_toggle_enable()

        # Low bits
        self.pin_D4.value = False
        self.pin_D5.value = False
        self.pin_D6.value = False
        self.pin_D7.value = False
        if bits & 0x01 == 0x01:
            self.pin_D4.value = True
        if bits & 0x02 == 0x02:
            self.pin_D5.value = True
        if bits & 0x04 == 0x04:
            self.pin_D6.value = True
        if bits & 0x08 == 0x08:
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

    def out(self, message, style=1):
        """
        Sends a string out to the bottom line of the display,
        shifting the previous lines up once
        """
        if style == 1:
            message = message.ljust(constants.LCD_WIDTH, " ")
        elif style == 2:
            message = message.center(constants.LCD_WIDTH, " ")
        elif style == 3:
            message = message.rjust(constants.LCD_WIDTH, " ")

        # Increment lines upward
        self.reg_line_1 = self.reg_line_2
        self.reg_line_2 = self.reg_line_3
        self.reg_line_3 = self.reg_line_4
        self.reg_line_4 = message

        self.__write_message(self.reg_line_1, constants.LCD_LINE_1)
        # time.sleep(0.5)
        self.__write_message(self.reg_line_2, constants.LCD_LINE_2)
        # time.sleep(0.5)
        self.__write_message(self.reg_line_3, constants.LCD_LINE_3)
        # time.sleep(0.5)
        self.__write_message(self.reg_line_4, constants.LCD_LINE_4)
        # time.sleep(0.5)

    def out_line(self, message, line, style=1):
        """
        Send string to display.
        Lines: LCD_LINE_X (1,2,3,4)
        styles (justification): X (1=left, 2=center, 3=right)
        """

        if style == 1:
            message = message.ljust(constants.LCD_WIDTH, " ")
        elif style == 2:
            message = message.center(constants.LCD_WIDTH, " ")
        elif style == 3:
            message = message.rjust(constants.LCD_WIDTH, " ")

        if line == constants.LCD_LINE_1:
            self.reg_line_1 = message
        elif line == constants.LCD_LINE_2:
            self.reg_line_2 = message
        elif line == constants.LCD_LINE_3:
            self.reg_line_3 = message
        elif line == constants.LCD_LINE_4:
            self.reg_line_4 = message

        self.__write_message(message, line)

    def __write_message(self, message, line):
        # print(message, line)
        self.__lcd_byte(line, constants.LCD_CMD)

        for i in range(constants.LCD_WIDTH):
            self.__lcd_byte(ord(message[i]), constants.LCD_CHR)

    def lcd_backlight(self, flag):
        # Toggle backlight on-off-on
        self.pin_ON.value = flag

    def clear_screen(self):
        # Clear the screen
        blank = ""
        blank = blank.ljust(constants.LCD_WIDTH, " ")

        self.reg_line_1 = blank
        self.reg_line_2 = blank
        self.reg_line_3 = blank
        self.reg_line_4 = blank

        self.__write_message(blank, constants.LCD_LINE_1)
        self.__write_message(blank, constants.LCD_LINE_2)
        self.__write_message(blank, constants.LCD_LINE_3)
        self.__write_message(blank, constants.LCD_LINE_4)


class Keypad:
    def __init__(self):

        self.pin_R0 = digitalio.DigitalInOut(D1)  # Top Row
        self.pin_R1 = digitalio.DigitalInOut(D6)
        self.pin_R2 = digitalio.DigitalInOut(D5)
        self.pin_R3 = digitalio.DigitalInOut(D19)  # Bottom Row
        self.pin_C0 = digitalio.DigitalInOut(D16)  # Leftmost Column
        self.pin_C1 = digitalio.DigitalInOut(D26)
        self.pin_C2 = digitalio.DigitalInOut(D20)
        self.pin_C3 = digitalio.DigitalInOut(D21)  # Rightmost Column

        self.rows = [self.pin_R0, self.pin_R1, self.pin_R2, self.pin_R3]
        self.cols = [self.pin_C0, self.pin_C1, self.pin_C2, self.pin_C3]

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
                    # print("Button: ", row, " ", col)
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
                    results.append("1")
                else:
                    results.append("0")
            self.rows[row].value = False

        # No buttons were pressed
        return results

    def readRow(self, lcd, line, characters):
        """
        Reads a row and prints any pressed characters to the screen
        """
        self.rows[line].value = True

        if constants.KEY_COL_0.value == 1:
            lcd.out(str(characters[0]), constants.LCD_LINE_1, 1)
            print(characters[0])
        if constants.KEY_COL_1.value == 1:
            lcd.out(str(characters[1]), constants.LCD_LINE_1, 1)
            print(characters[0])
        if constants.KEY_COL_2.value == 1:
            lcd.out(str(characters[2]), constants.LCD_LINE_1, 1)
            print(characters[0])
        if constants.KEY_COL_3.value == 1:
            lcd.out(str(characters[3]), constants.LCD_LINE_1, 1)
            print(characters[0])

        self.rows[line].value = False


if __name__ == "__main__":

    try:
        # Main program block
        lcd = LCD()
        key = Keypad()

        # test_lcd(lcd, key)
        # test_keypad(lcd, key)
    except KeyboardInterrupt:
        pass

# WAIT STOP DON'T PUT A FUNCTION DOWN HERE
