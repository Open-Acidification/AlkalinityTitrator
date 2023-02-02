"""
The file for mock Keypad class 
"""
import click


class Keypad:
    """
    This is a class for the mock Keypad class
    """

    def __init__(self, r0, r1, r2, r3, c0, c1, c2, c3):
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
