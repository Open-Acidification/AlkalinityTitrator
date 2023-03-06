"""
The file to test the PrimePump class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, SyringePump
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.prime_pump.prime_pump import PrimePump


@mock.patch.object(SyringePump, "pump_volume_out")
@mock.patch.object(SyringePump, "pump_volume_in")
@mock.patch.object(PrimePump, "_set_next_state")
def test_handle_key(_set_next_state, pump_volume_in, pump_volume_out):
    """
    The function to test PrimePump's handle_key function for each keypad input
    """
    prime_pump = PrimePump(Titrator(), MainMenu(Titrator()))

    prime_pump.handle_key("1")
    assert prime_pump.substate == 2
    pump_volume_in.assert_called_with(1.1)

    prime_pump.handle_key("1")
    assert prime_pump.substate == 1

    prime_pump.handle_key("2")
    assert prime_pump.substate == 3
    pump_volume_out.assert_called_with(1.1)

    prime_pump.handle_key("1")
    assert prime_pump.substate == 1

    prime_pump.handle_key("4")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "MainMenu"

    prime_pump.handle_key("D")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print):
    """
    The function to test PrimePump's loop function's LiquidCrystal calls
    """
    prime_pump = PrimePump(Titrator(), MainMenu(Titrator()))

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.substate = 2
    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.substate = 3
    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Emptying Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(SyringePump, "pump_volume_out")
@mock.patch.object(SyringePump, "pump_volume_in")
@mock.patch.object(PrimePump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_prime_pump(print, _set_next_state, pump_volume_in, pump_volume_out):
    """
    The function to test a use case of the PrimePump class:
        User enters "1" to fill pump
        User enters "1" to return to prime pump menu
        User enters "2" to empty pump
        User enters "1" to return to prime pump menu
        User enters "4" to return to main menu
    """
    prime_pump = PrimePump(Titrator(), MainMenu(Titrator()))

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("1")
    assert prime_pump.substate == 2
    pump_volume_in.assert_called_with(1.1)

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handle_key("1")
    assert prime_pump.substate == 1

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("2")
    assert prime_pump.substate == 3
    pump_volume_out.assert_called_with(1.1)

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Emptying Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    prime_pump.handle_key("1")
    assert prime_pump.substate == 1

    prime_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1. Fill Pump", line=1),
            mock.call("2. Empty Pump", line=2),
            mock.call("", line=3),
            mock.call("4. Return", line=4),
        ]
    )

    prime_pump.handle_key("4")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "MainMenu"
