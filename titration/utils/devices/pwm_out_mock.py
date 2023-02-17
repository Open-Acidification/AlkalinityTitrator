"""
The file for the mock PWMOut class
"""


class PWMOut:
    """
    The class for the mock PWMOut
    """

    def __init__(self, pin, duty_cycle, frequency):
        """
        The constructor for the mock PWMOut class
        """
        self.pin = pin
        self.duty_cycle = duty_cycle
        self.frequency = frequency
