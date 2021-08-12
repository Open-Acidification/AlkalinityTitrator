import pytest

import src.devices.board_mock as board
import src.devices.lcd_mock as lcd_mock


def test_lcd_create():
    # the mock LCD doesn't use it's inputs, real or None inputs should work
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    assert lcd != None


def test_lcd_create_null():
    lcd = lcd_mock.LCD(None, None, None, None, None, None, None)
    assert lcd != None


def test_lcd_begin_large(capsys):
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(20, 4)
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
    lcd = lcd_mock.LCD(None, None, None, None, None, None, None)

    lcd.begin(20, 4)
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
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(10, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*==========*\n" + "|          |\n" + "|          |\n" + "*==========*\n"
    )

    assert lcd.cols == 10
    assert lcd.rows == 2


def test_lcd_begin_small_null(capsys):
    lcd = lcd_mock.LCD(None, None, None, None, None, None, None)

    lcd.begin(10, 2)
    captured = capsys.readouterr()
    assert captured.out == (
        "*==========*\n" + "|          |\n" + "|          |\n" + "*==========*\n"
    )

    assert lcd.cols == 10
    assert lcd.rows == 2


def test_lcd_no_begin():
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    # print without using begin() first
    with pytest.raises(ValueError):
        lcd.print("This should fail", 1, 1)


def test_lcd_no_begin_null():
    lcd = lcd_mock.LCD(None, None, None, None, None, None, None)

    # print without using begin() first
    with pytest.raises(ValueError):
        lcd.print("This should fail", 1, 1)


def test_lcd_print_left(capsys):
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(20, 4)

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
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(20, 4)

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
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(20, 4)

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
    lcd = lcd_mock.LCD(
        rs=board.D27,
        backlight=board.D15,
        enable=board.D22,
        d4=board.D18,
        d5=board.D23,
        d6=board.D24,
        d7=board.D25,
    )

    lcd.begin(20, 4)

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
    lcd = lcd_mock.LCD(None, None, None, None, None, None, None)

    # test that a 20x4 empty box is properly shown on
    lcd.begin(20, 4)
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
