"""
The file to test the Volume class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.volume import Volume
from titration.utils import lcd_interface


@mock.patch.object(Volume, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test Volume's handle_key function for each keypad input
    """
    volume = Volume(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    volume.handle_key("C")
    assert volume.value == ""

    volume.handle_key("1")
    assert volume.value[-1] == "1"

    volume.handle_key("*")
    assert volume.value[-1] == "."


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test Volume's loop function's lcd_interface calls
    """
    volume = Volume(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(Volume, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_volume(lcd_out_mock, set_next_state_mock):
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
    volume = Volume(Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())))

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("3")
    assert volume.value == "3"

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("*")
    assert volume.value == "3."

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("*")
    assert volume.value == "3."

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("1")
    assert volume.value == "3.1"

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("B")
    assert volume.value == "3."

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("B")
    assert volume.value == "3"

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("C")
    assert volume.value == ""

    volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    volume.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert volume.titrator.volume == ""
