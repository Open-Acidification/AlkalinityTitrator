from unittest import mock
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import interfaces, LCD

# Test handleKey
@mock.patch.object(SetupCalibration, "_setNextState")
def test_handleKey(mock):
    calibratePh = SetupCalibration(Titrator(), Titrator())

    calibratePh.handleKey(1)
    assert mock.called
    mock.reset_mock()

    calibratePh.handleKey(2)
    assert mock.called
    mock.reset_mock()

    calibratePh.handleKey(3)
    assert mock.called
    mock.reset_mock()

    calibratePh.handleKey('a')
    assert not mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock):
    calibratePh = SetupCalibration(Titrator(), Titrator())

    calibratePh.loop()
    assert mock.called_with("3. Return", line=3)

# Test SetupCalibration
@mock.patch.object(SetupCalibration, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
def test_SetupCalibration(mock1, mock2):
    calibratePh = SetupCalibration(Titrator(), Titrator())

    calibratePh.loop()
    assert mock1.called_with("3. Return", line=3)

    calibratePh.handleKey(1)
    assert mock2.called
    mock2.reset_mock()
