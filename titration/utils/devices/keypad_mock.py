"""
Module for mocking the keypad.py Keypad() class for testing purposes
"""
import click


class Keypad:
    def __init__(self, r0, r1, r2, r3, c0, c1, c2, c3):
        # Flag for emulating the button being pressed and then released
        pass

    def keypad_poll(self):
        return click.getchar()
