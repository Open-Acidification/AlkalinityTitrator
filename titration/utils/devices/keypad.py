"""
The file for the Keypad device class
"""
import digitalio
import board
from AlkalinityTitrator.titration.utils import constants

# pylint: disable = R0902, R0913, R0903

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

        self.pin_r_zero = digitalio.DigitalInOut(board.D1)
        self.pin_r_one = digitalio.DigitalInOut(board.D6)
        self.pin_r_two = digitalio.DigitalInOut(board.D5)
        self.pin_r_three = digitalio.DigitalInOut(board.D19)
        self.pin_c_zero = digitalio.DigitalInOut(board.D16)
        self.pin_c_one = digitalio.DigitalInOut(board.D26)
        self.pin_c_two = digitalio.DigitalInOut(board.D20)
        self.pin_c_three = digitalio.DigitalInOut(board.D21)

        self.rows = [self.pin_r_zero, self.pin_r_one, self.pin_r_two, self.pin_r_three]
        self.cols = [self.pin_c_zero, self.pin_c_one, self.pin_c_two, self.pin_c_three]

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
