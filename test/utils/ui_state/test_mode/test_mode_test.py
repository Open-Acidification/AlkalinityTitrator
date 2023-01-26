"""
The file to test the TestMode class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils.devices.lcd_mock import LiquidCrystal
from titration.utils.ui_state.test_mode.test_mode import TestMode


@mock.patch.object(TestMode, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the TestMode's handle_key function for each keypad input
    """
    test_mode = TestMode(Titrator(), MainMenu(Titrator()))

    test_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    test_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "Pump"

    test_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetVolume"

    test_mode.handle_key("*")
    assert test_mode.substate == 2

    test_mode.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleTestMode"

    test_mode.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadVolume"

    test_mode.handle_key("6")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    test_mode.handle_key("*")
    assert test_mode.substate == 1


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test TestMode's loop function's LiquidCrystal calls
    """
    test_mode = TestMode(Titrator(), MainMenu(Titrator()))

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    test_mode.substate += 1
    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )


@mock.patch.object(TestMode, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_test_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the TestMode class:
        User enters "1" to read values
        User enters "2" to pump
        User enters "3" to set volume
        User enters "*" to get to page 2
        User enters "4" to toggle test mode
        User enters "5" to read volume
        User enters "6" to exit test mode
    """
    test_mode = TestMode(Titrator(), MainMenu(Titrator()))

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    test_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    test_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "Pump"

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    test_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetVolume"

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    test_mode.handle_key("*")
    assert test_mode.substate == 2

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    test_mode.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleTestMode"

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    test_mode.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadVolume"

    test_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    test_mode.handle_key("6")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
