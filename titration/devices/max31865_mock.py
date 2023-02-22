"""
The file to mock the MAX31865 class
"""

# pylint: disable = invalid-name, too-many-arguments, too-few-public-methods


class MAX31865:
    """
    The class for the mock MAX31865 class
    """

    def __init__(self, spi, cs, wires, rtd_nominal, ref_resistor):
        """
        The constructor for the MAX31865
        """
        self.spi = spi
        self.cs = cs
        self.wires = wires
        self.rtd_nominal = rtd_nominal
        self.ref_resistor = ref_resistor
        self.temperature = 0
        self.resistance = 1000
