"""
This test file is primarily to test the ability to import from the
src module
"""

from .context import src

def test_can_we_import():
    assert src.constants.IS_TEST == True

def test_import_interfaces(capsys):
    src.interfaces.setup_interfaces()

    #flush stdout
    _ = capsys.readouterr()

    src.interfaces.ui_lcd.print("We did it", 1, src.constants.LCD_LEFT_JUST)

    captured = capsys.readouterr()
    assert captured.out == (
          "*====================*\n"
        + "|We did it           |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )