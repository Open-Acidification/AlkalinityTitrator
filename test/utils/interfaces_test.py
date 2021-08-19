"""
This test file is primarily to test the ability to import from the
titration package
"""
# from titration import utils
from titration.utils import constants, interfaces


def setup_module(module):
    constants.IS_TEST = True
    interfaces.setup_module_classes()
    interfaces.ui_lcd = interfaces.setup_lcd()
    interfaces.stir_controller = interfaces.setup_stir_control()


def test_interfaces_lcd(capsys):
    # flush stdout
    _ = capsys.readouterr()

    interfaces.lcd_out("Test string", 1, constants.LCD_LEFT_JUST)

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|Test string         |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )

def test_interfaces_stir_fast(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed_fast()
    
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  1000.0\n"
        + "Stirrer set to  2000.0\n"
        + "Stirrer set to  3000.0\n"
        + "Stirrer set to  4000.0\n"
        + "Stirrer set to  5000.0\n"
        + "Stirrer set to  6000.0\n"
        + "Stirrer set to  7000.0\n"
        + "Stirrer set to  8000.0\n"
        + "Stirrer set to  9000.0\n"
        + "Stirrer set to  10000.0\n"
        + "Stirrer set to  11000.0\n"
        + "Stirrer set to  12000.0\n"
    )

    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  0\n")

def test_interfaces_stir_slow(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed_slow()
    
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  1000.0\n"
        + "Stirrer set to  2000.0\n"
        + "Stirrer set to  3000.0\n"
        + "Stirrer set to  4000.0\n"
        + "Stirrer set to  5000.0\n"
        + "Stirrer set to  6000.0\n"
        + "Stirrer set to  7000.0\n"
        + "Stirrer set to  8000.0\n"
    )

    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  0\n")

def test_interfaces_stir_set(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed(5000, gradual=True)
    
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  1000.0\n"
        + "Stirrer set to  2000.0\n"
        + "Stirrer set to  3000.0\n"
        + "Stirrer set to  4000.0\n"
        + "Stirrer set to  5000.0\n"
    )

    interfaces.stir_speed(8000, gradual=True)
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  6000.0\n"
        + "Stirrer set to  7000.0\n"
        + "Stirrer set to  8000.0\n"
    )

    interfaces.stir_speed(3000, gradual=True)
    captured = capsys.readouterr()
    assert captured.out == (
          "Stirrer set to  7000.0\n"
        + "Stirrer set to  6000.0\n"
        + "Stirrer set to  5000.0\n"
        + "Stirrer set to  4000.0\n"
        + "Stirrer set to  3000.0\n"
    )


    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to  0\n")