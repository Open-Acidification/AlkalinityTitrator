P0 = None
P1 = None
P2 = None
P3 = None


class ADS1115:
    def __init__(self, i2c, gain=1, data_rate=None, mode=None, address=None):
        self.i2c = i2c
        self.gain = gain
        self.data_rate = data_rate
        self.mode = mode
        self.address = address
