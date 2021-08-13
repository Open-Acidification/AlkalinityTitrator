"""
Mock temperature probe class
"""


class Temp_Probe:
    def __init__(self, sck, mosi, miso, cs, wires=2):
        self.resistance = 1000.0
        self.temperature = 0

    def get_temperature(self):
        return self.temperature

    def get_resistance(self):
        return self.resistance

    def mock_set_temperature(self, temp):
        self.temperature = temp

    def mock_set_resistance(self, res):
        self.resistance = res
