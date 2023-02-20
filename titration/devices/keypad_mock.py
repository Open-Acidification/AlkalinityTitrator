"""
The file for mock Keypad class
"""
import click
import digitalio

from titration.devices import board_mock as board


class Keypad:
    """
    The class for the mock Keypad
    """

    def __init__(self):
        """
        The constructor for the mock Keypad class.
        The parameters are the board pins that the keypad uses
        """

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

    def keypad_poll(self):
        """
        The function to poll a keyboard press
        """
        return click.getchar()
