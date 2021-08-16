"""
This test file is primarily to test the ability to import from the
src module
"""

from .context import titration_module


def test_can_we_import():
    assert titration_module.constants.IS_TEST is True


def test_import_interfaces(capsys):
    titration_module.interfaces.setup_interfaces()

    # flush stdout
    _ = capsys.readouterr()

    titration_module.interfaces.ui_lcd.print(
        "We did it", 1, titration_module.constants.LCD_LEFT_JUST
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
