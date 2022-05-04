from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.CalibratePh import CalibratePh
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(mock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.handleKey("1")
    assert(calibratePh.subState == 2)

    calibratePh.handleKey("a")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "InitialTitration")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
@mock.patch.object(LCD_interface, "read_user_value", return_value=5.5)
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
    mock1.assert_called_with("Enter buffer pH:")
    assert(calibratePh.values['buffer1_actual_pH'] == 5.5)
    mock1.reset_called()

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
@mock.patch.object(LCD_interface, "read_user_value", return_value=5.5)
@mock.patch.object(LCD_interface, "lcd_out")
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
    mock2.assert_called_with("Enter buffer pH:")
    assert(calibratePh.values['buffer1_actual_pH'] == 5.5)
    mock2.reset_called()

    calibratePh.handleKey("1")
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
    mock3.assert_called_with(ANY, True)
    assert(mock3.call_args.args[0].name() == "InitialTitration")
    