"""
The file to test the CalibrateTemp class
"""
from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, TemperatureProbe
from titration.titrator import Titrator
from titration.ui_state.calibration.calibrate_temp import CalibrateTemp
from titration.ui_state.calibration.setup_calibration import SetupCalibration
from titration.ui_state.main_menu import MainMenu


@mock.patch.object(TemperatureProbe, "calibrate")
@mock.patch.object(CalibrateTemp, "_set_next_state")
def test_handle_key(_set_next_state, calibrate):
    """
    The function to test CalibrateTemp's handle_key function for each keypad input
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "ReferenceTemperature"
    assert calibrate_temp.substate == 2

    calibrate_temp.handle_key("1")
    calibrate.assert_called()
    assert calibrate_temp.substate == 3

    calibrate_temp.handle_key("1")
    assert calibrate_temp.substate == 4

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "ReferenceTemperature"
    assert calibrate_temp.substate == 5

    calibrate_temp.handle_key("1")
    calibrate.assert_called()
    assert calibrate_temp.substate == 6

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "SetupCalibration"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print_mock):
    """
    The function to test CalibrateTemp's loop function's LiquidCrystal calls
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set probe one", line=1),
            mock.call("reference", line=2),
            mock.call("temperature", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.substate = 2
    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put probe one in", line=1),
            mock.call("solution", line=2),
            mock.call("Press any key to", line=3),
            mock.call("record temperature", line=4),
        ]
    )

    calibrate_temp.substate = 3
    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe one", line=1),
            mock.call(
                f"{(calibrate_temp.titrator.temperature_probe_control.get_temperature()):4.3f}",
                line=2,
            ),
            mock.call(
                f"{calibrate_temp.titrator.temperature_probe_control.get_resistance()}",
                line=3,
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.substate = 4
    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set probe two", line=1),
            mock.call("reference", line=2),
            mock.call("temperature", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.substate = 5
    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put probe two in", line=1),
            mock.call("solution", line=2),
            mock.call("Press any key to", line=3),
            mock.call("record temperature", line=4),
        ]
    )

    calibrate_temp.substate = 6
    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe two", line=1),
            mock.call(
                f"{(calibrate_temp.titrator.temperature_probe_logging.get_temperature()):>4.3f}",
                line=2,
            ),
            mock.call(
                f"{calibrate_temp.titrator.temperature_probe_logging.get_resistance()}",
                line=3,
            ),
            mock.call("Any key to continue", line=4),
        ]
    )


@mock.patch.object(TemperatureProbe, "calibrate")
@mock.patch.object(CalibrateTemp, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_calibrate_temp(print_mock, _set_next_state, calibrate):
    """
    The function to test a use case of the CalibrateTemp class:
        User enters "1" to continue setting reference solution
        User enters "1" after probe has entered solution to record value
        User enters "1" to continue setting up calibration
    """
    calibrate_temp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set probe one", line=1),
            mock.call("reference", line=2),
            mock.call("temperature", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "ReferenceTemperature"
    assert calibrate_temp.substate == 2

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put probe one in", line=1),
            mock.call("solution", line=2),
            mock.call("Press any key to", line=3),
            mock.call("record temperature", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    calibrate.assert_called()
    assert calibrate_temp.substate == 3

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe one", line=1),
            mock.call(
                f"{(calibrate_temp.titrator.temperature_probe_control.get_temperature()):4.3f}",
                line=2,
            ),
            mock.call(
                f"{calibrate_temp.titrator.temperature_probe_control.get_resistance()}",
                line=3,
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    assert calibrate_temp.substate == 4

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Set probe two", line=1),
            mock.call("reference", line=2),
            mock.call("temperature", line=3),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "ReferenceTemperature"
    assert calibrate_temp.substate == 5

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Put probe two in", line=1),
            mock.call("solution", line=2),
            mock.call("Press any key to", line=3),
            mock.call("record temperature", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    calibrate.assert_called()
    assert calibrate_temp.substate == 6

    calibrate_temp.loop()
    print_mock.assert_has_calls(
        [
            mock.call("Probe two", line=1),
            mock.call(
                f"{(calibrate_temp.titrator.temperature_probe_logging.get_temperature()):>4.3f}",
                line=2,
            ),
            mock.call(
                f"{calibrate_temp.titrator.temperature_probe_logging.get_resistance()}",
                line=3,
            ),
            mock.call("Any key to continue", line=4),
        ]
    )

    calibrate_temp.handle_key("1")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "SetupCalibration"
