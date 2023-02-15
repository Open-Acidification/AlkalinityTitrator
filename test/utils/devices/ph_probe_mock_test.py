"""
The file to test the mock pH probe
"""
import pytest
from AlkalinityTitrator.titration.utils.devices import board_mock as board_class
from AlkalinityTitrator.titration.utils.devices.ph_probe_mock import PhProbe


def create_ph_probe(pin_one=board_class.SCL, pin_two=board_class.SDA):
    """
    The function to create a mock pH probe
    """
    return PhProbe(pin_one, pin_two)


def test_ph_create():
    """
    The function to test creating a mock pH probe
    """
    ph_test = create_ph_probe()
    assert ph_test is not None


def test_ph_create_null():
    """
    The function to test creating a null mock pH probe
    """
    ph_test = create_ph_probe(None, None)
    assert ph_test is not None


def test_ph_voltage():
    """
    The function to test mock pH voltage
    """
    ph_test = create_ph_probe()
    assert ph_test.voltage() == 0


def test_ph_voltage_null():
    """
    The function to test null mock pH voltage
    """
    ph_test = create_ph_probe(None, None)
    assert ph_test.voltage() == 0


def test_ph_voltage_set():
    """
    The function to test setting the mock pH voltage
    """
    ph_test = create_ph_probe()
    ph_test.mock_set_voltage(3.0)
    assert ph_test.voltage() == 3.0


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
