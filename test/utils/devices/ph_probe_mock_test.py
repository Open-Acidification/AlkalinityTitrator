"""
The file to test the mock pH probe
"""
import pytest
from titration.utils.devices import board_mock
from titration.utils.devices.ph_probe_mock import pH_Probe


def create_ph_probe(pin_one=board_mock.SCL, pin_two=board_mock.SDA):
    """
    The function to create a mock pH probe for testing
    """
    return pH_Probe(pin_one, pin_two)


def test_ph_create():
    """
    The function to test creating a mock pH probe
    """
    ph_test = create_ph_probe()

    assert ph_test.i2c == (board_mock.SCL, board_mock.SDA)
    assert ph_test.ads == ph_test.i2c
    assert ph_test.channel == (ph_test.ads, "ADS.P0", "ADS.P1")
    assert ph_test.gain == 1
    assert ph_test.volt == 0
    assert ph_test is not None


def test_ph_create_null():
    """
    The function to test creating a null mock pH probe
    """
    ph_test = create_ph_probe(None, None)

    assert ph_test.volt == 0
    assert ph_test is not None


def test_ph_get_voltage():
    """
    The function to test setting the mock pH voltage
    """
    ph_test = create_ph_probe()
    ph_test.volt = 3.0

    assert ph_test.get_voltage() == 3.0


def test_ph_set_gain():
    """
    The function to test setting the mock pH gain
    """
    ph_test = create_ph_probe()
    gain_options = [2 / 3, 1, 2, 4, 8, 16]

    for gain in gain_options:
        ph_test.set_gain(gain)
        assert ph_test.get_gain() == gain

    with pytest.raises(ValueError):
        ph_test.set_gain(0)

    with pytest.raises(ValueError):
        ph_test.set_gain(32)


def test_ph_get_gain():
    """
    The function to test getting the mock pH gain
    """
    ph_test = create_ph_probe()
    ph_test.gain = 8

    assert ph_test.get_gain() == 8
