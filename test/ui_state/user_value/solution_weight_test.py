"""
The file to test the SolutionWeight class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.solution_weight import SolutionWeight


@mock.patch.object(SolutionWeight, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SolutionWeight's handle_key function for each keypad input
    """
    solution_weight = SolutionWeight(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_weight.handle_key("A")
    set_next_state_mock.assert_not_called()

    solution_weight.value = "1"
    solution_weight.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    solution_weight.handle_key("C")
    assert solution_weight.value == ""

    solution_weight.handle_key("1")
    assert solution_weight.value[-1] == "1"

    solution_weight.handle_key("*")
    assert solution_weight.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SolutionWeight's loop function's LiquidCrystal calls
    """
    solution_weight = SolutionWeight(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )


@mock.patch.object(SolutionWeight, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_solution_weight(print_mock, set_next_state_mock):
    """
    The function to test a use case of the SolutionWeight class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    solution_weight = SolutionWeight(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("3")
    assert solution_weight.value == "3"

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("*")
    assert solution_weight.value == "3."

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("*")
    assert solution_weight.value == "3."

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("1")
    assert solution_weight.value == "3.1"

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("B")
    assert solution_weight.value == "3."

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("B")
    assert solution_weight.value == "3"

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("C")
    assert solution_weight.value == ""

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("A")
    set_next_state_mock.assert_not_called()
    assert solution_weight.value == ""

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("1")
    assert solution_weight.value == "1"

    solution_weight.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    solution_weight.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert solution_weight.titrator.solution_weight == 1.0
