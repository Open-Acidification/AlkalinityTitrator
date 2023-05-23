"""
The file to test the mock temperature sensor
"""

from titration.devices.library import TemperatureProbe


def create_temperature_probe(probe_number):
    """
    The function to create a mock temperature sensor
    """
    return TemperatureProbe(probe_number)


def test_temperature_probe_one_create():
    """
    The function to test creating the first mock temperature probe
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor is not None


def test_temperature_probe_two_create():
    """
    The function to test creating the second mock temperature probe
    """
    temperature_sensor = create_temperature_probe(2)
    assert temperature_sensor is not None


def test_get_temperature():
    """
    The function to test getting a temperature from the mock sensor
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor.get_temperature() == 0


def test_get_resistance():
    """
    The function to test getting a resistance from a mock sensor
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor.get_resistance() == 100
