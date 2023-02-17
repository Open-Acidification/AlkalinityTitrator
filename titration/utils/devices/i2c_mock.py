"""
The file for the I2C mock class
"""


class I2C:
    """
    The class for the mock I2C peripheral
    """

    def __init__(self, scl, sda):
        """
        The constructor for the mock I2C class
        """
        self.scl = scl
        self.sda = sda
