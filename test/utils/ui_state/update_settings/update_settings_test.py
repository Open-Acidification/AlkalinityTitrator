"""
The file to test the UpdateSettings class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils import lcd_interface


@mock.patch.object(UpdateSettings, "_set_next_state")
def test_handle_key_update(set_next_state_mock):
    """
    The function to test UpdateSettings' handle_key function for each keypad input
    when a user wants to update settings
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.handle_key("y")
    assert update_settings.substate == 2

    update_settings.handle_key("1")
    assert update_settings.substate == 3

    update_settings.handle_key("y")
    assert update_settings.substate == 4

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert update_settings.substate == 5

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(UpdateSettings, "_set_next_state")
def test_handle_key_no_update(set_next_state_mock):
    """
    The function to test UpdateSettings' handle_key function for each keypad input
    when a user does not want to update settings
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.handle_key("n")
    assert update_settings.substate == 3

    update_settings.handle_key("n")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test UpdateSettings' loop function's lcd_interface calls
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Reset calibration", line=1),
            mock.call("settings to default?", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.substate += 1
    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Default constants", line=1),
            mock.call("restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.substate += 1
    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set volume in pump?", line=1),
            mock.call("", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.substate += 1
    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.substate += 1
    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump set", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(UpdateSettings, "_set_next_state")
@mock.patch.object(lcd_interface, "lcd_out")
def test_prime_pump(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "y" to set calibration settings to default
        User enters "1" to continue
        User enters "y" to set volume in pump
        User enters "1" to continue
        User enters "1" to return to the main menu
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Reset calibration", line=1),
            mock.call("settings to default?", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("y")
    assert update_settings.substate == 2

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Default constants", line=1),
            mock.call("restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("1")
    assert update_settings.substate == 3

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Set volume in pump?", line=1),
            mock.call("", line=2),
            mock.call("(y/n)", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("y")
    assert update_settings.substate == 4

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Enter Volume in pump", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UserValue"
    assert update_settings.substate == 5

    update_settings.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Volume in pump set", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
