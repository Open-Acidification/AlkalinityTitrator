"""
The file to test the PrimePump class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface
from titration.utils.ui_state.prime_pump.prime_pump import PrimePump


@mock.patch.object(PrimePump, "_setNextState")
def test_handle_key(set_next_state_mock):
    """
    The function to test PrimePump's handle_key function for each keypad input
    """
    prime_pump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    prime_pump.handleKey("3")
    assert prime_pump.values["selection"] == "3"
    assert prime_pump.subState == 2

    prime_pump.handleKey("1")
    assert prime_pump.values["selection"] == "1"

    prime_pump.handleKey("0")
    assert prime_pump.values["selection"] == "0"
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test PrimePump's loop function's lcd_interface calls
    """
    prime_pump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    prime_pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.subState += 1
    prime_pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(PrimePump, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_prime_pump(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "3" to select 3 pumps
        User enters "1" to select 1 more pump
        User enters "0" tot return to test mode
    """
    prime_pump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    prime_pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handleKey("3")
    assert prime_pump.values["selection"] == "3"
    assert prime_pump.subState == 2

    prime_pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handleKey("1")
    assert prime_pump.values["selection"] == "1"

    lcd_out_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handleKey("0")
    assert prime_pump.values["selection"] == "0"
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"
