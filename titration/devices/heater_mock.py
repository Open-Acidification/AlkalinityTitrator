"""
The file for the mock Heater class
"""


class Heater:
    """
    The mock Heater class. This class intends to mock the LED class found here:
    https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=LED
    """

    def __init__(self, pin):
        """
        The constructor for the mock Heater class
        """
        self.pin = pin
        self.value = False

    def on(self):
        """
        Turns the mock Heater on
        """
        self.value = True

    def off(self):
        """
        Turns the mock Heater off
        """
        self.value = False
