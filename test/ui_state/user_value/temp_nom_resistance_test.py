"""
The file to test the TempNomResistance class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal
from titration.titrator import Titrator
from titration.ui_state.update_settings.update_settings import UpdateSettings
from titration.ui_state.user_value.temp_nom_resistance import TempNomResistance


@mock.patch.object(TempNomResistance, "_set_next_state")
def test_handle_key(set_next_state_mock):
    """
    The function to test TempNomResistance's handle_key function for each keypad input
    """
    temp_nom_res = TempNomResistance(Titrator(), UpdateSettings(Titrator()))

    temp_nom_res.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"

    temp_nom_res.handle_key("C")
    assert temp_nom_res.value == ""

    temp_nom_res.handle_key("1")
    assert temp_nom_res.value[-1] == "1"

    temp_nom_res.handle_key("*")
    assert temp_nom_res.value[-1] == "."

    temp_nom_res.handle_key("D")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test TempNomResistance's loop function's LiquidCrystal calls
    """
    temp_nom_res = TempNomResistance(Titrator(), UpdateSettings(Titrator()))

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )


@mock.patch.object(TempNomResistance, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_ph_ref_ph(print_mock, set_next_state_mock):
    """
    The function to test a use case of the TempNomResistance class:
        User enters "3"
        User enters "."
        User enters "."
        User enters "1"
        User backspaces
        User backspaces
        User clears
        User accepts
    """
    temp_nom_res = TempNomResistance(Titrator(), UpdateSettings(Titrator()))

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("3")
    assert temp_nom_res.value == "3"

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("*")
    assert temp_nom_res.value == "3."

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("*")
    assert temp_nom_res.value == "3."

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("1")
    assert temp_nom_res.value == "3.1"

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3.1", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("B")
    assert temp_nom_res.value == "3."

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3.", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("B")
    assert temp_nom_res.value == "3"

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("3", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("C")
    assert temp_nom_res.value == ""

    temp_nom_res.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Temp Nom Resistance:", line=1),
            mock.call("", style="center", line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )

    temp_nom_res.handle_key("A")
    set_next_state_mock.assert_called_with(ANY, True)
    assert set_next_state_mock.call_args.args[0].name() == "UpdateSettings"
    assert temp_nom_res.value == ""
