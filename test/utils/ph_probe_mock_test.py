import pytest

import titration.utils.devices.board_mock as board_mock
import titration.utils.devices.ph_probe_mock as ph_probe_mock


def test_ph_create():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    assert ph is not None


def test_ph_create_null():
    ph = ph_probe_mock.pH_Probe(None, None)
    assert ph is not None


def test_ph_voltage():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    assert ph.voltage() == 0


def test_ph_voltage_null():
    ph = ph_probe_mock.pH_Probe(None, None)
    assert ph.voltage() == 0


def test_ph_voltage_set():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    ph.mock_set_voltage(3.0)
    assert ph.voltage() == 3.0


def test_ph_set_gain():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    gain_options = [2 / 3, 1, 2, 4, 8, 16]

    for gain in gain_options:
        ph.set_gain(gain)
        assert ph.get_gain() == gain

    with pytest.raises(ValueError):
        ph.set_gain(0)

    with pytest.raises(ValueError):
        ph.set_gain(32)
