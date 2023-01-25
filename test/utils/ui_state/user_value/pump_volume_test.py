"""
The file to test the PumpVolume class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.pump_volume import (
    PumpVolume,
)
from titration.utils import lcd_interface


@mock.patch.object(PumpVolume, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test PumpVolume's handle_key function for each keypad input
    """
    pump_volume = PumpVolume(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    pump_volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    pump_volume.handle_key("C")
    assert pump_volume.string == ""

    pump_volume.handle_key("1")
    assert pump_volume.string[-1] == "1"

    pump_volume.handle_key("*")
    assert pump_volume.string[-1] == "."


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test PumpVolume's loop function's lcd_interface calls
    """
    pump_volume = PumpVolume(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(PumpVolume, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_pump_volume(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the PumpVolume class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    pump_volume = PumpVolume(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator()))
    )

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("3")
    assert pump_volume.string == "3"

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("*")
    assert pump_volume.string == "3."

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("*")
    assert pump_volume.string == "3."

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("1")
    assert pump_volume.string == "3.1"

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("B")
    assert pump_volume.string == "3."

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("B")
    assert pump_volume.string == "3"

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("C")
    assert pump_volume.string == ""

    pump_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    pump_volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert pump_volume.titrator.pump_volume == ""
