"""
The file to test the SolutionSalinity class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.liquid_crystal_mock import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.solution_salinity import SolutionSalinity


@mock.patch.object(SolutionSalinity, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SolutionSalinity's handle_key function for each keypad input
    """
    solution_salinity = SolutionSalinity(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_salinity.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    solution_salinity.handle_key("C")
    assert solution_salinity.value == ""

    solution_salinity.handle_key("1")
    assert solution_salinity.value[-1] == "1"

    solution_salinity.handle_key("*")
    assert solution_salinity.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SolutionSalinity's loop function's LiquidCrystal calls
    """
    solution_salinity = SolutionSalinity(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(SolutionSalinity, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_solution_salinity(print_mock, set_next_state_mock):
    """
    The function to test a use case of the SolutionSalinity class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    solution_salinity = SolutionSalinity(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("3")
    assert solution_salinity.value == "3"

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("*")
    assert solution_salinity.value == "3."

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("*")
    assert solution_salinity.value == "3."

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("1")
    assert solution_salinity.value == "3.1"

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("B")
    assert solution_salinity.value == "3."

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("B")
    assert solution_salinity.value == "3"

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("C")
    assert solution_salinity.value == ""

    solution_salinity.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. salinity (ppt):", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_salinity.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert solution_salinity.titrator.solution_salinity == ""
