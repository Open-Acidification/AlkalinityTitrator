from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.handleKey("y")
    assert updateSettings.subState == 2

    updateSettings.handleKey("1")
    assert updateSettings.subState == 3

    updateSettings.handleKey("y")
    assert updateSettings.subState == 4

    updateSettings.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_mock()
    assert updateSettings.subState == 5

    updateSettings.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
    updateStateMock.reset_mock()

    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.handleKey("n")
    assert updateSettings.subState == 3

    updateSettings.handleKey("n")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Reset calibration", line=1),
            mock.call("settings to default?", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Default constants", line=1),
            mock.call("restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set volume in pump?", line=1),
            mock.call("", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump set", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


# Test UpdateSettings
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_UpdateSettings(lcdOutMock, updateStateMock):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Reset calibration", line=1),
            mock.call("settings to default?", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.handleKey("y")
    assert updateSettings.subState == 2

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Default constants", line=1),
            mock.call("restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.handleKey("1")
    assert updateSettings.subState == 3

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set volume in pump?", line=1),
            mock.call("", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.handleKey("y")
    assert updateSettings.subState == 4

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    updateSettings.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_mock()
    assert updateSettings.subState == 5

    updateSettings.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump set", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    updateSettings.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
    updateStateMock.reset_mock()
