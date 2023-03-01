"""
The file to test the PrimePump class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.prime_pump.prime_pump import PrimePump


@mock.patch.object(PrimePump, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test PrimePump's handle_key function for each keypad input
    """
    prime_pump = PrimePump(Titrator(), MainMenu(Titrator()))

    prime_pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "FillPump"

    prime_pump.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "EmptyPump"

    prime_pump.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    prime_pump.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test PrimePump's loop function's LiquidCrystal calls
    """
    prime_pump = PrimePump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )


@mock.patch.object(PrimePump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_prime_pump(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "1" to fill pump
        User enters "2" to empty pump
        User enters "4" to return to main menu
    """
    prime_pump = PrimePump(Titrator(), MainMenu(Titrator()))

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "FillPump"

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "EmptyPump"

    print_mock.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
