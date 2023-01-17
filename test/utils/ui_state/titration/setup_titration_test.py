"""
The file to test the SetupTitration class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.setup_titration import SetupTitration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants


@mock.patch.object(SetupTitration, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test SetupTitration's handle_key function for each keypad input
    """
    setup_titration = SetupTitration(Titrator())

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert setup_titration.substate == 2

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert setup_titration.substate == 3

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"

    setup_titration.handle_key("0")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "InitialTitration"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test SetupTitration's loop function's lcd_interface calls
    """
    setup_titration = SetupTitration(Titrator())

    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("weight (g)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    setup_titration.substate += 1
    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("salinity (ppt)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    setup_titration.substate += 1
    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Calibrate pH probe?", line=1),
            mock.call("Yes: 1", line=2),
            mock.call("No (use old): 0", line=3),
            mock.call(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            ),
        ]
    )


@mock.patch.object(SetupTitration, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_setup_titration(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the SetupTitration class:
        User enters "1" to continue to enter solution weight
        User enters "1" to continue to enter solution salinity
        User enters "1" to calibrate pH probe"
    """
    setup_titration = SetupTitration(Titrator())

    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("weight (g)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert setup_titration.substate == 2

    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("salinity (ppt)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert setup_titration.substate == 3

    setup_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Calibrate pH probe?", line=1),
            mock.call("Yes: 1", line=2),
            mock.call("No (use old): 0", line=3),
            mock.call(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            ),
        ]
    )

    setup_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "CalibratePh"
