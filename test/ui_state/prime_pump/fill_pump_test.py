"""
The file for the FillPump class tests
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.prime_pump.fill_pump import FillPump
from titration.ui_state.prime_pump.prime_pump import PrimePump


@mock.patch.object(FillPump, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test FillPump's handle_key function for each keypad input
    """
    fill_pump = FillPump(Titrator(), PrimePump(Titrator()))

    fill_pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PrimePump"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test FillPump's loop function's LiquidCrystal calls
    """
    fill_pump = FillPump(Titrator(), PrimePump(Titrator()))

    fill_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(FillPump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_prime_pump(print_mock, set_next_state_mock):
    """
    The function to test a use case of the FillPump class:
        User enters "1" to continue back to PrimePump menu
    """
    fill_pump = FillPump(Titrator(), PrimePump(Titrator()))

    fill_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    fill_pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PrimePump"
