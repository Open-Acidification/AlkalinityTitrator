"""
The file to test the Pump class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface
from titration.utils.ui_state.test_mode.pump import Pump


@mock.patch.object(Pump, "_setNextState")
def test_handle_key(set_next_state_mock):
    """
    The function to test Pump's handle_key function for each keypad input
    """
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert pump.subState == 2

    pump.handleKey("0")
    assert pump.values["p_direction"] == "0"
    assert pump.subState == 3

    pump.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test Pump's loop function's lcd_interface calls
    """
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.subState += 1
    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    pump.subState += 1
    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(Pump, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_Pump(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the Pump class:
        User enters "1" to continue setting volume
        User enters "0" to set in/out
        User enters "1" to set pumping volume
    """
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert pump.subState == 2

    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handleKey("0")
    assert pump.values["p_direction"] == "0"
    assert pump.subState == 3

    pump.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"
