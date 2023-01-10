from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.test_mode.toggle_test_mode import ToggleTestMode


# Test handleKey
@mock.patch.object(ToggleTestMode, "_setNextState")
def test_handleKey(setNextStateMock):
    toggleTestMode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggleTestMode.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    toggleTestMode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggleTestMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Testing: {}".format(constants.IS_TEST), line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


# Test ToggleTestMode
@mock.patch.object(ToggleTestMode, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_ToggleTestMode(lcdOutMock, setNextStateMock):
    toggleTestMode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggleTestMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Testing: {}".format(constants.IS_TEST), line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    toggleTestMode.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
