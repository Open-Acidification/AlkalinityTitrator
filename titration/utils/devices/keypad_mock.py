"""
The file for mock Keypad class
"""
import click
import digitalio
from AlkalinityTitrator.titration.utils.devices import board_mock as board


class Keypad:
    """
    The class for the mock Keypad
    """

    def __init__(self):
        """
        The constructor for the mock Keypad class.
        The parameters are the board pins that the keypad uses
        """

        self.pin_r_zero = board.D1
        self.pin_r_one = board.D6
        self.pin_r_two = board.D5
        self.pin_r_three = board.D19
        self.pin_c_zero = board.D16
        self.pin_c_one = board.D26
        self.pin_c_two = board.D20
        self.pin_c_three = board.D21

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
        The function to poll a keyboard press
        """
        return click.getchar()
