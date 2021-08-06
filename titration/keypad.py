# import
import digitalio

import constants
import interfaces


class Keypad:
    def __init__(self, r0, r1, r2, r3, c0, c1, c2, c3):

        self.pin_R0 = digitalio.DigitalInOut(r0)  # Top Row
        self.pin_R1 = digitalio.DigitalInOut(r1)
        self.pin_R2 = digitalio.DigitalInOut(r2)
        self.pin_R3 = digitalio.DigitalInOut(r3)  # Bottom Row
        self.pin_C0 = digitalio.DigitalInOut(c0)  # Leftmost Column
        self.pin_C1 = digitalio.DigitalInOut(c1)
        self.pin_C2 = digitalio.DigitalInOut(c2)
        self.pin_C3 = digitalio.DigitalInOut(c3)  # Rightmost Column

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

    # Following functions were just used for testing

    # def keypad_poll_all(self):
    #     """
    #     polls the keypad and returns the button label (1,2,A,B,*,#, etc)
    #     of the button pressed.
    #     """
    #     results = []
    #     # Set each row high and check if a column went high as well
    #     for row in range(len(self.rows)):
    #         self.rows[row].value = True
    #         for col in range(len(self.cols)):
    #             if self.cols[col].value:
    #                 results.append("1")
    #             else:
    #                 results.append("0")
    #         self.rows[row].value = False

    #     # No buttons were pressed
    #     return results

    # def readRow(self, lcd, line, characters):
    #     """
    #     Reads a row and prints any pressed characters to the screen
    #     """
    #     self.rows[line].value = True

    #     if constants.KEY_COL_0.value == 1:
    #         interfaces.lcd_out(str(characters[0]), constants.LCD_LINE_1, 1)
    #         print(characters[0])
    #     if constants.KEY_COL_1.value == 1:
    #         interfaces.lcd_out(str(characters[1]), constants.LCD_LINE_1, 1)
    #         print(characters[0])
    #     if constants.KEY_COL_2.value == 1:
    #         interfaces.lcd_out(str(characters[2]), constants.LCD_LINE_1, 1)
    #         print(characters[0])
    #     if constants.KEY_COL_3.value == 1:
    #         interfaces.lcd_out(str(characters[3]), constants.LCD_LINE_1, 1)
    #         print(characters[0])

    #     self.rows[line].value = False


if __name__ == "__main__":
    pass
