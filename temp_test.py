import time

import board
import busio
import digitalio
import adafruit_max31865

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
temp_sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=1000.0, ref_resistor=4300.0)

while True:
    temp = temp_sensor.temperature
    print("Temperature: {0:0.3f}C".format(temp))
    time.sleep(1)
