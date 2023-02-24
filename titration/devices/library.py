"""
The file to configure mock objects
"""

# pylint: disable=unused-import, ungrouped-imports, wrong-import-position
# mypy: disable-error-code= no-redef, assignment

from titration import constants

if constants.IS_TEST:
    from titration.devices import ads_mock as ADS
    from titration.devices import analog_mock as analog_in
    from titration.devices import board_mock as board
    from titration.devices import i2c_mock as busio
    from titration.devices import pwm_out_mock as pwmio
    from titration.devices.digital_mock import DigitalInOut
    from titration.devices.keypad_mock import Keypad
    from titration.devices.led_mock import LED
    from titration.devices.liquid_crystal_mock import LiquidCrystal
    from titration.devices.max31865_mock import MAX31865
    from titration.devices.serial_mock import Serial
    from titration.devices.spi_mock import SPI
else:
    import adafruit_ads1x15.ads1115 as ADS
    import board
    import busio
    import pwmio
    from adafruit_ads1x15 import analog_in
    from adafruit_max31865 import MAX31865
    from busio import SPI
    from digitalio import DigitalInOut
    from gpiozero import LED
    from serial import Serial

    from titration.devices.keypad import Keypad
    from titration.devices.liquid_crystal import LiquidCrystal

from titration.devices.ph_probe import PHProbe
from titration.devices.stir_control import StirControl
from titration.devices.syringe_pump import SyringePump
from titration.devices.temperature_control import TemperatureControl
from titration.devices.temperature_probe import TemperatureProbe
