"""
Mock ph probe class
"""


class pH_Probe:
    def __init__(self, scl, sda, gain=1):
        self.gain = gain

        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

    def voltage(self):
        return 3.14159

    def set_gain(self, gain):
        if gain not in self.gain_options:
            raise ValueError("Gain must be one of: {}".format(self.gain_options))
        else:
            self.gain = gain

    def get_gain(self):
        return self.gain
