"""
The file for mock Keypad class
"""
import click

# pylint: disable = R0913, W0107, R0903


class Keypad:
    """
    This is a class for the mock Keypad class
    """

    def __init__(self, r_zero, r_one, r_two, r_three, c_zero, c_one, c_two, c_three):
        """
        The constructor for the mock Keypad class.
        The Parameters are the board pins that the keypad uses
        """
        pass

    def keypad_poll(self):
        """
        The function to poll a keyboard press
        """
        return click.getchar()
