from unittest import mock
from titration.utils.UIState.calibration.CalibrateTemp import CalibrateTemp
from titration.utils.titrator import Titrator
from titration.utils import constants, interfaces, LCD

# Test handleKey
@mock.patch.object(CalibrateTemp, "_setNextState")
def test_handleKey(mock):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 2)

    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 3)

    calibrateTemp.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
def test_loop(mock1, mock2):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.loop()
    assert(calibrateTemp.values['expected_temperature'] == 5.5)

    calibrateTemp.subState += 1 
    calibrateTemp.loop()
    mock2.assert_has_calls(
        [mock.call("Put probe in sol", style=constants.LCD_CENT_JUST, line=1),
        mock.call("", line=2),
        mock.call("Press 1 to", style=constants.LCD_CENT_JUST, line=3),
        mock.call("record value", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock2.reset_called()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    mock2.assert_has_calls(
        [mock.call("Recorded temp:", line=1),
        mock.call("{0:0.3f}".format(calibrateTemp.values['actual_temperature']), line=2),
        mock.call("{}".format(calibrateTemp.values['new_ref_resistance']), line=3)]
    )

# Test CalibrateTemp
@mock.patch.object(CalibrateTemp, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
def test_CalibrateTemp(mock1, mock2, mock3):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.loop()
    assert(calibrateTemp.values['expected_temperature'] == 5.5)

    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 2)

    calibrateTemp.loop()
    mock2.assert_has_calls(
        [mock.call("Put probe in sol", style=constants.LCD_CENT_JUST, line=1),
        mock.call("", line=2),
        mock.call("Press 1 to", style=constants.LCD_CENT_JUST, line=3),
        mock.call("record value", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock2.reset_called()
    mock2.reset_mock()

    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 3)

    calibrateTemp.loop()
    mock2.assert_has_calls(
        [mock.call("Recorded temp:", line=1),
        mock.call("{0:0.3f}".format(calibrateTemp.values['actual_temperature']), line=2),
        mock.call("{}".format(calibrateTemp.values['new_ref_resistance']), line=3)]
    )

    calibrateTemp.handleKey(1)
    assert mock3.called
