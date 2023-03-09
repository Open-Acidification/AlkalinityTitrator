"""
The file to test the mock temperature sensor
"""

from titration.devices.library import TemperatureProbe


def test_init():
    """
    The function to test creating a mock temperature sensor
    """
    temperature_probe = TemperatureProbe()

    assert temperature_probe is not None
    assert temperature_probe.reference_resistance == 4300.0


def test_get_temperature():
    """
    The function to test getting a temperature from the mock sensor
    """
    temperature_probe = TemperatureProbe()

    assert temperature_probe.get_temperature() == 0


def test_get_resistance():
    """
    The function to test getting a resistance from a mock sensor
    """
    temperature_probe = TemperatureProbe()

    assert temperature_probe.get_resistance() == 1000.0


def test_calibrate_above_zero():
    """
    The function to test calibrating the temperature probe when temperature is above 0 C
    """
    temperature_probe = TemperatureProbe()

    temperature_probe.calibrate(20)

    assert temperature_probe.reference_resistance == 4610.8904545989235


def test_calibrate_below_zero():
    """
    The function to test calibrating the temperature probe when temperature is below 0 C
    """
    temperature_probe = TemperatureProbe()

    temperature_probe.calibrate(-10)

    assert temperature_probe.reference_resistance == 4124.8364597466525


def test_calibrate_zero():
    """
    The function to test calibrating the temperature probe when temperature is 0 C
    """
    temperature_probe = TemperatureProbe()

    temperature_probe.calibrate(0)

    assert temperature_probe.reference_resistance == 4300.0
