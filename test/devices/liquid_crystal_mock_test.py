"""
The file to test the mock liquid crystal display for the GUI
"""

from titration.devices.liquid_crystal_mock import LiquidCrystal


def test_lcd_create():
    """
    The function to test creating a GUI LCD
    """

    liquid_crystal = LiquidCrystal()

    assert liquid_crystal.cols == 20
    assert liquid_crystal.rows == 4

    assert liquid_crystal.lcd_lines[0] is None
    assert liquid_crystal.lcd_lines[1] is None
    assert liquid_crystal.lcd_lines[2] is None
    assert liquid_crystal.lcd_lines[3] is None


def test_print():
    """
    The function to test the printing to the GUI
    """

    liquid_crystal = LiquidCrystal()

    liquid_crystal.print("TEST1", 1)
    assert liquid_crystal.lcd_lines[0] == "TEST1"

    liquid_crystal.print("TEST2", 2)
    assert liquid_crystal.lcd_lines[1] == "TEST2"

    liquid_crystal.print("TEST3", 3)
    assert liquid_crystal.lcd_lines[2] == "TEST3"

    liquid_crystal.print("TEST4", 4)
    assert liquid_crystal.lcd_lines[3] == "TEST4"


def test_get_line():
    """
    The function to testing getting the message lines
    """

    liquid_crystal = LiquidCrystal()

    liquid_crystal.lcd_lines[0] = "TEST1"
    liquid_crystal.lcd_lines[1] = "TEST2"
    liquid_crystal.lcd_lines[2] = "TEST3"
    liquid_crystal.lcd_lines[3] = "TEST4"

    assert liquid_crystal.get_line(1) == "TEST1"
    assert liquid_crystal.get_line(2) == "TEST2"
    assert liquid_crystal.get_line(3) == "TEST3"
    assert liquid_crystal.get_line(4) == "TEST4"
    assert liquid_crystal.get_line(5) == "ERROR"
