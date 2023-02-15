"""
The file for the ADS1115 mock class
"""

# pylint: disable = R0903

P0 = None
P1 = None
P2 = None
P3 = None


class ADS1115:
    """
    The mock class for the ADS1115
    """

    def __init__(self, i2c, gain=1):
        """
        The constructor for the ADS1115 class
        """
        self.i2c = i2c
        self.gain = gain
