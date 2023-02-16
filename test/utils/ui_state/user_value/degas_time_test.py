"""
The file to test the DegasTime class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import (
    UpdateSettings,
)
from titration.utils.ui_state.user_value.degas_time import (
    DegasTime,
)
from titration.utils.devices.liquid_crystal_mock import LiquidCrystal


@mock.patch.object(DegasTime, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test DegasTime's handle_key function for each keypad input
    """
    degas_time = DegasTime(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    degas_time.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    degas_time.handle_key("C")
    assert degas_time.value == ""

    degas_time.handle_key("1")
    assert degas_time.value[-1] == "1"

    degas_time.handle_key("*")
    assert degas_time.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test DegasTime's loop function's LiquidCrystal calls
    """
    degas_time = DegasTime(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(DegasTime, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_degas_time(print_mock, set_next_state_mock):
    """
    The function to test a use case of the DegasTime class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    degas_time = DegasTime(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("3")
    assert degas_time.value == "3"

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("*")
    assert degas_time.value == "3."

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("*")
    assert degas_time.value == "3."

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("1")
    assert degas_time.value == "3.1"

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("B")
    assert degas_time.value == "3."

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("B")
    assert degas_time.value == "3"

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("C")
    assert degas_time.value == ""

    degas_time.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert degas_time.titrator.degas_time == ""
