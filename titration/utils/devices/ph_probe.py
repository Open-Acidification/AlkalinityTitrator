import adafruit_ads1x15.ads1115 as ADS  # pH
import adafruit_ads1x15.analog_in as analog_in  # pH
import busio  # pH


class pH_Probe:
    def __init__(self, scl, sda, gain=1):
        self.i2c = busio.I2C(scl, sda)
        self.ads = ADS.ADS1115(self.i2c)
        self.channel = analog_in.AnalogIn(self.ads, ADS.P0, ADS.P1)
        self.ads.gain = gain

        self.gain_options = [2 / 3, 1, 2, 4, 8, 16]

    def voltage(self):
        return self.channel.voltage

    def set_gain(self, gain):
        if gain not in self.gain_options:
            raise ValueError("Gain must be one of: {}".format(self.gain_options))
        else:
            self.ads.gain = gain

    def get_gain(self):
        return self.ads.gain

    def read_raw_pH(self):
        # Read pH registers; pH_val is raw value from pH probe
        volts = self.voltage()
        return volts
