"""
The file to test the titration CalibratePh class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.calibrate_ph import CalibratePh
from titration.utils.titrator import Titrator
from titration.utils.devices.lcd_mock import LiquidCrystal


@mock.patch.object(CalibratePh, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test CalibratePh's handle_key function for each keypad input
    """
    calibrate_ph = CalibratePh(Titrator())

    calibrate_ph.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert calibrate_ph.substate == 2

    calibrate_ph.handle_key("1")
    assert calibrate_ph.substate == 3

    calibrate_ph.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "InitialTitration"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test CalibratePh's loop function's LiquidCrystal calls
    """
    calibrate_ph = CalibratePh(Titrator())

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Enter buffer pH", line=1),
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
            mock.call("", line=4),
        ]
    )

    calibrate_ph.substate += 1
    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH, volts:", line=1),
            mock.call(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    calibrate_ph.values["buffer1_actual_pH"],
                    calibrate_ph.values["buffer1_measured_volts"],
                ),
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
        User enters "1" to continue entering buffer pH
        User enters "1" to continue after putting sensor in buffer
        User enters "1" to continue to initial titration after seeing recorded pH
    """
    calibrate_ph = CalibratePh(Titrator())

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
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert calibrate_ph.substate == 2

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    assert calibrate_ph.substate == 3

    calibrate_ph.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Recorded pH, volts:", line=1),
            mock.call(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    calibrate_ph.values["buffer1_actual_pH"],
                    calibrate_ph.values["buffer1_measured_volts"],
                ),
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibrate_ph.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "InitialTitration"
