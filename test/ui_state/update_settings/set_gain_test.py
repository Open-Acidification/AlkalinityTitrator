"""
The file to test the SetGain class
"""

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, PHProbe
from titration.titrator import Titrator
from titration.ui_state.update_settings.set_gain import SetGain
from titration.ui_state.update_settings.update_settings import UpdateSettings


@mock.patch.object(SetGain, "_set_next_state")
@mock.patch.object(PHProbe, "set_gain")
def test_handle_key_update(set_gain_mock, set_next_state_mock):
    """
    The function to test SetGain' handle_key function for each keypad input
    when a user wants to update settings
    """
    set_gain = SetGain(Titrator(), UpdateSettings(Titrator()))

    set_gain.handle_key("1")
    assert set_gain.user_choice == "2/3"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(2 / 3)

    set_gain.substate = 1
    set_gain.handle_key("2")
    assert set_gain.user_choice == "1"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(1)

    set_gain.substate = 1
    set_gain.handle_key("3")
    assert set_gain.user_choice == "2"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(2)

    set_gain.substate = 1
    assert set_gain.substate == 1
    set_gain.handle_key("4")
    assert set_gain.substate == 2

    set_gain.handle_key("1")
    assert set_gain.user_choice == "4"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(4)

    set_gain.substate = 2
    set_gain.handle_key("2")
    assert set_gain.user_choice == "8"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(8)

    set_gain.substate = 2
    set_gain.handle_key("3")
    assert set_gain.user_choice == "16"
    assert set_gain.substate == 3
    set_gain_mock.assert_called_with(16)

    set_gain.substate = 2
    set_gain.handle_key("4")
    assert set_gain.substate == 1

    set_gain.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test SetGain' loop function's lcd_interface calls
    """
    set_gain = SetGain(Titrator(), UpdateSettings(Titrator()))

    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: 2/3", line=1),
            mock.call("2: 1", line=2),
            mock.call("3: 2", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    set_gain.substate = 2
    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: 4", line=1),
            mock.call("2: 8", line=2),
            mock.call("3: 16", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    set_gain.substate = 3
    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe", line=1),
            mock.call("Gain Set To 1", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(SetGain, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_set_gain(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "1" to set gain
    """
    set_gain = SetGain(Titrator(), UpdateSettings(Titrator()))

    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: 2/3", line=1),
            mock.call("2: 1", line=2),
            mock.call("3: 2", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    set_gain.handle_key("4")
    assert set_gain.substate == 2

    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: 4", line=1),
            mock.call("2: 8", line=2),
            mock.call("3: 16", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    set_gain.handle_key("3")
    assert set_gain.substate == 3

    set_gain.loop()
    print_mock.assert_has_calls(
        [
            mock.call("pH Probe", line=1),
            mock.call("Gain Set To 16", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    set_gain.handle_key("5")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
