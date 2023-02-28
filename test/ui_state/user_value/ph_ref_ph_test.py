"""
The file to test the PHRefpH class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.ph_ref_ph import PHRefpH


@mock.patch.object(PHRefpH, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test PHRefpH's handle_key function for each keypad input
    """
    ph_ref_ph = PHRefpH(Titrator(), UpdateSettings(Titrator()))

    ph_ref_ph.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    ph_ref_ph.handle_key("C")
    assert ph_ref_ph.value == ""

    ph_ref_ph.handle_key("1")
    assert ph_ref_ph.value[-1] == "1"

    ph_ref_ph.handle_key("*")
    assert ph_ref_ph.value[-1] == "."

    ph_ref_ph.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test PHRefpH's loop function's LiquidCrystal calls
    """
    ph_ref_ph = PHRefpH(Titrator(), UpdateSettings(Titrator()))

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(PHRefpH, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_ph_ref_ph(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PHRefpH class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    ph_ref_ph = PHRefpH(Titrator(), UpdateSettings(Titrator()))

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("3")
    assert ph_ref_ph.value == "3"

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("*")
    assert ph_ref_ph.value == "3."

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("*")
    assert ph_ref_ph.value == "3."

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("1")
    assert ph_ref_ph.value == "3.1"

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("B")
    assert ph_ref_ph.value == "3."

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("B")
    assert ph_ref_ph.value == "3"

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("C")
    assert ph_ref_ph.value == ""

    ph_ref_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Ref pH:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    ph_ref_ph.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert ph_ref_ph.value == ""
