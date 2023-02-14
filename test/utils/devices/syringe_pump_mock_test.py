"""
The file to test the mock syringe
"""
from titration.utils import constants
from titration.utils.devices.syringe_pump_mock import Syringe_Pump
from titration.utils.devices.liquid_crystal_mock import LiquidCrystal
from titration.utils.devices import board_mock as board_class


def create_lcd():
    """
    The function to create a lcd mock for the mock syringe tests
    """
    return LiquidCrystal(
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )


def test_syringe_mock_create():
    """
    The function to test creating mock syringe
    """
    pump = Syringe_Pump()
    assert pump is not None
    assert pump.volume_in_pump == constants.volume_in_pump
    assert pump.max_pump_capacity == constants.MAX_PUMP_CAPACITY
    assert pump.serial is not None


def test_syringe_mock_pump_volume_out_less_than(capsys):
    """
    The function to test mock syringe pump volume out less than
    """
    pump = Syringe_Pump()
    lcd = create_lcd()
    lcd.mock_disable_clear()
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
    The function to test mock syringe pump volume out greater than
    """
    pump = Syringe_Pump()
    lcd = create_lcd()
    lcd.mock_disable_clear()
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
    The function to test mock syringe pump volume out greater than max
    """
    pump = Syringe_Pump()
    lcd = create_lcd()
    lcd.mock_disable_clear()
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
