"""
The file to test the Volume class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.volume_to_move import VolumeToMove


@mock.patch.object(VolumeToMove, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Volume's handle_key function for each keypad input
    """
    volume = VolumeToMove(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.handle_key("A")
    set_next_state_mock.assert_not_called()

    volume.value = "1"
    volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    volume.handle_key("C")
    assert volume.value == ""

    volume.handle_key("1")
    assert volume.value[-1] == "1"

    volume.handle_key("*")
    assert volume.value[-1] == "."


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test Volume's loop function's LiquidCrystal calls
    """
    volume = VolumeToMove(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )


@mock.patch.object(VolumeToMove, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_volume_to_move(print_mock, set_next_state_mock):
    """
    The function to test a use case of the Volume class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    volume = VolumeToMove(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("3")
    assert volume.value == "3"

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("*")
    assert volume.value == "3."

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("*")
    assert volume.value == "3."

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("1")
    assert volume.value == "3.1"

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("B")
    assert volume.value == "3."

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("B")
    assert volume.value == "3"

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("C")
    assert volume.value == ""

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("A")
    set_next_state_mock.assert_not_called()
    assert volume.value == ""

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("1")
    assert volume.value == "1"

    volume.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Volume to move:", line=1),
            mock.call("1", style="center", line=2),
            mock.call("*=. A)ccept B)ack", line=3, style="center"),
            mock.call("D)ecline  C)lear", line=4, style="center"),
        ]
    )

    volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert volume.titrator.volume_to_move == 1.0
