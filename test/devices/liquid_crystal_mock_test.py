"""
The file to test the mock liquid crystal display for the GUI
"""

from titration import constants
from titration.devices.liquid_crystal_mock import LiquidCrystal


def create_lcd(cols=constants.LCD_WIDTH, rows=constants.LCD_HEIGHT):
    """
    The function to create a mock LCD for testing
    """
    return LiquidCrystal(cols, rows)


def test_lcd_create():
    """
    The function to test creating a GUI LCD
    """

    liquid_crystal = create_lcd()

    assert liquid_crystal.cols == constants.LCD_WIDTH
    assert liquid_crystal.rows == constants.LCD_HEIGHT

    assert liquid_crystal.lcd_lines[0] is None
    assert liquid_crystal.lcd_lines[1] is None
    assert liquid_crystal.lcd_lines[2] is None
    assert liquid_crystal.lcd_lines[3] is None


def test_print():
    """
    The function to test the printing to the GUI
    """

    liquid_crystal = create_lcd()

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

    liquid_crystal = create_lcd()

    liquid_crystal.lcd_lines[0] = "TEST1"
    liquid_crystal.lcd_lines[1] = "TEST2"
    liquid_crystal.lcd_lines[2] = "TEST3"
    liquid_crystal.lcd_lines[3] = "TEST4"

    assert liquid_crystal.get_line(1) == "TEST1"
    assert liquid_crystal.get_line(2) == "TEST2"
    assert liquid_crystal.get_line(3) == "TEST3"
    assert liquid_crystal.get_line(4) == "TEST4"
    assert liquid_crystal.get_line(5) == "ERROR"
