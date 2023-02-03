"""
The file for the Keypad class
"""
import digitalio
from titration.utils import constants

KEY_VALUES = {
    0: {
        0: constants.KEY_1,
        1: constants.KEY_2,
        2: constants.KEY_3,
        3: constants.KEY_A,
    },
    1: {
        0: constants.KEY_4,
        1: constants.KEY_5,
        2: constants.KEY_6,
        3: constants.KEY_B,
    },
    2: {
        0: constants.KEY_7,
        1: constants.KEY_8,
        2: constants.KEY_9,
        3: constants.KEY_C,
    },
    3: {
        0: constants.KEY_STAR,
        1: constants.KEY_0,
        2: constants.KEY_HASH,
        3: constants.KEY_D,
    },
}


class Keypad:
    """
    The class for the Keypad
    """

    def __init__(self, r0, r1, r2, r3, c0, c1, c2, c3):
        """
        The constructor for the mock Keypad class.
        The parameters are the board pins that the keypad uses
        """
        self.pin_R0 = digitalio.DigitalInOut(r0)
        self.pin_R1 = digitalio.DigitalInOut(r1)
        self.pin_R2 = digitalio.DigitalInOut(r2)
        self.pin_R3 = digitalio.DigitalInOut(r3)
        self.pin_C0 = digitalio.DigitalInOut(c0)
        self.pin_C1 = digitalio.DigitalInOut(c1)
        self.pin_C2 = digitalio.DigitalInOut(c2)
        self.pin_C3 = digitalio.DigitalInOut(c3)

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
        The function that polls the keypad and returns the
        button label (1,2,A,B,*,#, etc) of the button pressed.
        """
        for row in range(len(self.rows)):
            self.rows[row].value = True
            for col in range(len(self.cols)):
                if self.cols[col].value:
                    self.rows[row].value = False
                    return KEY_VALUES[row][col]
            self.rows[row].value = False

        return None
