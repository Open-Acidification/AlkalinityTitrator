"""
This test file is primarily to test the ability to import from the
titration package
"""
# from titration import utils
from titration.utils import constants, interfaces


def test_interfaces_requirements():
    constants.IS_TEST = True
    interfaces.setup_module_classes()
    interfaces.ui_lcd = interfaces.setup_lcd()


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
