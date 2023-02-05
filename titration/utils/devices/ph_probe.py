"""
The file for the pH_Probe class
"""
import adafruit_ads1x15.ads1115 as ADS
import adafruit_ads1x15.analog_in as analog_in
import busio


class pH_Probe:
    """
    The class for the pH Probe device
    """

    def __init__(self, scl, sda, gain=1):
        """
        The constructor for the pH_Probe class
        Initializes I2C pins, gain, and voltage
        """
        self.i2c = busio.I2C(scl, sda)
        self.ads = ADS.ADS1115(self.i2c)
        self.channel = analog_in.AnalogIn(self.ads, ADS.P0, ADS.P1)

        self.ads.gain = gain
        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

    def get_voltage(self):
        """
        The function to return the pH probe's voltage
        """
        return self.channel.voltage

    def set_gain(self, gain):
        """
        The function to set the pH probe's gain
        """
        if gain not in self.gain_options:
            raise ValueError("Gain must be one of: {}".format(self.gain_options))
        else:
            self.ads.gain = gain

    def get_gain(self):
        """
        The function to return the pH probe's gain
        """
        return self.ads.gain
