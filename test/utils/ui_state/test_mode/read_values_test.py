"""
The file to test the ReadValues class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, interfaces
from titration.utils.ui_state.test_mode.read_values import ReadValues


@mock.patch.object(ReadValues, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadValues' handle_key function for each keypad input
    """
    read_values = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"


@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(interfaces, "delay")
def test_loop(delay_mock, lcd_out_mock):
    """
    The function to test ReadValues' loop function's lcd_interface calls and delay calls
    """
    read_values = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    assert delay_mock.called_with(read_values.values["timeStep"])
    for i in range(read_values.values["numVals"]):
        lcd_out_mock.assert_has_calls(
            [
                mock.call(
                    "Temp: {0:>4.3f} C".format(read_values.values["temp"]), line=1
                ),
                mock.call(
                    "Res:  {0:>4.3f} Ohms".format(read_values.values["res"]), line=2
                ),
                mock.call(
                    "pH:   {0:>4.5f} pH".format(read_values.values["pH_reading"]),
                    line=3,
                ),
                mock.call(
                    "pH V: {0:>3.4f} mV".format(read_values.values["pH_volts"] * 1000),
                    line=4,
                ),
                mock.call("Reading: {}".format(i), 1, console=True),
            ]
        )

    lcd_out_mock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ReadValues, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(interfaces, "delay")
def test_read_values(delay_mock, lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the ReadValues class:
        User enters "1" after the lcd reads values for temp, res, pH, and pH_volts
    """
    read_values = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_values.loop()
    assert delay_mock.called_with(read_values.values["timeStep"])
    for i in range(read_values.values["numVals"]):
        lcd_out_mock.assert_has_calls(
            [
                mock.call(
                    "Temp: {0:>4.3f} C".format(read_values.values["temp"]), line=1
                ),
                mock.call(
                    "Res:  {0:>4.3f} Ohms".format(read_values.values["res"]), line=2
                ),
                mock.call(
                    "pH:   {0:>4.5f} pH".format(read_values.values["pH_reading"]),
                    line=3,
                ),
                mock.call(
                    "pH V: {0:>3.4f} mV".format(read_values.values["pH_volts"] * 1000),
                    line=4,
                ),
                mock.call("Reading: {}".format(i), 1, console=True),
            ]
        )

    lcd_out_mock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    read_values.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"
