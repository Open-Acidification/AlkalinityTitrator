"""
The file to test the DemoTempControl Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_temp_probe import DemoTempControl


@mock.patch.object(DemoTempControl, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoTempControl's handle_key function for each keypad input
    """
    demo_temp_probe = DemoTempControl(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 2

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.handle_key("2")
    assert demo_temp_probe.substate == 3

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_temp_probe = DemoTempControl(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe One", line=1),
            mock.call("2: Probe Two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.substate = 2
    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe One", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_one.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_one.get_resistance()} Ohms",
                line=3,
                style="center",
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    demo_temp_probe.substate = 3
    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Two", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_two.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_two.get_resistance()} Ohms",
                line=3,
                style="center",
            ),
            mock.call("Any key to continue", line=4),
        ]
    )


@mock.patch.object(DemoTempControl, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test sampling through the options in DemoTempControl
    """
    demo_temp_probe = DemoTempControl(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe One", line=1),
            mock.call("2: Probe Two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 2

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe One", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_one.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_one.get_resistance()} Ohms",
                line=3,
                style="center",
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe One", line=1),
            mock.call("2: Probe Two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("2")
    assert demo_temp_probe.substate == 3

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe Two", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_two.get_temperature()} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temp_probe_two.get_resistance()} Ohms",
                line=3,
                style="center",
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 1

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe One", line=1),
            mock.call("2: Probe Two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
