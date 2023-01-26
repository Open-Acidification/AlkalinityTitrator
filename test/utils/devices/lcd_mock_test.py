"""
Module to create a mock LCD
"""

import titration.utils.devices.board_mock as board
from titration.utils.devices.lcd_mock import LiquidCrystal
from titration.utils import constants


def test_lcd_create():
    """
    Function to create a mock LCD for testing
    """
    # the mock LCD doesn't use it's inputs, real or None inputs should work
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )

    assert lcd is not None


def test_lcd_create_null():
    """
    Function to create a mock null LCD for testing
    """
    lcd = LiquidCrystal(
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
    assert lcd is not None


def test_lcd_begin_large(capsys):
    """
    Function to test startup of a large mock LCD
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
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

    assert lcd.cols == 20
    assert lcd.rows == 4


def test_lcd_begin_large_null(capsys):
    """
    Function to test startup of a large null mock LCD
    """
    lcd = LiquidCrystal(
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

    assert lcd.cols == 20
    assert lcd.rows == 4


def test_lcd_begin_small(capsys):
    """
    Function to test startup of a small mock LCD
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=10,
        rows=2,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        "*==========*\n" + "|          |\n" + "|          |\n" + "*==========*\n"
    )

    assert lcd.cols == 10
    assert lcd.rows == 2


def test_lcd_begin_small_null(capsys):
    """
    Function to test startup of a small null mock LCD
    """
    lcd = LiquidCrystal(None, None, None, None, None, None, None, 10, 2)

    captured = capsys.readouterr()
    assert captured.out == (
        "*==========*\n" + "|          |\n" + "|          |\n" + "*==========*\n"
    )

    assert lcd.cols == 10
    assert lcd.rows == 2


def test_lcd_print_left(capsys):
    """
    Function to test mock LCD printing from the left
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )

    # Flush the current stdout buffer from begin() output
    _ = capsys.readouterr()

    # print into the first line
    lcd.print("test string 1", 1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the first line again
    lcd.print("test string 1 (2)", 1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the second line
    lcd.print("test string 2", 2, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the third line
    lcd.print("test string 3", 3, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string 1 (2)   |\n"
        + "|test string 2       |\n"
        + "|test string 3       |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the fourth line, too long
    lcd.print("test string 4", 4, 1)
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
    Function to test mock LCD printing from the center
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )

    # Flush the current stdout buffer from begin() output
    _ = capsys.readouterr()

    # print into the first line
    lcd.print("test string 1", 1, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the first line again
    lcd.print("test string 1 (2)", 1, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the second line
    lcd.print("test string 2", 2, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the third line
    lcd.print("test string 3", 3, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "| test string 1 (2)  |\n"
        + "|   test string 2    |\n"
        + "|   test string 3    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the fourth line, too long
    lcd.print("test string 4", 4, 2)
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
    Function to test mock LCD printing from the right
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )

    # Flush the current stdout buffer from begin() output
    _ = capsys.readouterr()

    # print into the first line
    lcd.print("test string 1", 1, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|       test string 1|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the first line again
    lcd.print("test string 1 (2)", 1, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the second line
    lcd.print("test string 2", 2, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the third line
    lcd.print("test string 3", 3, 3)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|   test string 1 (2)|\n"
        + "|       test string 2|\n"
        + "|       test string 3|\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # print into the fourth line, too long
    lcd.print("test string 4", 4, 3)
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
    Function to test mock LCD when a print call is too long
    """
    lcd = LiquidCrystal(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
        cols=constants.LCD_WIDTH,
        rows=constants.LCD_HEIGHT,
    )

    # Flush the current stdout buffer from begin() and prints
    _ = capsys.readouterr()

    # print into the first line, too long
    lcd.print("test string that's too long", 1, 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|test string that's too long|\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_lcd_clear(capsys):
    """
    Function to test a mock LCD clear call
    """
    lcd = LiquidCrystal(None, None, None, None, None, None, None, 20, 4)

    # test that a 20x4 empty box is properly shown on
    lcd.print("test string", 1, 2)
    lcd.print("test string", 2, 2)
    lcd.print("test string", 3, 2)
    lcd.print("test string", 4, 2)

    # Flush the current stdout buffer from begin() and prints
    _ = capsys.readouterr()

    # clear the LCD
    lcd.clear()
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

    # clear the LCD again
    lcd.clear()
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )
