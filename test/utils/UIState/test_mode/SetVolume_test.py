from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.test_mode.SetVolume import SetVolume

# Test handleKey
@mock.patch.object(SetVolume, "_setNextState")
def test_handleKey(setNextStateMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "UserValue")
    setNextStateMock.reset_called()
    assert(setVolume.subState == 2)

    setVolume.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "MainMenu")

# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Set volume in pump", line=1),
        mock.call("", line=2),
        mock.call("Press any to cont", line=3),
        mock.call("", line=4)]
    )
    lcdOutMock.reset_called()

    setVolume.subState += 1
    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Volume in pump", line=1),
        mock.call("recorded", line=2),
        mock.call("Press any to cont", line=3),
        mock.call("", line=4)]
    )

# Test SetVolume
@mock.patch.object(LCD_interface, "lcd_out")
@mock.patch.object(SetVolume, "_setNextState")
def test_SetVolume(setNextStateMock, lcdOutMock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Set volume in pump", line=1),
        mock.call("", line=2),
        mock.call("Press any to cont", line=3),
        mock.call("", line=4)]
    )
    lcdOutMock.reset_called()

    setVolume.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "UserValue")
    setNextStateMock.reset_called()
    assert(setVolume.subState == 2)

    setVolume.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Volume in pump", line=1),
        mock.call("recorded", line=2),
        mock.call("Press any to cont", line=3),
        mock.call("", line=4)]
    )

    setVolume.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "MainMenu")
