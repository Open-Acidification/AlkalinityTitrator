"""
The file to test the DemoTemperatureProbe Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_temperature_probe import (
    DemoTemperatureProbe,
)


@mock.patch.object(DemoTemperatureProbe, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test the DemoTemperatureProbe's handle_key function for each keypad input
    """
    demo_temp_probe = DemoTemperatureProbe(Titrator(), DemoModeMenu(Titrator()))

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
    demo_temp_probe = DemoTemperatureProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe one", line=1),
            mock.call("2: Probe two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.substate = 2
    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe one", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_control.get_temperature():>4.3f} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_control.get_resistance()} Ohms",
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
            mock.call("Probe two", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_logging.get_temperature():>4.3f} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_logging.get_resistance()} Ohms",
                line=3,
                style="center",
            ),
            mock.call("Any key to continue", line=4),
        ]
    )


@mock.patch.object(DemoTemperatureProbe, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test sampling through the options in DemoTemperatureProbe
    """
    demo_temp_probe = DemoTemperatureProbe(Titrator(), DemoModeMenu(Titrator()))

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Probe one", line=1),
            mock.call("2: Probe two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("1")
    assert demo_temp_probe.substate == 2

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe one", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_control.get_temperature():>4.3f} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_control.get_resistance()} Ohms",
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
            mock.call("1: Probe one", line=1),
            mock.call("2: Probe two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("2")
    assert demo_temp_probe.substate == 3

    demo_temp_probe.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe two", line=1),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_logging.get_temperature():>4.3f} C",
                line=2,
                style="center",
            ),
            mock.call(
                f"{demo_temp_probe.titrator.temperature_probe_logging.get_resistance()} Ohms",
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
            mock.call("1: Probe one", line=1),
            mock.call("2: Probe two", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temp_probe.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
