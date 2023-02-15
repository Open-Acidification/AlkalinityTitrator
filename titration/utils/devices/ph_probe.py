"""
The file for the pH Probe device
"""

# pylint: disable = E0401

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15 import analog_in
import busio


class PhProbe:
    """
    The file for the pH Probe device
    """

    def __init__(self, scl, sda, gain=1):
        """
        The constructor for the PhProbe class
        """
        self.i2c = busio.I2C(scl, sda)
        self.ads = ADS.ADS1115(self.i2c)
        self.channel = analog_in.AnalogIn(self.ads, ADS.P0, ADS.P1)
        self.ads.gain = gain

        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

    def voltage(self):
        """
        The function to return the pH Probe voltage
        """
        return self.channel.voltage

    def set_gain(self, gain):
        """
        The function to set the pH Probe's gain
        """
        if gain not in self.gain_options:
            raise ValueError(f"Gain must be one of: {self.gain_options}")
        self.ads.gain = gain

    def get_gain(self):
        """
        The function to return the pH Probe's gain
        """
        return self.ads.gain
