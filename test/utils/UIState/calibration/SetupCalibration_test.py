from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import LCD

# Test handleKey
@mock.patch.object(SetupCalibration, "_setNextState")
def test_handleKey(mock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "CalibratePh")
    mock.reset_mock()

    setupCalibration.handleKey("2")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "CalibrateTemp")
    mock.reset_mock()

    setupCalibration.handleKey("3")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

    setupCalibration.handleKey('a')
    assert not mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    assert mock.called_with("3. Return", line=3)

# Test SetupCalibration
@mock.patch.object(SetupCalibration, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
def test_SetupCalibration(mock1, mock2):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    assert mock1.called_with("3. Return", line=3)

    setupCalibration.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "CalibratePh")
    mock2.reset_mock()
