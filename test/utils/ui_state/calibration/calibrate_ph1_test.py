"""
The file to test the calibration CalibratePh class
"""

# pylint: disable = C0301

from unittest import mock
from unittest.mock import ANY
from AlkalinityTitrator.titration.utils.ui_state.main_menu import MainMenu
from AlkalinityTitrator.titration.utils.ui_state.calibration.calibrate_ph import (
    CalibratePh,
)
from AlkalinityTitrator.titration.utils.ui_state.calibration.setup_calibration import (
    SetupCalibration,
)
from AlkalinityTitrator.titration.utils.titrator import Titrator
from AlkalinityTitrator.titration.utils.devices.liquid_crystal_mock import LiquidCrystal


@mock.patch.object(CalibratePh, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test CalibratePh's handle_key function for each keypad input
    """
    calibrate_ph = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_ph.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SolutionWeight"
    assert calibrate_ph.substate == 2

    calibrate_ph.handle_key("1")
    assert calibrate_ph.substate == 3

    calibrate_ph.handle_key("a")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test CalibratePh's loop function's LiquidCrystal calls
    """
    calibrate_ph = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter Sol weight", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.substate += 1
    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("to record value", line=4),
        ]
    )

    calibrate_ph.substate += 1
    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
            mock.call(
                f"{calibrate_ph.values['buffer1_actual_pH']} pH, {calibrate_ph.values['buffer1_measured_volts']} V",
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(CalibratePh, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_calibrate_ph(print_mock, set_next_state_mock):
    """
    The function to test a use case of the CalibratePh class:
        User enters "1" to continue entering solution weight
        User enters "1" after putting sensor in buffer to continue recording value
        User enters "a" to continue setting up calibration
    """
    calibrate_ph = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter Sol weight", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SolutionWeight"
    assert calibrate_ph.substate == 2

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("to record value", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    assert calibrate_ph.substate == 3

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
            mock.call(
                f"{calibrate_ph.values['buffer1_actual_pH']} pH, {calibrate_ph.values['buffer1_measured_volts']} V",
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("a")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"
