"""
Mock ph probe class
"""


class pH_Probe:
    def __init__(self, scl, sda, gain=1):
        self.gain = gain

        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

        self.volt = 0

    def voltage(self):
        return self.volt

    def set_gain(self, gain):
        if gain not in self.gain_options:
            raise ValueError("Gain must be one of: {}".format(self.gain_options))
        else:
            self.gain = gain

    def get_gain(self):
        return self.gain
    
    def mock_set_voltage(self, voltage):
        self.volt = voltage
