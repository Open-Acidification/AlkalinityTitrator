"""
The file to test the Pump class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.demo_mode.demo_mode import DemoMode
from titration.utils.titrator import Titrator
from titration.utils.devices.liquid_crystal_mock import LiquidCrystal
from titration.utils.ui_state.demo_mode.pump import Pump


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

    pump.handle_key("0")
    assert pump.values["p_direction"] == "0"
    assert pump.substate == 3

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
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    pump.substate += 1
    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(Pump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_Pump(print_mock, set_next_state_mock):
    """
    The function to test a use case of the Pump class:
        User enters "1" to continue setting volume
        User enters "0" to set in/out
        User enters "1" to set pumping volume
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
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("0")
    assert pump.values["p_direction"] == "0"
    assert pump.substate == 3

    pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"
