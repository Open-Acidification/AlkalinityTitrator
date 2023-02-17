"""
The file to configure mock objects
"""
from titration import constants

if constants.IS_TEST:
    from titration.devices import ads_mock as ADS
    from titration.devices import analog_mock as analog_in
    from titration.devices import board_mock as board
    from titration.devices import i2c_mock as busio
    from titration.devices.liquid_crystal_mock import LiquidCrystal
    from titration.devices.keypad_mock import Keypad
    from titration.devices import pwm_out_mock as pwmio
    from titration.devices.serial_mock import Serial
else:
    import adafruit_ads1x15.ads1115 as ADS  # type: ignore
    import adafruit_ads1x15.analog_in as analog_in  # type: ignore
    import busio  # type: ignore
    import board  # type: ignore
    from titration.devices.liquid_crystal import LiquidCrystal  # type: ignore
    from titration.devices.keypad import Keypad  # type: ignore
    import pwmio  # type: ignore
    from serial import Serial  # type: ignore
