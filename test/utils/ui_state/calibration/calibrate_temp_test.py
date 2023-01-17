"""
The file to test the CalibrateTemp class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.calibration.calibrate_temp import CalibrateTemp
from titration.utils.ui_state.calibration.setup_calibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


@mock.patch.object(CalibrateTemp, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test CalibrateTemp's handle_key function for each keypad input
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert calibrate_temp.substate == 2

    calibrate_temp.handle_key("1")
    assert calibrate_temp.substate == 3

    calibrate_temp.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test CalibrateTemp's loop function's lcd_interface calls
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_temp.substate += 1
    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )

    calibrate_temp.substate += 1
    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call(
                "{0:0.3f}".format(calibrate_temp.values["actual_temperature"]), line=2
            ),
            mock.call("{}".format(calibrate_temp.values["new_ref_resistance"]), line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(CalibrateTemp, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_calibrate_temp(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the CalibrateTemp class:
        User enters "1" to continue setting reference solution
        User enters "1" after probe has entered solution to record value
        User enters "1" to continue setting up calibration
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert calibrate_temp.substate == 2

    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    assert calibrate_temp.substate == 3

    calibrate_temp.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call(
                "{0:0.3f}".format(calibrate_temp.values["actual_temperature"]), line=2
            ),
            mock.call("{}".format(calibrate_temp.values["new_ref_resistance"]), line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"
