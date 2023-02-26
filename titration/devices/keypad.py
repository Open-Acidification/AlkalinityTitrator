"""
The file for the Keypad device class
"""
import board
import digitalio

from titration import constants

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
        else:
            return None

    def keypad_poll(self):
        """
        The function that polls the keypad and returns the button label (1,2,A,B,*,#, etc)
        of the button pressed.
        """
        for row in enumerate(self.rows):
            self.rows[row].value = True
            for col in enumerate(self.cols):
                if self.cols[col].value:
                    self.rows[row].value = False
                    return KEY_VALUES[row][col]
            self.rows[row].value = False

        return None
