"""
The file to test the calibration CalibratePh class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.liquid_crystal_mock import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.calibration.calibrate_ph import CalibratePh
from titration.ui_state.calibration.setup_calibration import SetupCalibration
from titration.ui_state.main_menu import MainMenu


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
                f"{calibrate_ph.values['buffer1_actual_pH']:>2.5f} pH,"
                + f" {calibrate_ph.values['buffer1_measured_volts']:>3.4f} V",
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
                f"{calibrate_ph.values['buffer1_actual_pH']:>2.5f} pH,"
                + f" {calibrate_ph.values['buffer1_measured_volts']:>3.4f} V",
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("a")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"
