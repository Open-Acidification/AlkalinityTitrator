"""
The file to test the DemopHProbe Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_ph_probe import DemopHProbe


@mock.patch.object(DemopHProbe, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemopHProbe's handle_key function for each keypad input
    """
    demo_ph_probe = DemopHProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 2

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 1

    demo_ph_probe.handle_key("2")
    assert demo_ph_probe.substate == 3

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 1

    demo_ph_probe.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    demo_ph_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_ph_probe = DemopHProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Voltage", line=1),
            mock.call("2: Get Gain", line=2),
            mock.call("3: Return", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.substate = 2
    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe Voltage:", line=1),
            mock.call(
                f"{demo_ph_probe.titrator.ph_probe.get_voltage()} volts",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.substate = 3
    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe Gain:", line=1),
            mock.call(
                f"{demo_ph_probe.titrator.ph_probe.get_gain()} volts",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(DemopHProbe, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test a use case of the  class:
        User enters "1" to Get Voltage
        User enters "1" to return to pH Probe menu
        User enters "2" to Get Gain
        User enters "1" to return to pH Probe menu
        User enters "D" to return to the main menu
    """
    demo_ph_probe = DemopHProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Voltage", line=1),
            mock.call("2: Get Gain", line=2),
            mock.call("3: Return", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 2

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe Voltage:", line=1),
            mock.call(
                f"{demo_ph_probe.titrator.ph_probe.get_voltage()} volts",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 1

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Voltage", line=1),
            mock.call("2: Get Gain", line=2),
            mock.call("3: Return", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.handle_key("2")
    assert demo_ph_probe.substate == 3

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe Gain:", line=1),
            mock.call(
                f"{demo_ph_probe.titrator.ph_probe.get_gain()} volts",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.handle_key("1")
    assert demo_ph_probe.substate == 1

    demo_ph_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Get Voltage", line=1),
            mock.call("2: Get Gain", line=2),
            mock.call("3: Return", line=3),
            mock.call("", line=4),
        ]
    )

    demo_ph_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
