"""
The file to the SetupCalibration class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.calibration.setup_calibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


@mock.patch.object(SetupCalibration, "_setNextState")
def test_handle_key(set_next_state_mock):
    """
    The function to test SetupCalibration's handle_key function for each keypad input
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"
    set_next_state_mock.reset_called()

    setup_calibration.handleKey("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibrateTemp"
    set_next_state_mock.reset_called()

    setup_calibration.handleKey("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test SetupCalibration's loop function's lcd_interface calls
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(SetupCalibration, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_setup_calibration(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the SetupCalibration class:
        User enters "1" to calibrate pH
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )

    setup_calibration.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"
