"""
The file to test the mock temperature sensor
"""

from titration.devices.library import TemperatureProbe


def create_temperature_probe():
    """
    The function to create a mock temperature sensor
    """
    return TemperatureProbe()


def test_temperature_probe_create():
    """
    The function to test creating a mock temperature sensor
    """
    temperature_sensor = create_temperature_probe()
    assert temperature_sensor is not None


def test_temperature_probe_create_null():
    """
    The function to test creating a null mock temperature sensor
    """
    temperature_sensor = TemperatureProbe(None, None, None, None)
    assert temperature_sensor is not None


def test_temperature_probe_get_temperature():
    """
    The function to test getting a temperature from the mock sensor
    """
    temperature_sensor = create_temperature_probe()
    assert temperature_sensor.get_temperature() == 0


def test_temperature_probe_temperature_null():
    """
    The function to test getting a temperature from a null mock sensor
    """
    temperature_sensor = TemperatureProbe(None, None, None, None)
    assert temperature_sensor.get_temperature() == 0


def test_temperature_probe_resistance():
    """
    The function to test getting a resistance from a mock sensor
    """
    temperature_sensor = create_temperature_probe()
    assert temperature_sensor.get_resistance() == 1000.0


def test_temperature_probe_resistance_null():
    """
    The function to test getting a resistance from a null mock sensor
    """
    temperature_sensor = TemperatureProbe(None, None, None, None)
    assert temperature_sensor.get_resistance() == 1000.0
