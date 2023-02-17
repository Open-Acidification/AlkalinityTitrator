"""
The file to test the ReadVolume class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.liquid_crystal_mock import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.demo_mode.read_volume import ReadVolume
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(ReadVolume, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadVolume's handle_key function for each keypad input
    """
    read_volume = ReadVolume(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SetVolume's loop function's LiquidCrystal calls
    """
    read_volume = ReadVolume(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                f"{read_volume.titrator.pump.get_volume_in_pump():1.2f}",
                style="center",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ReadVolume, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_read_volume(print_mock, set_next_state_mock):
    """
    The function to test a use case of the SetVolume class:
        User enters "1" to continue after the pump volume is read
    """
    read_volume = ReadVolume(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                f"{read_volume.titrator.pump.get_volume_in_pump():1.2f}",
                style="center",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    read_volume.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"
