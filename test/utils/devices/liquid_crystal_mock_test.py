"""
The file to test the mock liquid crystal display
"""

from AlkalinityTitrator.titration.utils.devices import board_mock as board
from AlkalinityTitrator.titration.utils.devices.liquid_crystal_mock import LiquidCrystal
from AlkalinityTitrator.titration.utils import constants


def create_lcd(cols=constants.LCD_WIDTH, rows=constants.LCD_HEIGHT):
    """
    The function to create a mock LCD for testing
    """

    liquid_crystal = LiquidCrystal(
        r_s=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d_four=board.D18,
        d_five=board.D23,
        d_six=board.D24,
        d_seven=board.D25,
        cols=cols,
        rows=rows,
    )

    return liquid_crystal


def test_lcd_create():
    """
    The function to test initializing the mock LCD
    """

    liquid_crystal = create_lcd()

    assert liquid_crystal is not None
    assert liquid_crystal.cols == 20
    assert liquid_crystal.rows == 4


def test_lcd_create_null():
    """
    The function to test creating a mock null LCD for testing
    """
    liquid_crystal = LiquidCrystal(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        constants.LCD_WIDTH,
        constants.LCD_HEIGHT,
    )
    assert liquid_crystal is not None
    assert liquid_crystal.cols == 20
    assert liquid_crystal.rows == 4


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


def test_lcd_init_null_out(capsys):
    """
    The function to test startup of a null mock LCD
    """
    LiquidCrystal(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        constants.LCD_WIDTH,
        constants.LCD_HEIGHT,
    )

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


def test_lcd_init_small_null_out(capsys):
    """
    The function to test startup of a small null mock LCD
    """
    liquid_crystal = LiquidCrystal(None, None, None, None, None, None, None, 10, 2)

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

    liquid_crystal.print("test string 1", 1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|test string 3       |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, 1)
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

    liquid_crystal.print("test string 1", 1, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|   test string 3    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, 2)
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

    liquid_crystal.print("test string 1", 1, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|       test string 1|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 1 (2)", 1, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 2", 2, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 3", 3, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|       test string 3|\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    liquid_crystal.print("test string 4", 4, 3)
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

    liquid_crystal.print("test string that's too long", 1, 1)
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
    The function to test a mock LCD clear call
    """
    liquid_crystal = create_lcd()

    liquid_crystal.print("test string", 1, 1)
    liquid_crystal.print("test string", 2, 1)
    liquid_crystal.print("test string", 3, 1)

    _ = capsys.readouterr()

    liquid_crystal.print("test string", 4, 1)

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
