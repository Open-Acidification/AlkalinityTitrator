"""
The file to test the ManualTitration class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.manual_titration import ManualTitration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


@mock.patch.object(ManualTitration, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ManualTitration's handle_key function for each keypad input
    """
    manual_titration = ManualTitration(Titrator())

    manual_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert manual_titration.substate == 2

    manual_titration.handle_key("1")
    assert manual_titration.values["p_direction"] == "1"
    assert manual_titration.substate == 3

    manual_titration.handle_key("0")
    assert manual_titration.substate == 4

    manual_titration.handle_key("1")
    assert manual_titration.substate == 5

    manual_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert manual_titration.substate == 6

    manual_titration.handle_key("0")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test ManualTitration's loop function's lcd_interface calls
    """
    manual_titration = ManualTitration(Titrator())

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.substate += 1
    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Direction (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.substate += 1
    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manual_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("Add more HCl?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.substate += 1
    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manual_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("Degas?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.substate += 1
    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Degas time", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.substate += 1
    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ManualTitration, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_manual_titration(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the ManualTitration class:
        User enters "1" to continue to entering volume
        User enters "1" to enter p_direction
        User enters "0" to not add more HCl
        User enters "1" to enter degas
        User enters "1" to enter degas time
        User enters "0" to return to main menu
    """

    manual_titration = ManualTitration(Titrator())

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert manual_titration.substate == 2

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Direction (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("1")
    assert manual_titration.values["p_direction"] == "1"
    assert manual_titration.substate == 3

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manual_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("Add more HCl?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("0")
    assert manual_titration.substate == 4

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manual_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("Degas?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("1")
    assert manual_titration.substate == 5

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Degas time", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert manual_titration.substate == 6

    manual_titration.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manual_titration.handle_key("0")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
