"""
Module to test mock pH probe
"""

import pytest

import titration.utils.devices.board_mock as board_mock
import titration.utils.devices.ph_probe_mock as ph_probe_mock

def test_ph_create():
    """
    Function to test creating a mock pH probe
    """
    ph_test = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    assert ph_test is not None


def test_ph_create_null():
    """
    Function to test creating a null mock pH probe
    """
    ph_test = ph_probe_mock.pH_Probe(None, None)
    assert ph_test is not None


def test_ph_voltage():
    """
    Function to test mock pH voltage
    """
    ph_test = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    assert ph_test.voltage() == 0


def test_ph_voltage_null():
    """
    Function to test null mock pH voltage
    """
    ph_test = ph_probe_mock.pH_Probe(None, None)
    assert ph_test.voltage() == 0


def test_ph_voltage_set():
    """
    Function to test setting the mock pH voltage
    """
    ph_test = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    ph_test.mock_set_voltage(3.0)
    assert ph_test.voltage() == 3.0


def test_ph_set_gain():
    """
    Function to test setting the mock pH gain
    """
    ph_test = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    gain_options = [2 / 3, 1, 2, 4, 8, 16]

    for gain in gain_options:
        ph_test.set_gain(gain)
        assert ph_test.get_gain() == gain

    with pytest.raises(ValueError):
        ph_test.set_gain(0)

    with pytest.raises(ValueError):
        ph_test.set_gain(32)
