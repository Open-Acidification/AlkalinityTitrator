"""
The file to test the pH probe
"""
import pytest

from titration.devices.library import board, ADS
from titration.devices.ph_probe import PHProbe


def create_ph_probe():
    """
    The function to create a pH probe for testing
    """
    return PHProbe()


def test_ph_create():
    """
    The function to test creating a pH probe
    """
    ph_test = create_ph_probe()

    assert ph_test.i2c.scl == board.SCL
    assert ph_test.i2c.sda == board.SDA
    assert ph_test.ads.i2c == ph_test.i2c
    assert ph_test.channel.ads == ph_test.ads
    assert ph_test.channel.p_0 == ADS.P0
    assert ph_test.channel.p_1 == ADS.P1
    assert ph_test.ads.gain == 1
    assert ph_test.channel.voltage == 0


def test_ph_get_voltage():
    """
    The function to test setting the pH voltage
    """
    ph_test = create_ph_probe()
    ph_test.channel.voltage = 3.0

    assert ph_test.get_voltage() == 3.0


def test_ph_set_gain():
    """
    The function to test setting the pH gain
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
    The function to test getting the pH gain
    """
    ph_test = create_ph_probe()
    ph_test.ads.gain = 8

    assert ph_test.get_gain() == 8
