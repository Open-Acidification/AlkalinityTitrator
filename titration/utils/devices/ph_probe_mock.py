"""
Mock ph probe class
"""

# pylint: disable = W0613


class PhProbe:
    """
    The class for the mock PhProbe
    """

    def __init__(self, scl, sda, gain=1):
        """
        The constructor for the PhProbe class
        """
        self.gain = gain

        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

        self.volt = 0

    def voltage(self):
        """
        The function to return the mock voltage
        """
        return self.volt

    def set_gain(self, gain):
        """
        The function to set the mock gain
        """
        if gain not in self.gain_options:
            raise ValueError(f"Gain must be one of: {self.gain_options}")
        self.gain = gain

    def get_gain(self):
        """
        The function to get the mock gain
        """
        return self.gain

    def mock_set_voltage(self, voltage):
        """
        The function to set the mock voltage
        """
        self.volt = voltage
