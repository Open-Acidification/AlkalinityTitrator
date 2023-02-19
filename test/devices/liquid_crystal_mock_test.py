"""
The file to test the mock liquid crystal display
"""

import digitalio

from titration import constants
from titration.devices.library import board, LiquidCrystal


def create_lcd(cols=constants.LCD_WIDTH, rows=constants.LCD_HEIGHT):
    """
    The function to create a mock LCD for testing
    """

    return LiquidCrystal(cols, rows)


def test_lcd_create():
    """
    The function to test initializing the mock LCD
    """

    liquid_crystal = create_lcd()

    assert liquid_crystal.pin_rs == board.D27
    assert liquid_crystal.pin_on == board.D15
    assert liquid_crystal.pin_e == board.D22
    assert liquid_crystal.pin_d4 == board.D18
    assert liquid_crystal.pin_d5 == board.D23
    assert liquid_crystal.pin_d6 == board.D24
    assert liquid_crystal.pin_d7 == board.D25

    assert liquid_crystal.pin_rs.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_e.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_d4.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_d5.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_d6.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_d7.direction == digitalio.Direction.OUTPUT
    assert liquid_crystal.pin_on.direction == digitalio.Direction.OUTPUT

    assert liquid_crystal.pin_on.value is True

    assert liquid_crystal.cols == 20
    assert liquid_crystal.rows == 4

    assert liquid_crystal.clear_flag is True
    assert liquid_crystal.strings == [
        "".ljust(liquid_crystal.cols),
        "".ljust(liquid_crystal.cols),
        "".ljust(liquid_crystal.cols),
        "".ljust(liquid_crystal.cols),
    ]


def test_lcd_init_out(capsys):
    """
    The function to test the startup of a large mock LCD
    """
    create_lcd()

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_lcd_init_small_out(capsys):
    """
    The function to test startup of a small mock LCD
    """
    liquid_crystal = create_lcd(10, 2)

    captured = capsys.readouterr()
    assert captured.out == (
        "*==========*\n" + "|          |\n" + "|          |\n" + "*==========*\n"
    )

    assert liquid_crystal.cols == 10
    assert liquid_crystal.rows == 2


def test_lcd_print_left(capsys):
    """
    The function to test mock LCD printing from the left
    """
    liquid_crystal = create_lcd()

    _ = capsys.readouterr()

    liquid_crystal.print("test string 1", 1, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|test string 3       |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|test string 3       |\n"
        + "|test string 4       |\n"
        + "*====================*\n"
    )


def test_lcd_print_center(capsys):
    """
    The function to test mock LCD printing from the center
    """
    liquid_crystal = create_lcd()

    _ = capsys.readouterr()

    liquid_crystal.print("test string 1", 1, "center")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, "center")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, "center")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, "center")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|   test string 3    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, "center")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|   test string 3    |\n"
        + "|   test string 4    |\n"
        + "*====================*\n"
    )


def test_lcd_print_right(capsys):
    """
    The function to test mock LCD printing from the right
    """
    liquid_crystal = create_lcd()

    _ = capsys.readouterr()

    liquid_crystal.print("test string 1", 1, "right")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|       test string 1|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, "right")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, "right")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, "right")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|       test string 3|\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, "right")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|       test string 3|\n"
        + "|       test string 4|\n"
        + "*====================*\n"
    )


def test_lcd_print_long(capsys):
    """
    The function to test mock LCD when a print call is too long
    """
    liquid_crystal = create_lcd()

    _ = capsys.readouterr()

    liquid_crystal.print("test string that's too long", 1, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string that's t|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_lcd_clear(capsys):
    """
    The function to test a mock LCD clear
    """
    liquid_crystal = create_lcd()

    liquid_crystal.print("test string", 1, "left")
    liquid_crystal.print("test string", 2, "left")
    liquid_crystal.print("test string", 3, "left")

    _ = capsys.readouterr()

    liquid_crystal.print("test string", 4, "left")

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string         |\n"
        + "|test string         |\n"
        + "|test string         |\n"
        + "|test string         |\n"
        + "*====================*\n"
    )

    liquid_crystal.clear()
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.clear()
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_lcd_backlight(capsys):
    """
    The function to test the mock LCD lcd_backlight function
    """
    liquid_crystal = create_lcd()

    _ = capsys.readouterr()

    assert liquid_crystal.pin_on.value is True

    liquid_crystal.lcd_backlight(False)

    assert liquid_crystal.pin_on.value is False

    liquid_crystal.print("test string", 1, "left")
    captured = capsys.readouterr()
    assert captured.out == ""

    liquid_crystal.lcd_backlight(True)

    assert liquid_crystal.pin_on.value is True

    liquid_crystal.print("test string", 1, "left")
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string         |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_mock_disable_clear():
    """
    The function to test the LCD mock_disable_clear function
    """
    liquid_crystal = create_lcd()

    assert liquid_crystal.clear_flag is True

    liquid_crystal.mock_disable_clear()

    assert liquid_crystal.clear_flag is False
