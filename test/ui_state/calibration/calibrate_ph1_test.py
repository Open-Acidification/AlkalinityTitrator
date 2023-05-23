"""
The file to test the calibration CalibratePh class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, PHProbe
from titration.titrator import Titrator
from titration.ui_state.calibration.calibrate_ph import CalibratePh
from titration.ui_state.calibration.setup_calibration import SetupCalibration
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(PHProbe, "get_voltage")
@mock.patch.object(CalibratePh, "_set_next_state")
def test_handle_key(_set_next_state, get_voltage):
    """
    The function to test CalibratePh's handle_key function for each keypad input
    """
    calibrate_ph = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_ph.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "BufferPH"
    assert calibrate_ph.substate == 2

    calibrate_ph.handle_key("1")
    get_voltage.assert_called()
    assert calibrate_ph.substate == 3

    calibrate_ph.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "SetupCalibration"


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
            mock.call("Enter buffer pH", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.substate = 2
    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("to record value", line=4),
        ]
    )

    calibrate_ph.substate = 3
    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
            mock.call(
                f"{calibrate_ph.titrator.buffer_nominal_ph:>2.5f} pH,"
                + f" {calibrate_ph.titrator.buffer_measured_volts:>3.4f} V",
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(PHProbe, "get_voltage", return_value=0)
@mock.patch.object(CalibratePh, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_calibrate_ph(print_mock, _set_next_state, get_voltage):
    """
    The function to test a use case of the CalibratePh class:
        User enters "1" to continue entering solution weight
        User enters "1" after putting sensor in buffer to continue recording value
        User enters "1" to continue setting up calibration
    """
    calibrate_ph = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "BufferPH"
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
    get_voltage.assert_called()
    assert calibrate_ph.substate == 3

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
            mock.call(
                f"{calibrate_ph.titrator.buffer_nominal_ph:>2.5f} pH,"
                + f" {calibrate_ph.titrator.buffer_measured_volts:>3.4f} V",
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "SetupCalibration"
