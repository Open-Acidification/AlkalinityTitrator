from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface, constants

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

# Test loop
@mock.patch.object(LCD_interface, "display_list")
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(mock1, mock2):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    assert mock1.called_with("3. Return", line=3)
    assert mock2.called_with(constants.SENSOR_OPTIONS)

# Test SetupCalibration
@mock.patch.object(LCD_interface, "display_list")
@mock.patch.object(SetupCalibration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_SetupCalibration(mock1, mock2, mock3):
    setupCalibration = SetupCalibration(Titrator(), MainMenu(Titrator()))

    setupCalibration.loop()
    assert mock1.called_with("3. Return", line=3)
    assert mock3.called_with(constants.SENSOR_OPTIONS)
    mock3.reset_called()

    setupCalibration.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "CalibratePh")
    mock2.reset_mock()
