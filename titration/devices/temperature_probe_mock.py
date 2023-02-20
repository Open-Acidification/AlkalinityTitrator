"""
Mock temperature probe class
"""

# pylint: disable = too-many-arguments, unused-argument


class TemperatureProbe:
    """
    The class for the Temperature Probe
    """

    def __init__(self, sck, mosi, miso, c_s, wires=2):
        """
        The constructor for the temperature probe
        """
        self.resistance = 1000.0
        self.temperature = 0

    def get_temperature(self):
        """
        The function to get the temperature
        """
        return self.temperature

    def get_resistance(self):
        """
        The function to get Temperature Probe resistance
        """
        return self.resistance

    def mock_set_temperature(self, temperature):
        """
        The function to set the mock temperature
        """
        self.temperature = temperature

    def mock_set_resistance(self, resistance):
        """
        The function to set the mock resistance
        """
        self.resistance = resistance

    def read_temperature(self):
        """
        Reads and returns the temperature from GPIO
        :returns: temperature in celsius, resistance in ohms
        """
        return self.get_temperature(), self.get_resistance()
