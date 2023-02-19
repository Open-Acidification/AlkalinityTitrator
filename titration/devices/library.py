"""
The file to configure mock objects
"""

# pylint: disable=unused-import, ungrouped-imports

from titration import constants
from titration.devices.ph_probe import PHProbe
from titration.devices.stir_control import StirControl
from titration.devices.syringe_pump import SyringePump

if constants.IS_TEST:
    from titration.devices import ads_mock as ADS
    from titration.devices import analog_mock as analog_in
    from titration.devices import board_mock as board
    from titration.devices import i2c_mock as busio
    from titration.devices import pwm_out_mock as pwmio
    from titration.devices.keypad_mock import Keypad
    from titration.devices.library import LiquidCrystal
    from titration.devices.serial_mock import Serial
    from titration.devices.temperature_control_mock import TemperatureControl
    from titration.devices.temperature_probe_mock import TemperatureProbe
else:
    import adafruit_ads1x15.ads1115 as ADS  # type: ignore
    import board  # type: ignore
    import busio  # type: ignore
    import pwmio  # type: ignore
    from adafruit_ads1x15 import analog_in  # type: ignore
    from serial import Serial  # type: ignore

    from titration.devices.keypad import Keypad  # type: ignore
    from titration.devices.liquid_crystal import LiquidCrystal  # type: ignore
    from titration.devices.temperature_control_mock import TemperatureControl  # type: ignore
    from titration.devices.temperature_probe_mock import TemperatureProbe  # type: ignore
