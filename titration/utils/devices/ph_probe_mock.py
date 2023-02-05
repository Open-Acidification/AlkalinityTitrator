"""
The file for the mock pH_Probe class
"""


class pH_Probe:
    """
    The class for the mock pH Probe
    """

    def __init__(self, scl, sda, gain=1):
        """
        The constructor for the mock pH_Probe class
        Initializes I2C pins, gain, and voltage

        Parameters:
            scl (Pin object): I2C clock pin
            sda (Pin object): I2C data pin
            gain (int): gain of the pH_Probe
        """
        self.i2c = (scl, sda)
        self.ads = self.i2c
        self.channel = (self.ads, "ADS.P0", "ADS.P1")

        self.gain = gain
        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

        self.volt = 0

    def get_voltage(self):
        """
        The function to return the mock pH_Probe voltage
        """
        return self.volt

    def set_gain(self, gain):
        """
        The function to set the mock pH_Probe gain

        Parameters:
            gain (int): the gain of the pH_Probe
        """
        if gain not in self.gain_options:
            raise ValueError("Gain must be one of: {}".format(self.gain_options))
        else:
            self.gain = gain

    def get_gain(self):
        """
        The function to get the mock pH_Probe gain
        """
        return self.gain
