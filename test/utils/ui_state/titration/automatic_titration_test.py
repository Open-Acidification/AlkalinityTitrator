"""
The file to test the AutomaticTitration class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.automatic_titration import AutomaticTitration
from titration.utils.titrator import Titrator
from titration.utils.devices.lcd_mock import LCD


@mock.patch.object(AutomaticTitration, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test AutomaticTitration's handle_key function for each keypad input
    """
    automatic_titration = AutomaticTitration(Titrator())

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 2

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 3

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 4

    automatic_titration.handle_key("0")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LCD, "print")
def test_loop(print_mock):
    """
    The function to test AutomaticTitration's loop function's LCD calls
    """
    automatic_titration = AutomaticTitration(Titrator())

    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                "Titrating to {} pH".format(
                    str(automatic_titration.values["pH_target"])
                ),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.substate += 1
    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Mixing...", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.substate += 1
    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                "pH value {} reached".format(automatic_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.substate += 1
    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(AutomaticTitration, "_set_next_state")
@mock.patch.object(LCD, "print")
def test_automatic_titration(print_mock, set_next_state_mock):
    """
    The function to test a use case of the AutomaticTitration class:
        User enters "1" to continue after titrating to desired pH target
        User enters "1" to continue after mixing
        User enters "1" after pH value reached
        User enters "0" to return to main menu
    """
    automatic_titration = AutomaticTitration(Titrator())

    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                "Titrating to {} pH".format(
                    str(automatic_titration.values["pH_target"])
                ),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 2

    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Mixing...", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 3

    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call(
                "pH value {} reached".format(automatic_titration.values["current_pH"]),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.handle_key("1")
    assert automatic_titration.substate == 4

    automatic_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automatic_titration.handle_key("0")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
