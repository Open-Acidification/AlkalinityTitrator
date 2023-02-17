"""
The file to test the mock temperature sensor
"""
from titration.devices import board_mock as board_class
from titration.devices.temperature_probe_mock import TemperatureProbe


def create_temperature_probe():
    """
    The function to create a mock temperature sensor
    """
    return TemperatureProbe(
        board_class.SCK, board_class.MOSI, board_class.MISO, board_class.D4, wires=2
    )


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


def test_temperature_probe_set_temperature():
    """
    The function to test setting the temperature for the mock sensor
    """
    temperature_sensor = create_temperature_probe()
    temperature_sensor.mock_set_temperature(25)
    assert temperature_sensor.get_temperature()


def test_temperature_probe_set_resistance():
    """
    The function to test setting the resistance for the mock sensor
    """
    temperature_sensor = create_temperature_probe()
    temperature_sensor.mock_set_resistance(500)
    assert temperature_sensor.get_resistance() == 500
