"""
The file to test the DemoMode class
"""
from unittest import mock
from unittest.mock import ANY
from AlkalinityTitrator.titration.utils.ui_state.main_menu import MainMenu
from AlkalinityTitrator.titration.utils.titrator import Titrator
from AlkalinityTitrator.titration.utils.devices.liquid_crystal_mock import LiquidCrystal
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.demo_mode import DemoMode


@mock.patch.object(DemoMode, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoMode's handle_key function for each keypad input
    """
    demo_mode = DemoMode(Titrator(), MainMenu(Titrator()))

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "Pump"

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetVolume"

    demo_mode.handle_key("*")
    assert demo_mode.substate == 2

    demo_mode.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleDemoMode"

    demo_mode.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadVolume"

    demo_mode.handle_key("6")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"

    demo_mode.handle_key("*")
    assert demo_mode.substate == 1


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test DemoMode's loop function's LiquidCrystal calls
    """
    demo_mode = DemoMode(Titrator(), MainMenu(Titrator()))

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    demo_mode.substate += 1
    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Demo Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Demo Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )


@mock.patch.object(DemoMode, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the DemoMode class:
        User enters "1" to read values
        User enters "2" to pump
        User enters "3" to set volume
        User enters "*" to get to page 2
        User enters "4" to toggle demo mode
        User enters "5" to read volume
        User enters "6" to exit demo mode
    """
    demo_mode = DemoMode(Titrator(), MainMenu(Titrator()))

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "Pump"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetVolume"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("*")
    assert demo_mode.substate == 2

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Demo Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Demo Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleDemoMode"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Demo Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Demo Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadVolume"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("4: Toggle Demo Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Demo Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("6")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
