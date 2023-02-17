"""
The file to test the PrimePump class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.liquid_crystal_mock import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.prime_pump.prime_pump import PrimePump


@mock.patch.object(PrimePump, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test PrimePump's handle_key function for each keypad input
    """
    prime_pump = PrimePump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    prime_pump.handle_key("3")
    assert prime_pump.values["selection"] == "3"
    assert prime_pump.substate == 2

    prime_pump.handle_key("1")
    assert prime_pump.values["selection"] == "1"

    prime_pump.handle_key("0")
    assert prime_pump.values["selection"] == "0"
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test PrimePump's loop function's LiquidCrystal calls
    """
    prime_pump = PrimePump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.substate += 1
    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(PrimePump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_prime_pump(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "3" to select 3 pumps
        User enters "1" to select 1 more pump
        User enters "0" tot return to test mode
    """
    prime_pump = PrimePump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handle_key("3")
    assert prime_pump.values["selection"] == "3"
    assert prime_pump.substate == 2

    prime_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handle_key("1")
    assert prime_pump.values["selection"] == "1"

    print_mock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handle_key("0")
    assert prime_pump.values["selection"] == "0"
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"
