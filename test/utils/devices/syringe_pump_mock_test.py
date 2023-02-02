"""
Module to test mock syringe pump
"""

from titration.utils import constants, interfaces
from titration.utils.devices import syringe_pump_mock as syringe


def setup_module():
    """
    Function to setup syringe test module
    """
    constants.IS_TEST = True
    interfaces.setup_module_classes()


def test_syringe_mock_create():
    """
    Function to test creating mock syringe
    """
    pump = syringe.Syringe_Pump()
    assert pump is not None
    assert pump.volume_in_pump == constants.volume_in_pump
    assert pump.max_pump_capacity == constants.MAX_PUMP_CAPACITY
    assert pump.serial is not None


def test_syringe_mock_pump_volume_out_less_than(capsys):
    """
    Function to test mock syringe pump volume out less than
    """
    pump = syringe.Syringe_Pump()
    interfaces.lcd.mock_disable_clear()
    pump.set_volume_in_pump(1.0)
    _ = capsys.readouterr()
    pump.pump_volume(0.5, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pumping 0.50 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.50 ml   |\n"
        + "*====================*\n"
    )


def test_syringe_mock_pump_volume_out_greater_than_current(capsys):
    """
    Function to test mock syringe pump volume out greater than
    """
    pump = syringe.Syringe_Pump()
    interfaces.lcd.mock_disable_clear()
    pump.set_volume_in_pump(0.5)
    _ = capsys.readouterr()
    pump.pump_volume(1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pumping 0.50 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.00 ml   |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Filling 0.50 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.50 ml   |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pumping 0.50 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.00 ml   |\n"
        + "*====================*\n"
    )


def test_syringe_mock_pump_volume_out_greater_than_max(capsys):
    """
    Function to test mock syringe pump volume out greater than max
    """
    pump = syringe.Syringe_Pump()
    interfaces.lcd.mock_disable_clear()
    pump.set_volume_in_pump(1.0)
    _ = capsys.readouterr()
    pump.pump_volume(2, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "| Volume > pumpable  |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pumping 1.00 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.00 ml   |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Filling 1.00 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 1.00 ml   |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pumping 1.00 ml     |\n"
        + "*====================*\n"
        + "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.00 ml   |\n"
        + "*====================*\n"
    )
