"""
The file to test the DemoPump Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_pump import DemoPump


@mock.patch.object(DemoPump, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoPump's handle_key function for each keypad input
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.handle_key("1")
    assert demo_pump.substate == 3

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"

    demo_pump.handle_key("3")
    assert demo_pump.substate == 1

    demo_pump.handle_key("4")
    assert demo_pump.substate == 2

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.handle_key("4")
    assert demo_pump.substate == 1

    demo_pump.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Pump Volume In", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.substate = 2
    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Pump Volume Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.substate = 3
    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_volume_in_pump()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(DemoPump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the  class:
        User enters "1" to Get Volume
        User enters "1" to return to demo pump menu
        User enters "2" to Set Volume
        User enters "3" to test pulling liquid
        User enters "4" to go to 2nd page of options
        User enters "1" to test pushing liquid
        User enters "4" to go to 1st page of options
        User enters "D" to return to Demo Menu
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Pump Volume In", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 3

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Pump Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_volume_in_pump()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Pump Volume In", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PumpVolume"

    demo_pump.handle_key("3")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Pump Volume In", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("4")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Pump Volume Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Pump Volume Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.handle_key("4")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Pump Volume In", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
