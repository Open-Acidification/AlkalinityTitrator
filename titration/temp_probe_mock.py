"""
Mock temperature probe class
"""


class Temp_Probe:
    def __init__(self, sck, mosi, miso, cs, wires=2):
        self.res = 1000.0
        self.temp = 0

    def temperature(self):
        return self.temp

    def resistance(self):
        return self.res
    
    def mock_set_temperature(self, temp):
        self.temp = temp
    
    def mock_set_resistance(self,res):
        self.res = res
