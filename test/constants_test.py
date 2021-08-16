"""
This test file is primarily to test the ability to import from the
src module
"""
# from titration import utils
from titration.utils import interfaces, constants

def setup_test_mode():
    constants.IS_TEST = True

def test_can_we_import():
    assert constants.IS_TEST is True


def test_import_interfaces(capsys):
    interfaces.ui_lcd = interfaces.setup_lcd()

    # flush stdout
    _ = capsys.readouterr()

    interfaces.ui_lcd.print(
        "We did it", 1, constants.LCD_LEFT_JUST
    )

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|We did it           |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )
