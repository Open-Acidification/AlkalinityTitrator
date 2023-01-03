from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.calibration.setup_calibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "CalibratePh"
    updateStateMock.reset_called()

    setupCalibration.handleKey("2")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "CalibrateTemp"
    updateStateMock.reset_called()

    setupCalibration.handleKey("3")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )


# Test SetupCalibration
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_SetupCalibration(lcdOutMock, updateStateMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1. pH", line=1),
            mock.call("2. Temperature", line=2),
            mock.call("3. Return", line=3),
            mock.call("", line=4),
        ]
    )

    setupCalibration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "CalibratePh"
