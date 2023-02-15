"""
The file to test the BufferPH class
"""
from unittest import mock
from unittest.mock import ANY
from AlkalinityTitrator.titration.utils.titrator import Titrator
from AlkalinityTitrator.titration.utils.ui_state.main_menu import MainMenu
from AlkalinityTitrator.titration.utils.ui_state.update_settings.update_settings import (
    UpdateSettings,
)
from AlkalinityTitrator.titration.utils.ui_state.user_value.buffer_ph import (
    BufferPH,
)
from AlkalinityTitrator.titration.utils.devices.liquid_crystal_mock import LiquidCrystal


@mock.patch.object(BufferPH, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test BufferPH's handle_key function for each keypad input
    """
    buffer_ph = BufferPH(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    buffer_ph.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    buffer_ph.handle_key("C")
    assert buffer_ph.value == ""

    buffer_ph.handle_key("1")
    assert buffer_ph.value[-1] == "1"

    buffer_ph.handle_key("*")
    assert buffer_ph.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test BufferPH's loop function's LiquidCrystal calls
    """
    buffer_ph = BufferPH(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(BufferPH, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_buffer_ph(print_mock, set_next_state_mock):
    """
    The function to test a use case of the BufferPH class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    buffer_ph = BufferPH(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("3")
    assert buffer_ph.value == "3"

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("*")
    assert buffer_ph.value == "3."

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("*")
    assert buffer_ph.value == "3."

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("1")
    assert buffer_ph.value == "3.1"

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("B")
    assert buffer_ph.value == "3."

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("B")
    assert buffer_ph.value == "3"

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("C")
    assert buffer_ph.value == ""

    buffer_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    buffer_ph.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert buffer_ph.titrator.buffer_ph == ""
