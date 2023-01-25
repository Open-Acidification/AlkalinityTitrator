"""
The file to test the DegasTime class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.degas_time import (
    DegasTime,
)
from titration.utils import lcd_interface


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
    assert degas_time.string == ""

    degas_time.handle_key("1")
    assert degas_time.string[-1] == "1"

    degas_time.handle_key("*")
    assert degas_time.string[-1] == "."


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test DegasTime's loop function's lcd_interface calls
    """
    degas_time = DegasTime(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(DegasTime, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_degas_time(lcd_out_mock, set_next_state_mock):
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
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("3")
    assert degas_time.string == "3"

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("*")
    assert degas_time.string == "3."

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("*")
    assert degas_time.string == "3."

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("1")
    assert degas_time.string == "3.1"

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("B")
    assert degas_time.string == "3."

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("B")
    assert degas_time.string == "3"

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("C")
    assert degas_time.string == ""

    degas_time.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Degas time (s):", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    degas_time.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert degas_time.titrator.degas_time == ""
