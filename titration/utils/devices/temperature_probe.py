"""
The class for the TemperatureProbe
"""

# pylint: disable = invalid-name, too-many-arguments

from titration.utils import constants

if constants.IS_TEST:
    from titration.utils.devices.digital_mock import DigitalInOut
    from titration.utils.devices.max31865_mock import MAX31865
    from titration.utils.devices.spi_mock import SPI
else:
    from digitalio import DigitalInOut
    from adafruit_max31865 import MAX31865
    from busio import SPI


class TemperatureProbe:
    """
    The class for the temperature probe device
    """

    def __init__(self, sck, mosi, miso, cs, wires=2):
        """
        The constructor for the TemperatureProbe class
        """
        self.spi = SPI(sck, MOSI=mosi, MISO=miso)
        self.cs = DigitalInOut(cs)
        self.sensor = MAX31865(
            self.spi,
            self.cs,
            wires=wires,
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
