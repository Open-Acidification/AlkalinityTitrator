from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
@mock.patch.object(SetupCalibration, "_setNextState")
def test_handleKey(setNextStateMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "CalibratePh")
    setNextStateMock.reset_called()

    setupCalibration.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "CalibrateTemp")
    setNextStateMock.reset_called()

    setupCalibration.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "MainMenu")

# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("1. pH", line=1), 
        mock.call("2. Temperature", line=2),
        mock.call("3. Return", line=3),
        mock.call("", line=4)
    ])

# Test SetupCalibration
@mock.patch.object(SetupCalibration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_SetupCalibration(lcdOutMock, setNextStateMock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("1. pH", line=1), 
        mock.call("2. Temperature", line=2),
        mock.call("3. Return", line=3),
        mock.call("", line=4)
    ])

    setupCalibration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "CalibratePh")
