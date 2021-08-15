import src.devices.board_mock as board_mock
import src.devices.temperature_probe_mock as temperature_probe_mock


def test_temperature_probe_create():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(
        board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2
    )
    assert temperature_sensor is not None


def test_temperature_probe_create_null():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(None, None, None, None)
    assert temperature_sensor is not None


def test_temperature_probe_get_temperature():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(
        board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2
    )
    assert temperature_sensor.get_temperature() == 0


def test_temperature_probe_temperature_null():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(None, None, None, None)
    assert temperature_sensor.get_temperature() == 0


def test_temperature_probe_resistance():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(
        board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2
    )
    assert temperature_sensor.get_resistance() == 1000.0


def test_temperature_probe_resistance_null():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(None, None, None, None)
    assert temperature_sensor.get_resistance() == 1000.0


def test_temperature_probe_set_temperature():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(
        board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2
    )
    temperature_sensor.mock_set_temperature(25)
    assert temperature_sensor.get_temperature()


def test_temperature_probe_set_resistance():
    temperature_sensor = temperature_probe_mock.Temperature_Probe(
        board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2
    )
    temperature_sensor.mock_set_resistance(500)
    assert temperature_sensor.get_resistance() == 500
