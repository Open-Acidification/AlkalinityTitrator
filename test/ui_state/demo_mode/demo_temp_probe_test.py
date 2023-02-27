"""
The file to test the DemoTempProbe Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_temp_probe import DemoTempProbe


@mock.patch.object(DemoTempProbe, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoTempProbe's handle_key function for each keypad input
    """
    demo_temp_probe = DemoTempProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 2

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.handle_key("2")
    assert demo_temp_probe.substate == 3

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    demo_temp_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_temp_probe = DemoTempProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Temperature", line=1),
            mock.call("2: Get Resistance", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.substate = 2
    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Temperature", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_sensor.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_temp_probe.substate = 3
    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Resistance", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_sensor.get_resistance()} Ohms",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(DemoTempProbe, "_set_next_state")
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
    demo_temp_probe = DemoTempProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Temperature", line=1),
            mock.call("2: Get Resistance", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 2

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Temperature", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_sensor.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Temperature", line=1),
            mock.call("2: Get Resistance", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("2")
    assert demo_temp_probe.substate == 3

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Resistance", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_sensor.get_resistance()} Ohms",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Temperature", line=1),
            mock.call("2: Get Resistance", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
