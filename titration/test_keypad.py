"""
Module for mocking the keypad.py Keypad() class for testing purposes
"""


class test_Keypad:
    def __init__(self):
        # Flag for emulating the button being pressed and then released
        self.buttonPressed = False

    def keypad_poll(self):
        if not self.buttonPressed:
            self.buttonPressed = not self.buttonPressed
            return input()
        else:
            self.buttonPressed = not self.buttonPressed
            return None
