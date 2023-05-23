"""
The file to test the DemoTemperatureControl Class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, TemperatureControl
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_temperature_controller import (
    DemoTemperatureControl,
)


@mock.patch.object(TemperatureControl, "deactivate")
@mock.patch.object(TemperatureControl, "activate")
@mock.patch.object(TemperatureControl, "heater_off")
@mock.patch.object(TemperatureControl, "heater_on")
@mock.patch.object(DemoTemperatureControl, "_set_next_state")
def test_handle_key(
    set_next_state_mock, heater_on_mock, heater_off_mock, activate_mock, deactivate_mock
):
    """
    The function to test the DemoTemperatureControl's handle_key function for each keypad input
    """
    demo_temperature_controller = DemoTemperatureControl(
        Titrator(), DemoModeMenu(Titrator())
    )

    demo_temperature_controller.handle_key("1")
    heater_on_mock.assert_called()
    assert demo_temperature_controller.substate == 2

    demo_temperature_controller.handle_key("1")
    deactivate_mock.assert_called()
    heater_off_mock.assert_called()
    assert demo_temperature_controller.substate == 1

    demo_temperature_controller.handle_key("2")
    activate_mock.assert_called()
    assert demo_temperature_controller.substate == 3

    demo_temperature_controller.handle_key("1")
    deactivate_mock.assert_called()
    heater_off_mock.assert_called()
    assert demo_temperature_controller.substate == 1

    demo_temperature_controller.handle_key("4")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"

    demo_temperature_controller.handle_key("D")
    deactivate_mock.assert_called()
    heater_off_mock.assert_called()
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_temperature_controller = DemoTemperatureControl(
        Titrator(), DemoModeMenu(Titrator())
    )

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Turn Heater On", line=1),
            mock.call("2: Temp Controller", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temperature_controller.substate = 2
    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heater is on", line=1),
            mock.call("Current Temperature:", line=2),
            mock.call(
                f"{demo_temperature_controller.titrator.temp_probe_one.get_temperature()} C",
                line=3,
                style="center",
            ),
            mock.call("Any key to turn off", line=4),
        ]
    )

    demo_temperature_controller.substate = 3
    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Controller On", line=1),
            mock.call("Current Temperature:", line=2),
            mock.call(
                f"{demo_temperature_controller.titrator.temp_probe_one.get_temperature()} C",
                line=3,
                style="center",
            ),
            mock.call("Any key to turn off", line=4),
        ]
    )


@mock.patch.object(DemoTemperatureControl, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print_mock, set_next_state_mock):
    """
    The function to test sampling through the options in DemoTemperatureControl
    """
    demo_temperature_controller = DemoTemperatureControl(
        Titrator(), DemoModeMenu(Titrator())
    )

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Turn Heater On", line=1),
            mock.call("2: Temp Controller", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temperature_controller.handle_key("1")
    assert demo_temperature_controller.substate == 2

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Heater is on", line=1),
            mock.call("Current Temperature:", line=2),
            mock.call(
                f"{demo_temperature_controller.titrator.temp_probe_one.get_temperature()} C",
                line=3,
                style="center",
            ),
            mock.call("Any key to turn off", line=4),
        ]
    )

    demo_temperature_controller.handle_key("1")
    assert demo_temperature_controller.substate == 1

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Turn Heater On", line=1),
            mock.call("2: Temp Controller", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temperature_controller.handle_key("2")
    assert demo_temperature_controller.substate == 3

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Controller On", line=1),
            mock.call("Current Temperature:", line=2),
            mock.call(
                f"{demo_temperature_controller.titrator.temp_probe_one.get_temperature()} C",
                line=3,
                style="center",
            ),
            mock.call("Any key to turn off", line=4),
        ]
    )

    demo_temperature_controller.handle_key("1")
    assert demo_temperature_controller.substate == 1

    demo_temperature_controller.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Turn Heater On", line=1),
            mock.call("2: Temp Controller", line=2),
            mock.call("", line=3),
            mock.call("4: Return", line=4),
        ]
    )

    demo_temperature_controller.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "DemoModeMenu"
