from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.test_mode.read_volume import ReadVolume
from titration.utils.ui_state.test_mode.test_mode import TestMode


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "TestMode"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                "{0:1.2f}".format(constants.volume_in_pump),
                style=constants.LCD_CENT_JUST,
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


# Test ReadVolume
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_ReadVolume(lcdOutMock, updateStateMock):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                "{0:1.2f}".format(constants.volume_in_pump),
                style=constants.LCD_CENT_JUST,
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    readVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "TestMode"
