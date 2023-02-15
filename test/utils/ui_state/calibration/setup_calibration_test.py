"""
The file to the SetupCalibration class
"""
from unittest import mock
from unittest.mock import ANY
from AlkalinityTitrator.titration.utils.ui_state.main_menu import MainMenu
from AlkalinityTitrator.titration.utils.ui_state.calibration.setup_calibration import (
    SetupCalibration,
)
from AlkalinityTitrator.titration.utils.titrator import Titrator
from AlkalinityTitrator.titration.utils.devices.liquid_crystal_mock import LiquidCrystal


@mock.patch.object(SetupCalibration, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SetupCalibration's handle_key function for each keypad input
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"
    set_next_state_mock.reset_called()

    setup_calibration.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibrateTemp"
    set_next_state_mock.reset_called()

    setup_calibration.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SetupCalibration's loop function's LiquidCrystal calls
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(SetupCalibration, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_setup_calibration(print_mock, set_next_state_mock):
    """
    The function to test a use case of the SetupCalibration class:
        User enters "1" to calibrate pH
    """
    setup_calibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setup_calibration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )

    setup_calibration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"
