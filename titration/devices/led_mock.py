"""
The file for the mock LED class
"""

# pylint: disable = invalid-name


class LED:
    """
    The mock LED class
    """

    def __init__(self, pin):
        """
        The constructor for the mock LED class
        """
        self.pin = pin
        self.value = False

    def on(self):
        """
        Turns the mock LED on
        """
        self.value = True

    def off(self):
        """
        Turns the mock LED off
        """
        self.value = False
