"""
The file for mock Keypad class
"""
import digitalio

from titration.devices.library import board


class Keypad:
    """
    The class for the mock Keypad
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

    def __init__(self):
        """
        The constructor for the mock Keypad class.
        The parameters are the board pins that the keypad uses
        """
        self.key_pressed = None

        self.pin_r0 = board.D1
        self.pin_r1 = board.D6
        self.pin_r2 = board.D5
        self.pin_r3 = board.D19
        self.pin_c0 = board.D16
        self.pin_c1 = board.D26
        self.pin_c2 = board.D20
        self.pin_c3 = board.D21

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

    def set_key(self, key):
        """
        The function to set the key for the GUI
        """
        self.key_pressed = key

    def get_key(self):
        """
        The function to poll a keyboard press
        """
        temp = self.key_pressed
        self.key_pressed = None
        return temp
