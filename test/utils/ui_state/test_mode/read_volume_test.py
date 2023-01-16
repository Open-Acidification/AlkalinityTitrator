"""
The file to test the ReadVolume class
"""
from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.test_mode.read_volume import ReadVolume
from titration.utils.ui_state.test_mode.test_mode import TestMode


@mock.patch.object(ReadVolume, "_setNextState")
def test_handle_key(set_next_state_mock):
    """
    The function to test ReadVolume's handle_key function for each keypad input
    """
    read_volume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_volume.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"


@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcd_out_mock):
    """
    The function to test SetVolume's loop function's lcd_interface calls
    """
    read_volume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                "{0:1.2f}".format(constants.volume_in_pump),
                style=constants.LCD_CENT_JUST,
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ReadVolume, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_read_volume(lcd_out_mock, set_next_state_mock):
    """
    The function to test a use case of the SetVolume class:
        User enters "1" to continue after the pump volume is read
    """
    read_volume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    read_volume.loop()
    lcd_out_mock.assert_has_calls(
        [
            mock.call("Pump Vol: ", line=1),
            mock.call(
                "{0:1.2f}".format(constants.volume_in_pump),
                style=constants.LCD_CENT_JUST,
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    read_volume.handleKey("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TestMode"
