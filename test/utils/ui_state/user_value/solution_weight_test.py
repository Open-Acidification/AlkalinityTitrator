"""
The file to test the SolutionWeight class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.solution_weight import SolutionWeight
from titration.utils import lcd_interface


@mock.patch.object(SolutionWeight, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SolutionWeight's handle_key function for each keypad input
    """
    solution_weight = SolutionWeight(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_weight.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    solution_weight.handle_key("C")
    assert solution_weight.value == ""

    solution_weight.handle_key("1")
    assert solution_weight.value[-1] == "1"

    solution_weight.handle_key("*")
    assert solution_weight.value[-1] == "."


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test SolutionWeight's loop function's lcd_interface calls
    """
    solution_weight = SolutionWeight(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(SolutionWeight, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_solution_weight(lcd_out_mock, set_next_state_mock):
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
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("3")
    assert solution_weight.value == "3"

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("*")
    assert solution_weight.value == "3."

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("*")
    assert solution_weight.value == "3."

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("1")
    assert solution_weight.value == "3.1"

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("B")
    assert solution_weight.value == "3."

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("B")
    assert solution_weight.value == "3"

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("C")
    assert solution_weight.value == ""

    solution_weight.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Sol. weight (g):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    solution_weight.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert solution_weight.titrator.solution_weight == ""
