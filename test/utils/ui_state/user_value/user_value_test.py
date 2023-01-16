"""
The file to test the UserValue class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.user_value import UserValue
from titration.utils import lcd_interface


@mock.patch.object(UserValue, "_setNextState")
def test_handle_key(set_next_state_mock):
    """
    The function to test UserValue's handle_key function for each keypad input
    """
    user_value = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    user_value.handleKey("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    user_value.handleKey("C")
    assert user_value.string == ""

    user_value.handleKey("1")
    assert user_value.string[-1] == "1"

    user_value.handleKey("*")
    assert user_value.string[-1] == "."


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test UserValue's loop function's lcd_interface calls
    """
    user_value = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(UserValue, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_user_value(lcd_out_mock, set_next_state_mock):
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
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("3")
    assert user_value.string == "3"

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("*")
    assert user_value.string == "3."

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("*")
    assert user_value.string == "3."

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("1")
    assert user_value.string == "3.1"

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("B")
    assert user_value.string == "3."

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("B")
    assert user_value.string == "3"

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("C")
    assert user_value.string == ""

    user_value.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    user_value.handleKey("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
