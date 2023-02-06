"""
Module to test mock syringe pump
"""

from titration.utils import constants
from titration.utils.devices.syringe_pump_mock import Syringe_Pump


def create_test_syringe():
    """
    The function to create a mock test syringe
    """
    return Syringe_Pump()


def test_syringe_mock_create():
    """
    Function to test creating mock syringe
    """
    pump = create_test_syringe()
    assert pump is not None
    assert pump.volume_in_pump == constants.volume_in_pump
    assert pump.max_pump_capacity == constants.MAX_PUMP_CAPACITY
    assert pump.serial is not None


def test_syringe_mock_pump_volume_out_less_than():
    """
    Function to test mock syringe pump volume out less than
    """
    pump = create_test_syringe()


def test_syringe_mock_pump_volume_out_greater_than_current():
    """
    Function to test mock syringe pump volume out greater than
    """
    pump = create_test_syringe()


def test_syringe_mock_pump_volume_out_greater_than_max():
    """
    Function to test mock syringe pump volume out greater than max
    """
    pump = create_test_syringe()
