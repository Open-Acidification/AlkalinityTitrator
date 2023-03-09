"""
The file to test the ToggleDemoMode class
"""
from unittest import mock
from unittest.mock import ANY

from titration import constants
from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.toggle_demo_mode import ToggleDemoMode
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(ToggleDemoMode, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ToggleDemoMode's handle_key function for each keypad input
    """
    toggle_demo_mode = ToggleDemoMode(
        Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator()))
    )

    toggle_demo_mode.handle_key("1")
    assert constants.IS_TEST is True
    assert toggle_demo_mode.substate == 2

    toggle_demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    toggle_demo_mode.substate = 1
    toggle_demo_mode.handle_key("0")
    assert constants.IS_TEST is False
    assert toggle_demo_mode.substate == 2

    toggle_demo_mode.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    constants.IS_TEST = True


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test ToggleDemoMode's loop function's LiquidCrystal calls
    """
    toggle_demo_mode = ToggleDemoMode(
        Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator()))
    )

    toggle_demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Mode:", line=1),
            mock.call("Mock Devices: 1", line=2),
            mock.call("Real Devices: 0", line=3),
            mock.call("", line=4),
        ]
    )

    toggle_demo_mode.substate = 2
    toggle_demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Mode Set To:", line=1),
            mock.call("Mock Devices", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    constants.IS_TEST = False
    toggle_demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Mode Set To:", line=1),
            mock.call("Real Devices", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ToggleDemoMode, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_toggle_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the ToggleDemoMode class:
        User enters "1" to continue after testing
    """
    toggle_demo_mode = ToggleDemoMode(
        Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator()))
    )

    toggle_demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Mode:", line=1),
            mock.call("Mock Devices: 1", line=2),
            mock.call("Real Devices: 0", line=3),
            mock.call("", line=4),
        ]
    )

    toggle_demo_mode.handle_key("1")
    toggle_demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Mode Set To:", line=1),
            mock.call("Mock Devices", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    toggle_demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
