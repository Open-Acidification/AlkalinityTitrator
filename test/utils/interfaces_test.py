"""
The file to test the lcd interface
"""
from titration.utils import constants, interfaces


def setup_module(module):
    constants.IS_TEST = True
    interfaces.setup_module_classes()
    interfaces.ui_lcd = interfaces.setup_lcd()


def test_interfaces_lcd(capsys):
    # flush stdout
    _ = capsys.readouterr()

    interfaces.lcd_out("           ", 1, constants.LCD_LEFT_JUST)

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )
