"""
The file to test the SetVolume class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.set_volume import SetVolume
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(SetVolume, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SetVolume's handle_key function for each keypad input
    """
    set_volume = SetVolume(Titrator(), MainMenu(Titrator()))

    set_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"
    assert set_volume.substate == 2

    set_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SetVolume's loop function's LiquidCrystal calls
    """
    set_volume = SetVolume(Titrator(), MainMenu(Titrator()))

    set_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Volume In Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    set_volume.substate += 1
    set_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Volume Set To:", line=1),
            mock.call(f"{set_volume.titrator.pump_volume}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(LiquidCrystal, "print")
@mock.patch.object(SetVolume, "_set_next_state")
def test_set_volume(set_next_state_mock, print_mock):
    """
    The function to test a use case of the SetVolume class:
        User enters "1" to continue setting volume in pump
        User enters "1" to continue after the pump volume has been recorded
    """
    set_volume = SetVolume(Titrator(), MainMenu(Titrator()))

    set_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set Volume In Pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    set_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"
    assert set_volume.substate == 2

    set_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Volume Set To:", line=1),
            mock.call(f"{set_volume.titrator.pump_volume}", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    set_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
