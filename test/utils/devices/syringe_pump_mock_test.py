"""
The file to test the mock syringe pump
"""
import pytest
from titration.utils.devices.syringe_pump_mock import SyringePump


def create_syringe_pump():
    """
    The function to create a test mock syringe pump
    """
    return SyringePump()


def test_syringe_mock_create():
    """
    The function to test creating mock syringe
    """
    pump = create_syringe_pump()

    assert pump.volume_in_pump == 0
    assert pump.serial is not None
    assert pump is not None


def test_syringe_mock_set_volume_above_max():
    """
    The function to test setting the mock syringe volume
    """
    pump = create_syringe_pump()

    with pytest.raises(Exception) as exc_info:
        pump.set_volume_in_pump(1.11)

    assert exc_info.value.args == (
        "Set Volume Error: Volume set is higher than maximum capacity",
    )
    assert pump.volume_in_pump == 0


def test_syringe_mock_set_volume_negative():
    """
    The function to test setting the mock syringe volume below zero
    """
    pump = create_syringe_pump()

    with pytest.raises(Exception) as exc_info:
        pump.set_volume_in_pump(-1)

    assert exc_info.value.args == (
        "Set Volume Error: Volume set cannot be a negative value",
    )
    assert pump.volume_in_pump == 0


def test_syringe_mock_set_volume():
    """
    The function to test setting the mock syringe volume correctly
    """
    pump = create_syringe_pump()

    pump.set_volume_in_pump(0.5)

    assert pump.volume_in_pump == 0.5


def test_syringe_mock_get_volume():
    """
    The function to test getting the mock syringe volume
    """
    pump = create_syringe_pump()

    pump.volume_in_pump = 0.5

    assert pump.get_volume_in_pump() == 0.5


def test_pump_volume_in():
    """
    The function to test pulling liquid into the mock syringe
    """
    pump = create_syringe_pump()

    pump.pump_volume_in(0.5)

    assert pump.volume_in_pump == 0.5


def test_pump_volume_in_above_max():
    """
    The function to test pulling more liquid than the syringe can hold
    """
    pump = create_syringe_pump()

    pump.pump_volume_in(1.11)

    assert pump.volume_in_pump == 1.1


def test_pump_volume_in_negative():
    """
    The function to test pulling in negative liquid to the syringe
    """
    pump = create_syringe_pump()

    with pytest.raises(Exception) as exc_info:
        pump.pump_volume_in(-0.5)

    assert exc_info.value.args == ("can't convert negative int to unsigned",)
    assert pump.volume_in_pump == 0


def test_pump_volume_out_exact():
    """
    The function to test pumping a volume out of the syringe

    Testing line 107: volume is equal to the volume in the pump
    """
    pump = create_syringe_pump()

    pump.volume_in_pump = 0.5
    pump.pump_volume_out(0.5)

    assert pump.volume_in_pump == 0


def test_pump_volume_out_above_max_capacity():
    """
    The function to test pumping more than the max amount of volume the pump can hold

    Testing line 81: volume is greater than max pump capacity
    """
    pump = create_syringe_pump()

    pump.volume_in_pump = 1.1
    pump.pump_volume_out(1.11)

    assert pump.volume_in_pump == 0


def test_pump_volume_out_above_syringe_volume():
    """
    The function to test when pumping out more volume than what is currently in the syringe

    Testing line 98: volume to add is greater than volume in pump
    """
    pump = create_syringe_pump()

    pump.volume_in_pump = 0.5
    pump.pump_volume_out(0.75)

    assert pump.volume_in_pump == 0


def test_pump_volume_out_negative():
    """
    The function to test pumping out a negative amount of liquid
    """
    pump = create_syringe_pump()

    pump.volume_in_pump = 0.5

    with pytest.raises(Exception) as exc_info:
        pump.pump_volume_out(-0.5)

    assert exc_info.value.args == ("can't convert negative int to unsigned",)
    assert pump.volume_in_pump == 0.5
