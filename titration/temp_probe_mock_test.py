import pytest
import temp_probe_mock
import board_mock

def test_temp_probe_create():
    temp_sensor = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    assert temp_sensor != None

def test_temp_probe_create_none():
    temp_sensor = temp_probe_mock.Temp_Probe(None, None, None, None)
    assert temp_sensor != None

def test_temp_probe_temperature():
    temp_sensor_1 = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    temp_sensor_2 = temp_probe_mock.Temp_Probe(None, None, None, None)

    assert temp_sensor_1.temperature() == 0
    assert temp_sensor_2.temperature() == 0

def test_temp_probe_resistance():
    temp_sensor_1 = temp_probe_mock.Temp_Probe(board_mock.SCK, board_mock.MOSI, board_mock.MISO, board_mock.D4, wires=2)
    temp_sensor_2 = temp_probe_mock.Temp_Probe(None, None, None, None)

    assert temp_sensor_1.resistance() == 1000.0
    assert temp_sensor_2.resistance() == 1000.0