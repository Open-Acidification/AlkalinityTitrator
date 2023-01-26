"""
The file to test the InitialTitration class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.initial_titration import InitialTitration
from titration.utils.titrator import Titrator
from titration.utils import constants
from titration.utils.devices.lcd_mock import LiquidCrystal


def test_handle_key():
    """
    The function to test InitialTitration's handle_key function for each user input
    """
    initial_titration = InitialTitration(Titrator())

    initial_titration.handle_key("1")
    assert initial_titration.choice == "1"
    assert initial_titration.substate == 2


@mock.patch.object(InitialTitration, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock, set_next_state_mock):
    """
    The function to test InitialTitration's loop function's LiquidCrystal calls
    """
    initial_titration = InitialTitration(Titrator())

    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )

    initial_titration.substate += 1
    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "AutomaticTitration"

    initial_titration = InitialTitration(Titrator())

    initial_titration.substate += 1
    initial_titration.choice = "1"
    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ManualTitration"


@mock.patch.object(InitialTitration, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_initial_titration_manual(print_mock, set_next_state_mock):
    """
    The function to test a use case of the InitialTitration class:
        User enters "1" to perform a manual titration
    """
    initial_titration = InitialTitration(Titrator())

    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )

    initial_titration.handle_key("1")
    assert initial_titration.choice == "1"
    assert initial_titration.substate == 2

    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ManualTitration"


@mock.patch.object(InitialTitration, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_initial_titration_automatic(print_mock, set_next_state_mock):
    """
    The function to test a use case of the InitialTitration class:
        User enters "2" to perform a manual titration
    """
    initial_titration = InitialTitration(Titrator())

    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )

    initial_titration.handle_key("2")
    assert initial_titration.choice == "2"
    assert initial_titration.substate == 2

    initial_titration.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "AutomaticTitration"
