"""
The file to test the ReferenceTemperature class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.reference_temperature import (
    ReferenceTemperature,
)


@mock.patch.object(ReferenceTemperature, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReferenceTemperature's handle_key function for each keypad input
    """
    reference_temperature = ReferenceTemperature(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    reference_temperature.handle_key("A")
    set_next_state_mock.assert_not_called()

    reference_temperature.value = "1"
    reference_temperature.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    reference_temperature.handle_key("C")
    assert reference_temperature.value == ""

    reference_temperature.handle_key("1")
    assert reference_temperature.value[-1] == "1"

    reference_temperature.handle_key("*")
    assert reference_temperature.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test ReferenceTemperature's loop function's LiquidCrystal calls
    """
    reference_temperature = ReferenceTemperature(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )


@mock.patch.object(ReferenceTemperature, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_reference_temperature(print_mock, set_next_state_mock):
    """
    The function to test a use case of the ReferenceTemperature class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    reference_temperature = ReferenceTemperature(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("3")
    assert reference_temperature.value == "3"

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("*")
    assert reference_temperature.value == "3."

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("*")
    assert reference_temperature.value == "3."

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("1")
    assert reference_temperature.value == "3.1"

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("B")
    assert reference_temperature.value == "3."

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("B")
    assert reference_temperature.value == "3"

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("C")
    assert reference_temperature.value == ""

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("A")
    set_next_state_mock.assert_not_called()
    assert reference_temperature.value == ""

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("1")
    assert reference_temperature.value == "1"

    reference_temperature.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Reference temp (C):", line=1),
            mock.call("1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    reference_temperature.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert reference_temperature.titrator.reference_temperature == 1.0
