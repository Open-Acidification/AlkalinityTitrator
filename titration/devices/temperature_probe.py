"""
The file for the temperature probe device
"""
import adafruit_max31865
import busio
import digitalio

from titration import constants


class TemperatureProbe:
    """
    The class for the Temperature Probe device
    """

    def __init__(self, sck, mosi, miso, c_s, wires=2):
        """
        The constructor for the Temperature Probe
        """
        self.spi = busio.SPI(sck, MOSI=mosi, MISO=miso)
        self.c_s = digitalio.DigitalInOut(c_s)
        self.sensor = adafruit_max31865.MAX31865(
            self.spi,
            self.c_s,
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
        Reads and returns the temperature from GPIO
        :returns: temperature in celsius, resistance in ohms
        """
        return self.get_temperature(), self.get_resistance()
