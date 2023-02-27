"""
The file to test the UpdateSettings class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings


@mock.patch.object(UpdateSettings, "_set_next_state")
def test_handle_key_update(set_next_state_mock):
    """
    The function to test UpdateSettings' handle_key function for each keypad input
    when a user wants to update settings
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetGain"

    update_settings.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    update_settings.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test UpdateSettings' loop function's lcd_interface calls
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set pH Probe Gain", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )


@mock.patch.object(UpdateSettings, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_update_settings(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "1" to set gain
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set pH Probe Gain", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetGain"
