import temp_probe_mock
import board_mock

def test_temp_probe_create():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    assert temp_sensor != None

def test_temp_probe_create_null():
    temp_sensor = temp_probe_mock.Temp_Probe(None, None, None, None)
    assert temp_sensor != None

def test_temp_probe_temperature():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    assert temp_sensor.temperature() == 0

def test_temp_probe_temperature_null():
    temp_sensor = temp_probe_mock.Temp_Probe(None, None, None, None)
    assert temp_sensor.temperature() == 0

def test_temp_probe_resistance():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    assert temp_sensor.resistance() == 1000.0

def test_temp_probe_resistance_null():
    temp_sensor = temp_probe_mock.Temp_Probe(None, None, None, None)
    assert temp_sensor.resistance() == 1000.0

def test_temp_probe_set_temperature():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    temp_sensor.mock_set_temperature(25)
    assert temp_sensor.temperature()

def test_temp_probe_resistance():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    temp_sensor.mock_set_resistance(500)
    assert temp_sensor.resistance() == 500
