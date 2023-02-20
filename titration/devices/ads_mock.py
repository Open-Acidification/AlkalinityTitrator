"""
The file to for the mock ADS1115 class
"""

P0 = None
P1 = None


class ADS1115:
    """
    The class to mock the ads module for the ph_probe
    """

    def __init__(self, i2c, gain=1):
        """
        The constructor for the mock ADS1115
        """
        self.i2c = i2c
        self.gain = gain
