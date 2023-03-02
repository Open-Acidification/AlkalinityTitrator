"""
The file to test the DemoModeMenu class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(DemoModeMenu, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the 's handle_key function for each keypad input
    """
    demo_mode = DemoModeMenu(Titrator(), MainMenu(Titrator()))

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemopHProbe"

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoPump"

    demo_mode.handle_key("4")
    assert demo_mode.substate == 2

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoStirControl"

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoTempControl"

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleDemoMode"

    demo_mode.handle_key("4")
    assert demo_mode.substate == 1

    demo_mode.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_mode = DemoModeMenu(Titrator(), MainMenu(Titrator()))

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.substate = 2
    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Demo Stir Control", line=1),
            mock.call("2: Demo Temp Probe", line=2),
            mock.call("3: Toggle Demo Mode", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )


@mock.patch.object(DemoModeMenu, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the  class:
        User enters "1" to read values
        User enters "2" to demo the pH Probe
        User enters "3" to demo the Pump
        User enters "4" to get to page 2
        User enters "1" to demo the Stir Control
        User enters "2" to demo the Temp Probe
        User enters "3" to toggle the demo mode
        User enters "4" to get to page 1
        User enters "D" to return to the main menu
    """
    demo_mode = DemoModeMenu(Titrator(), MainMenu(Titrator()))

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ReadValues"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemopHProbe"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoPump"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("4")
    assert demo_mode.substate == 2

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Demo Stir Control", line=1),
            mock.call("2: Demo Temp Probe", line=2),
            mock.call("3: Toggle Demo Mode", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoStirControl"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Demo Stir Control", line=1),
            mock.call("2: Demo Temp Probe", line=2),
            mock.call("3: Toggle Demo Mode", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoTempControl"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Demo Stir Control", line=1),
            mock.call("2: Demo Temp Probe", line=2),
            mock.call("3: Toggle Demo Mode", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "ToggleDemoMode"

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Demo Stir Control", line=1),
            mock.call("2: Demo Temp Probe", line=2),
            mock.call("3: Toggle Demo Mode", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_mode.handle_key("4")
    assert demo_mode.substate == 1

    demo_mode.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Demo pH Probe", line=2),
            mock.call("3: Demo Pump", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_mode.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
