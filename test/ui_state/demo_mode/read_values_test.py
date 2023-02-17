"""
The file to test the ReadValues class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.liquid_crystal_mock import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.demo_mode.read_values import ReadValues
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(ReadValues, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadValues' handle_key function for each keypad input
    """
    read_values = ReadValues(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test ReadValues' loop function's LiquidCrystal calls and delay calls
    """
    read_values = ReadValues(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    for i in range(read_values.values["numVals"]):
        print_mock.assert_has_calls(
            [
                mock.call(f"Temp: {read_values.values['temp']:>4.3f} C", line=1),
                mock.call(f"Res:  {read_values.values['res']:>4.3f} Ohms", line=2),
                mock.call(
                    f"pH:   {read_values.values['pH_reading']:>4.5f} pH",
                    line=3,
                ),
                mock.call(
                    f"pH V: {(read_values.values['pH_volts'] * 1000):>3.4f} mV",
                    line=4,
                ),
                mock.call(f"Reading: {i}", 1, console=True),
            ]
        )

    print_mock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ReadValues, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_read_values(print_mock, set_next_state_mock):
    """
    The function to test a use case of the ReadValues class:
        User enters "1" after the liquid_crystal reads values for temp, res, pH, and pH_volts
    """
    read_values = ReadValues(Titrator(), DemoMode(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    for i in range(read_values.values["numVals"]):
        print_mock.assert_has_calls(
            [
                mock.call(f"Temp: {read_values.values['temp']:>4.3f} C", line=1),
                mock.call(f"Res:  {read_values.values['res']:>4.3f} Ohms", line=2),
                mock.call(
                    f"pH:   {read_values.values['pH_reading']:>4.5f} pH",
                    line=3,
                ),
                mock.call(
                    f"pH V: {(read_values.values['pH_volts'] * 1000):>3.4f} mV",
                    line=4,
                ),
                mock.call(f"Reading: {i}", 1, console=True),
            ]
        )

    print_mock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"
