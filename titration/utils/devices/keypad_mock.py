"""
The file for mock Keypad class
"""
import click


class Keypad:
    """
    The class for the mock Keypad
    """

    def __init__(self, r0, r1, r2, r3, c0, c1, c2, c3):
        """
        The constructor for the mock Keypad class.
        The parameters are the board pins that the keypad uses
        """
        self.pin_R0 = r0
        self.pin_R1 = r1
        self.pin_R2 = r2
        self.pin_R3 = r3
        self.pin_C0 = c0
        self.pin_C1 = c1
        self.pin_C2 = c2
        self.pin_C3 = c3

        self.rows = [self.pin_R0, self.pin_R1, self.pin_R2, self.pin_R3]
        self.cols = [self.pin_C0, self.pin_C1, self.pin_C2, self.pin_C3]

        self.rows[0] = "OUTPUT"
        self.rows[1] = "OUTPUT"
        self.rows[2] = "OUTPUT"
        self.rows[3] = "OUTPUT"
        self.cols[0] = "INPUT"
        self.cols[1] = "INPUT"
        self.cols[2] = "INPUT"
        self.cols[3] = "INPUT"

        self.cols[0] = "Pull Down"
        self.cols[1] = "Pull Down"
        self.cols[2] = "Pull Down"
        self.cols[3] = "Pull Down"

    def keypad_poll(self):
        """
        The function to poll a keyboard press
        """
        return click.getchar()
