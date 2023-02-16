"""
The file to test the MainMenu class
"""
from unittest.mock import ANY
from unittest import mock
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils.devices.liquid_crystal_mock import LiquidCrystal


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

    main_menu.handle_key("*")
    assert main_menu.substate == 2

    main_menu.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    main_menu.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"

    main_menu.handle_key("*")
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
            mock.call("Run titration", line=1),
            mock.call("Calibrate sensors", line=2),
            mock.call("Prime pump", line=3),
            mock.call("Page 2", line=4),
        ]
    )

    main_menu.substate = 2
    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Update settings", line=1),
            mock.call("Test mode", line=2),
            mock.call("Exit", line=3),
            mock.call("Page 1", line=4),
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
            mock.call("Run titration", line=1),
            mock.call("Calibrate sensors", line=2),
            mock.call("Prime pump", line=3),
            mock.call("Page 2", line=4),
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

    main_menu.handle_key("*")
    assert main_menu.substate == 2

    main_menu.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Update settings", line=1),
            mock.call("Test mode", line=2),
            mock.call("Exit", line=3),
            mock.call("Page 1", line=4),
        ]
    )

    main_menu.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    main_menu.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoMode"

    main_menu.handle_key("*")
    assert main_menu.substate == 1
