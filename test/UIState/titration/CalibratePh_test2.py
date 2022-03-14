from unittest import mock
from titration.utils.UIState.titration.CalibratePh import CalibratePh
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(mock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.handleKey(1)
    assert(calibratePh.subState == 2)

    calibratePh.handleKey('a')
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
def test_loop(mock1, mock2):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    assert(calibratePh.values['buffer1_actual_ph'] == 5.5)

    calibratePh.subState += 1
    calibratePh.loop()
    mock1.called_with("to continue", style=constants.LCD_CENT_JUST, line=4)

@mock.patch.object(interfaces, "lcd_out")
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(CalibratePh, "_setNextState")
def test_CalibratePh(mock1, mock2, mock3):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    assert(calibratePh.values['buffer1_actual_ph'] == 5.5)

    calibratePh.handleKey(1)
    assert(calibratePh.subState == 2)

    calibratePh.loop()
    mock1.called_with("to continue", style=constants.LCD_CENT_JUST, line=4)

    calibratePh.handleKey('a')
    assert mock3.called
    