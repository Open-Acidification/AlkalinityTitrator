"""
<<<<<<< HEAD
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
=======
The file for the PHProbe class
"""
from titration.utils import constants

if constants.IS_TEST:
    from titration.utils.devices import board_mock as board
    from titration.utils.devices import i2c_mock as busio
    from titration.utils.devices import ads_mock as ADS
    from titration.utils.devices import analog_mock as analog_in
else:
    import adafruit_ads1x15.ads1115 as ADS  # type: ignore
    import adafruit_ads1x15.analog_in as analog_in  # type: ignore
    import busio  # type: ignore
    import board  # type: ignore


class PHProbe:
    """
    The class for the pH Probe device
    """

    def __init__(self, gain=1):
        """
        The constructor for the PHProbe class
        Initializes I2C pins, gain, and voltage

        Parameters:
            gain (float): gain of the PHProbe
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
>>>>>>> main
        self.ads = ADS.ADS1115(self.i2c)
        self.channel = analog_in.AnalogIn(self.ads, ADS.P0, ADS.P1)

        self.ads.gain = gain
        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

<<<<<<< HEAD
    def voltage(self):
        """
        The function to return the pH Probe voltage
=======
    def get_voltage(self):
        """
        The function to return the pH probe's voltage
>>>>>>> main
        """
        return self.channel.voltage

    def set_gain(self, gain):
        """
<<<<<<< HEAD
        The function to set the pH Probe's gain
=======
        The function to set the pH probe's gain

        Parameters:
            gain (int): the gain of the PHProbe
>>>>>>> main
        """
        if gain not in self.gain_options:
            raise ValueError(f"Gain must be one of: {self.gain_options}")
        self.ads.gain = gain

    def get_gain(self):
        """
<<<<<<< HEAD
        The function to return the pH Probe's gain
=======
        The function to return the pH probe's gain
>>>>>>> main
        """
        return self.ads.gain
