"""
The file to test the mock syringe pump
"""
from titration.utils import interfaces
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
    assert pump.max_pump_capacity == 1.1
    assert pump.serial is not None
    assert pump is not None


def test_syringe_mock_set_volume():
    """
    The function to test setting the mock syringe volume
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


def test_syringe_mock_pump_volume_out_less_than(capsys):
    """
    The function to test mock syringe pump volume out less than
    """
    pump = create_syringe_pump()
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
    The function to test mock syringe pump volume out greater than
    """
    pump = create_syringe_pump()
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
    The function to test mock syringe pump volume out greater than max
    """
    pump = create_syringe_pump()
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
