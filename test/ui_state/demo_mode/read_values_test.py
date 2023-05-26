"""
The file to test the ReadValues class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.read_values import ReadValues
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(ReadValues, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadValues' handle_key function for each keypad input
    """
    read_values = ReadValues(Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator())))

    read_values.handle_key("1")
    assert read_values.substate == 2

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    read_values.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test ReadValues' loop function's LiquidCrystal calls and delay calls
    """
    read_values = ReadValues(Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                f"pH:     {read_values.titrator.ph_probe.get_voltage():>4.5f} pH",
                line=1,
            ),
            mock.call(
                f"pH V:   {(read_values.titrator.ph_probe.get_voltage() * 1000):>3.4f} mV",
                line=2,
            ),
            mock.call(f"Gain:   {read_values.titrator.ph_probe.get_gain()}", line=3),
            mock.call(
                f"Volume: {read_values.titrator.pump.get_volume_in_pump()} ml",
                line=4,
            ),
        ]
    )

    read_values.substate = 2
    read_values.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                f"Temp:   {read_values.titrator.temperature_probe_control.get_temperature():>4.3f} C",
                line=1,
            ),
            mock.call(
                f"Res:    {read_values.titrator.temperature_probe_control.get_resistance():>4.3f} Ohms",
                line=2,
            ),
            mock.call("", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )


@mock.patch.object(ReadValues, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_read_values(print_mock, set_next_state_mock):
    """
    The function to test a use case of the ReadValues class:
        User enters "1" for the next set of values
        User enters "1" to return to demo mode menu
    """
    read_values = ReadValues(Titrator(), DemoModeMenu(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                f"pH:     {read_values.titrator.ph_probe.get_voltage():>4.5f} pH",
                line=1,
            ),
            mock.call(
                f"pH V:   {(read_values.titrator.ph_probe.get_voltage() * 1000):>3.4f} mV",
                line=2,
            ),
            mock.call(f"Gain:   {read_values.titrator.ph_probe.get_gain()}", line=3),
            mock.call(
                f"Volume: {read_values.titrator.pump.get_volume_in_pump()} ml",
                line=4,
            ),
        ]
    )

    read_values.handle_key("1")
    assert read_values.substate == 2

    read_values.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                f"Temp:   {read_values.titrator.temperature_probe_control.get_temperature():>4.3f} C",
                line=1,
            ),
            mock.call(
                f"Res:    {read_values.titrator.temperature_probe_control.get_resistance():>4.3f} Ohms",
                line=2,
            ),
            mock.call("", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
