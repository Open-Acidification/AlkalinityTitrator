"""
The file to test the mock syringe
"""
from titration.utils import constants
from titration.utils.devices.syringe_pump_mock import SyringePump


def create_test_syringe():
    """
    The function to create a mock test syringe
    """
    return SyringePump()


def test_syringe_mock_create():
    """
    The function to test creating mock syringe
    """
    pump = create_test_syringe()
    assert pump is not None
    assert pump.volume_in_pump == constants.VOLUME_IN_PUMP
    assert pump.max_pump_capacity == constants.MAX_PUMP_CAPACITY
    assert pump.serial is not None
