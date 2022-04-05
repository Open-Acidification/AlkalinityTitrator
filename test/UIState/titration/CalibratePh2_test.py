from unittest import mock
from titration.utils.UIState.titration.CalibratePh import CalibratePh
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD

# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(mock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.handleKey(1)
    assert(calibratePh.subState == 2)

    calibratePh.handleKey('a')
    assert mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
def test_loop(mock1, mock2):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    mock2.assert_has_calls(
        [mock.call("Put sensor in buffer", style=constants.LCD_CENT_JUST, line=1),
        mock.call("", line=2),
        mock.call("Press any button", style=constants.LCD_CENT_JUST, line=3),
        mock.call("to record value", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock2.reset_called()
    assert(calibratePh.values['buffer1_actual_pH'] == 5.5)

    calibratePh.subState += 1
    calibratePh.loop()
    mock2.assert_has_calls(
        [mock.call("Recorded pH, volts:", line=1),
        mock.call(
                "{0:>2.5f} pH, {1:>3.4f} V".format(calibratePh.values['buffer1_actual_pH'], calibratePh.values['buffer1_measured_volts']),
                line=2,
            ),
        mock.call("Press any button", style=constants.LCD_CENT_JUST, line=3),
        mock.call("to continue", style=constants.LCD_CENT_JUST, line=4)]
    )

@mock.patch.object(CalibratePh, "_setNextState")
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
@mock.patch.object(LCD, "lcd_out")
def test_CalibratePh(mock1, mock2, mock3):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    mock1.assert_has_calls(
        [mock.call("Put sensor in buffer", style=constants.LCD_CENT_JUST, line=1),
        mock.call("", line=2),
        mock.call("Press any button", style=constants.LCD_CENT_JUST, line=3),
        mock.call("to record value", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock1.reset_called()
    assert(calibratePh.values['buffer1_actual_pH'] == 5.5)

    calibratePh.handleKey(1)
    assert(calibratePh.subState == 2)

    calibratePh.loop()
    mock1.assert_has_calls(
        [mock.call("Recorded pH, volts:", line=1),
        mock.call(
            "{0:>2.5f} pH, {1:>3.4f} V".format(calibratePh.values['buffer1_actual_pH'], calibratePh.values['buffer1_measured_volts']),
            line=2,
        ),
        mock.call("Press any button", style=constants.LCD_CENT_JUST, line=3),
        mock.call("to continue", style=constants.LCD_CENT_JUST, line=4)]
    )

    calibratePh.handleKey('a')
    assert mock3.called
    