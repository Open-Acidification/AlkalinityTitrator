"""
The file to test the UserValue class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.user_value import UserValue
from titration.utils.devices.liquid_crystal_mock import LiquidCrystal


@mock.patch.object(UserValue, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test UserValue's handle_key function for each keypad input
    """
    user_value = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    user_value.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    user_value.handle_key("C")
    assert user_value.string == ""

    user_value.handle_key("1")
    assert user_value.string[-1] == "1"

    user_value.handle_key("*")
    assert user_value.string[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test UserValue's loop function's lcd_interface calls
    """
    user_value = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(UserValue, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_user_value(print_mock, set_next_state_mock):
    """
    The function to test a use case of the UserValue class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    user_value = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("3")
    assert user_value.string == "3"

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("*")
    assert user_value.string == "3."

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("*")
    assert user_value.string == "3."

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("1")
    assert user_value.string == "3.1"

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("B")
    assert user_value.string == "3."

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("B")
    assert user_value.string == "3"

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("C")
    assert user_value.string == ""

    user_value.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
