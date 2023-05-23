"""
The file for the Keypad device class
"""

# pylint: disable = consider-using-enumerate

import board
import digitalio


class Keypad:
    """
    The class for the Keypad
    """

    KEY_0 = "0"
    KEY_1 = "1"
    KEY_2 = "2"
    KEY_3 = "3"
    KEY_4 = "4"
    KEY_5 = "5"
    KEY_6 = "6"
    KEY_7 = "7"
    KEY_8 = "8"
    KEY_9 = "9"
    KEY_A = "A"
    KEY_B = "B"
    KEY_C = "C"
    KEY_D = "D"
    KEY_STAR = "*"
    KEY_HASH = "#"

    KEY_VALUES = {
        0: {
            0: KEY_1,
            1: KEY_2,
            2: KEY_3,
            3: KEY_A,
        },
        1: {
            0: KEY_4,
            1: KEY_5,
            2: KEY_6,
            3: KEY_B,
        },
        2: {
            0: KEY_7,
            1: KEY_8,
            2: KEY_9,
            3: KEY_C,
        },
        3: {
            0: KEY_STAR,
            1: KEY_0,
            2: KEY_HASH,
            3: KEY_D,
        },
    }

    def __init__(self):
        """
        The constructor for the mock Keypad class.
        """

        self.pin_r0 = digitalio.DigitalInOut(board.D1)
        self.pin_r1 = digitalio.DigitalInOut(board.D6)
        self.pin_r2 = digitalio.DigitalInOut(board.D5)
        self.pin_r3 = digitalio.DigitalInOut(board.D19)
        self.pin_c0 = digitalio.DigitalInOut(board.D16)
        self.pin_c1 = digitalio.DigitalInOut(board.D26)
        self.pin_c2 = digitalio.DigitalInOut(board.D20)
        self.pin_c3 = digitalio.DigitalInOut(board.D21)

        self.rows = [self.pin_r0, self.pin_r1, self.pin_r2, self.pin_r3]
        self.cols = [self.pin_c0, self.pin_c1, self.pin_c2, self.pin_c3]

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

        self.key = None

    def get_key(self):
        """
        The function that gets a key from user input
        """
        if self.key != self.keypad_poll():
            self.key = self.keypad_poll()
            return self.keypad_poll()
        return None

    def keypad_poll(self):
        """
        The function that polls the keypad and returns the button label (1,2,A,B,*,#, etc)
        of the button pressed.
        """
        for row in range(len(self.rows)):
            self.rows[row].value = True
            for col in range(len(self.cols)):
                if self.cols[col].value:
                    self.rows[row].value = False
                    return self.KEY_VALUES[row][col]
            self.rows[row].value = False

        return None
