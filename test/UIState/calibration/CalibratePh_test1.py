from unittest import mock
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(mock):
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.handleKey('a')
    assert not mock.called
    mock.reset_call()

    calibratePh.subState += 1
    calibratePh.handleKey('a')
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(interfaces, 'lcd_out')
def test_loop(mock1, mock2):
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.loop()
    assert(calibratePh.values['buffer1_actual_pH'] == 5.5)
    assert(calibratePh.subState == 2)

    calibratePh.loop()
    assert mock1.called_with("to continue", style=constants.LCD_CENT_JUST, line=4)

def test_CalibratePh():
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.loop()
    assert(calibratePh.subState == 2)

    calibratePh    
