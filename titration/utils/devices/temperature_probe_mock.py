"""
Mock temperature probe class
"""


class Temperature_Probe:
    def __init__(self, sck, mosi, miso, cs, wires=2):
        self.resistance = 1000.0
        self.temperature = 0

    def get_temperature(self):
        return self.temperature

    def get_resistance(self):
        return self.resistance

    def mock_set_temperature(self, temperature):
        self.temperature = temperature

    def mock_set_resistance(self, resistance):
        self.resistance = resistance

    def read_temperature(self):
        """
        Reads and returns the temperature from GPIO
        :returns: temperature in celsius, resistance in ohms
        """
        return self.get_temperature(), self.get_resistance()
