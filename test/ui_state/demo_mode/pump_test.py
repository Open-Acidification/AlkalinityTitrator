"""
The file to test the Pump class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.demo_mode.pump import Pump
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(Pump, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Pump's handle_key function for each keypad input
    """
    pump = Pump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"
    assert pump.substate == 2

    pump.handle_key("1")
    assert pump.substate == 3

    pump.handle_key("1")
    assert pump.substate == 4
    assert pump.titrator.pump.get_pump_direction() == "1"

    pump.substate = 3
    pump.handle_key("0")
    assert pump.substate == 4
    assert pump.titrator.pump.get_pump_direction() == "0"

    pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test Pump's loop function's LiquidCrystal calls
    """
    pump = Pump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.substate += 1
    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pumping Volume Set To:", line=1),
            mock.call(f"{pump.titrator.pump_volume}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.substate += 1
    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Pump Direction:", line=1),
            mock.call("", line=2),
            mock.call("In/Out (0/1)", line=3),
            mock.call("", line=4),
        ]
    )

    pump.substate += 1
    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Direction Set To:", line=1),
            mock.call(f"{pump.titrator.pump.get_pump_direction()}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(Pump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_pump(print_mock, set_next_state_mock):
    """
    The function to test a use case of the Pump class:
        User enters "1" to set volume
        User enters "1" to display set volume
        User enters "0" to set pumping direction
        User enters "1" to return to demo mode
    """
    pump = Pump(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"
    assert pump.substate == 2

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pumping Volume Set To:", line=1),
            mock.call(f"{pump.titrator.pump_volume}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("1")
    assert pump.substate == 3

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Pump Direction:", line=1),
            mock.call("", line=2),
            mock.call("In/Out (0/1)", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("0")
    assert pump.titrator.pump.get_pump_direction() == "0"
    assert pump.substate == 4

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Direction Set To:", line=1),
            mock.call(f"{pump.titrator.pump.get_pump_direction()}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"
