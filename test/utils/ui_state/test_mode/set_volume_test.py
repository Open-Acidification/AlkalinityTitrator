from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface
from titration.utils.ui_state.test_mode.set_volume import SetVolume


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_called()
    assert setVolume.subState == 2

    setVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setVolume.subState += 1
    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump", line=1),
            mock.call("recorded", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


# Test SetVolume
@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(Titrator, "updateState")
def test_SetVolume(updateStateMock, lcdOutMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_called()
    assert setVolume.subState == 2

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump", line=1),
            mock.call("recorded", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    setVolume.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
