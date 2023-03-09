"""
The file for the temperature probe device
"""

# pylint: disable = too-many-arguments

from titration import constants
from titration.devices.library import MAX31865, SPI, DigitalInOut, board


class TemperatureProbe:
    """
    The class for the temperature probe device
    """

    def __init__(self):
        """
        The constructor for the TemperatureProbe class
        """
        self.spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.c_s = DigitalInOut(board.D4)
        self.sensor = MAX31865(
            self.spi,
            self.c_s,
            wires=3,
            rtd_nominal=constants.TEMPERATURE_NOMINAL_RESISTANCE,
            ref_resistor=constants.TEMPERATURE_REF_RESISTANCE,
        )

    def get_temperature(self):
        """
        The function to get the probe's temperature
        """
        return self.sensor.temperature

    def get_resistance(self):
        """
        The function to get the probe's resistance
        """
        return self.sensor.resistance

    def read_temperature(self):
        """
        The function that reads and returns the temperature from GPIO
        """
        return self.get_temperature(), self.get_resistance()
