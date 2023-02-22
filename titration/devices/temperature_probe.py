"""
The file for the temperature probe device
"""

# pylint: disable = too-many-arguments

from titration.devices.library import MAX31865, SPI, DigitalInOut

TEMPERATURE_REF_RESISTANCE = 4300.0
TEMPERATURE_NOMINAL_RESISTANCE = 1000.0


class TemperatureProbe:
    """
    The class for the temperature probe device
    """

    def __init__(self, sck, mosi, miso, c_s, wires=2):
        """
        The constructor for the TemperatureProbe class
        """
        self.spi = SPI(sck, MOSI=mosi, MISO=miso)
        self.c_s = DigitalInOut(c_s)
        self.sensor = MAX31865(
            self.spi,
            self.c_s,
            wires=wires,
            rtd_nominal=TEMPERATURE_NOMINAL_RESISTANCE,
            ref_resistor=TEMPERATURE_REF_RESISTANCE,
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
