"""
The file to mock the SPI class
"""

# pylint: disable = invalid-name, too-few-public-methods


class SPI:
    """
    The mock SPI class
    """

    def __init__(self, sck, MOSI, MISO):
        """
        The constructor for the mock SPI class
        """
        self.sck = sck
        self.MOSI = MOSI
        self.MISO = MISO
