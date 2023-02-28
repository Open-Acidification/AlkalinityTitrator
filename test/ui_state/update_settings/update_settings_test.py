"""
The file to test the UpdateSettings class
"""
from unittest import mock
from unittest.mock import ANY

from titration import constants
from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.main_menu import MainMenu
from titration.ui_state.update_settings.update_settings import UpdateSettings


@mock.patch.object(UpdateSettings, "_set_next_state")
def test_handle_key_update(set_next_state_mock):
    """
    The function to test UpdateSettings' handle_key function for each keypad input
    when a user wants to update settings
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.handle_key("1")
    assert update_settings.substate == 4

    update_settings.substate = 1
    update_settings.handle_key("2")
    assert constants.TEMPERATURE_REF_RESISTANCE == 4300.0
    assert constants.TEMPERATURE_NOMINAL_RESISTANCE == 1000.0
    assert constants.PH_REF_VOLTAGE == -0.012
    assert constants.PH_REF_PH == 7.0
    assert update_settings.substate == 5

    update_settings.substate = 1
    update_settings.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TempRefResistance"

    update_settings.substate = 1
    update_settings.handle_key("4")
    assert update_settings.substate == 2

    update_settings.substate = 2
    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "TempNomResistance"

    update_settings.substate = 2
    update_settings.handle_key("2")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PHRefVoltage"

    update_settings.substate = 2
    update_settings.handle_key("3")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "PHRefpH"

    update_settings.substate = 2
    update_settings.handle_key("4")
    assert update_settings.substate == 3

    update_settings.substate = 3
    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetGain"

    update_settings.substate = 3
    update_settings.handle_key("4")
    assert update_settings.substate == 1

    update_settings.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test UpdateSettings' loop function's lcd_interface calls
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: View Settings", line=1),
            mock.call("2: Default Settings", line=2),
            mock.call("3: T Ref Resistance", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    update_settings.substate = 2
    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: T Nom Resistance", line=1),
            mock.call("2: pH Ref Voltage", line=2),
            mock.call("3: pH Ref pH", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    update_settings.substate = 3
    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Gain", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    update_settings.substate = 4
    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call(f"T Ref Res: {constants.TEMPERATURE_REF_RESISTANCE}", line=1),
            mock.call(f"T Nom Res: {constants.TEMPERATURE_NOMINAL_RESISTANCE}", line=2),
            mock.call(f"pH Ref Vol: {constants.PH_REF_VOLTAGE}", line=3),
            mock.call(f"pH Ref pH: {constants.PH_REF_PH}", line=4),
        ]
    )

    update_settings.substate = 5
    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Default Constants", line=1),
            mock.call("Restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(UpdateSettings, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_update_settings(print_mock, set_next_state_mock):
    """
    The function to test a use case of the PrimePump class:
        User enters "1" to View Settings
        User enters "1" to return to Update Settings Menu
        User enters "2" to set Default Values
        User enters "4" to go to second page
        User enters "4" to go to third page
        User enters "1" to Set Gain
        User enters "4" to go to Page 1
        User enters "D" to return to Main Menu
    """
    update_settings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: View Settings", line=1),
            mock.call("2: Default Settings", line=2),
            mock.call("3: T Ref Resistance", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    update_settings.handle_key("1")
    assert update_settings.substate == 4

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call(f"T Ref Res: {constants.TEMPERATURE_REF_RESISTANCE}", line=1),
            mock.call(f"T Nom Res: {constants.TEMPERATURE_NOMINAL_RESISTANCE}", line=2),
            mock.call(f"pH Ref Vol: {constants.PH_REF_VOLTAGE}", line=3),
            mock.call(f"pH Ref pH: {constants.PH_REF_PH}", line=4),
        ]
    )

    update_settings.handle_key("1")
    assert update_settings.substate == 1

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: View Settings", line=1),
            mock.call("2: Default Settings", line=2),
            mock.call("3: T Ref Resistance", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    update_settings.handle_key("2")
    assert constants.TEMPERATURE_REF_RESISTANCE == 4300.0
    assert constants.TEMPERATURE_NOMINAL_RESISTANCE == 1000.0
    assert constants.PH_REF_VOLTAGE == -0.012
    assert constants.PH_REF_PH == 7.0
    assert update_settings.substate == 5

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Default Constants", line=1),
            mock.call("Restored", line=2),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    update_settings.handle_key("1")
    assert update_settings.substate == 1

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: View Settings", line=1),
            mock.call("2: Default Settings", line=2),
            mock.call("3: T Ref Resistance", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    update_settings.handle_key("4")
    assert update_settings.substate == 2

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: T Nom Resistance", line=1),
            mock.call("2: pH Ref Voltage", line=2),
            mock.call("3: pH Ref pH", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    update_settings.handle_key("4")
    assert update_settings.substate == 3

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: Set Gain", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    update_settings.handle_key("1")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "SetGain"

    update_settings.handle_key("4")
    assert update_settings.substate == 1

    update_settings.loop()
    print_mock.assert_has_calls(
        [
            mock.call("1: View Settings", line=1),
            mock.call("2: Default Settings", line=2),
            mock.call("3: T Ref Resistance", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    update_settings.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "MainMenu"
