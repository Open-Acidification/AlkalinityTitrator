"""
The file to test the ToggleTestMode class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.test_mode.toggle_test_mode import ToggleTestMode


@mock.patch.object(ToggleTestMode, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ToggleTestMode's handle_key function for each keypad input
    """
    toggle_test_mode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggle_test_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test ToggleTestMode's loop function's lcd_interface calls
    """
    toggle_test_mode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggle_test_mode.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Testing: {}".format(constants.IS_TEST), line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ToggleTestMode, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_toggle_test_mode(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the ToggleTestMode class:
        User enters "1" to continue after testing
    """
    toggle_test_mode = ToggleTestMode(
        Titrator(), TestMode(Titrator(), MainMenu(Titrator()))
    )

    toggle_test_mode.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Testing: {}".format(constants.IS_TEST), line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    toggle_test_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"
