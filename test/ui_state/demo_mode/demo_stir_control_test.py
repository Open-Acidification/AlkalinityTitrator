"""
The file to test the DemoStirControl Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_stir_control import DemoStirControl


@mock.patch.object(DemoStirControl, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoStirControl's handle_key function for each keypad input
    """
    demo_stir_control = DemoStirControl(Titrator(), DemoModeMenu(Titrator()))

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 2

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 1

    demo_stir_control.handle_key("2")
    assert demo_stir_control.substate == 3

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 1

    demo_stir_control.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    demo_stir_control.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_stir_control = DemoStirControl(Titrator(), DemoModeMenu(Titrator()))

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Fast Speed", line=1),
            mock.call("2: Set Slow Speed", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_stir_control.substate = 2
    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Motor Speed", line=1),
            mock.call("Set To Fast", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_stir_control.substate = 3
    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Motor Speed", line=1),
            mock.call("Set To Slow", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(DemoStirControl, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the  class:
        User enters "1" to set Motor Speed to Fast
        User enters "1" to return to stir control menu
        User enters "2" to set Motor Speed to Slow
        User enters "1" to return to stir contolr menu
        User enters "D" to return to the main menu
    """
    demo_stir_control = DemoStirControl(Titrator(), DemoModeMenu(Titrator()))

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Fast Speed", line=1),
            mock.call("2: Set Slow Speed", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 2

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Motor Speed", line=1),
            mock.call("Set To Fast", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 1

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Fast Speed", line=1),
            mock.call("2: Set Slow Speed", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_stir_control.handle_key("2")
    assert demo_stir_control.substate == 3

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Motor Speed", line=1),
            mock.call("Set To Slow", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_stir_control.handle_key("1")
    assert demo_stir_control.substate == 1

    demo_stir_control.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Fast Speed", line=1),
            mock.call("2: Set Slow Speed", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_stir_control.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
