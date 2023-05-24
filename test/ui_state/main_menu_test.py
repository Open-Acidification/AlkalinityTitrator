"""
The file to test the MainMenu class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(MainMenu, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test MainMenu's handle_key function for each keypad input
    """
    main_menu = MainMenu(Titrator())

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupTitration"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"

    main_menu.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PrimePump"

    main_menu.handle_key("4")
    assert main_menu.substate == 2

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    main_menu.handle_key("4")
    assert main_menu.substate == 1


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test MainMenu's loop function's LiquidCrystal calls
    """
    main_menu = MainMenu(Titrator())

    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Run titration", line=1),
            mock.call("2: Calibrate sensors", line=2),
            mock.call("3: Prime pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    main_menu.substate = 2
    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Update settings", line=1),
            mock.call("2: Test mode", line=2),
            mock.call("3: Exit", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )


@mock.patch.object(LiquidCrystal, "print")
@mock.patch.object(MainMenu, "_set_next_state")
def test_main_menu(set_next_state_mock, print_mock):
    """
    The function to test the entire use case of the MainMenu class
    """
    main_menu = MainMenu(Titrator())

    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Run titration", line=1),
            mock.call("2: Calibrate sensors", line=2),
            mock.call("3: Prime pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupTitration"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetupCalibration"

    main_menu.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PrimePump"

    main_menu.handle_key("4")
    assert main_menu.substate == 2

    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Update settings", line=1),
            mock.call("2: Test mode", line=2),
            mock.call("3: Exit", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    main_menu.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    main_menu.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    main_menu.handle_key("4")
    assert main_menu.substate == 1
