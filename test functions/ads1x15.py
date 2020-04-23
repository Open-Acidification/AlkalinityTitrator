import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Start i2c bus
i2c = busio.I2C(board.SCL, board.SDA)

# Gain arg          Range (V)
# ---------------------------
#   2/3             +/- 6.144
#   1               +/- 4.096


adc = ADS.ads1015(i2c, data_rate=920, gain=2)
chan = AnalogIn(adc, ADS.P0, ADS.P1)

print("Ctrl-C to quit Continuous Test")
temp = 0
go = 1

while go:
    temp = temp + 1

    volts = chan.voltage
    diff = volts / 9.7
    volts = volts / 10
    percent_diff = (diff - volts)/volts*100
    print("Ideal: {}\tActual: {}\tPercDiff: {}".format(volts, diff, percent_diff))

    if (temp == 10):
        print("----------------------------------")
        time.sleep(1)
        temp = 0
