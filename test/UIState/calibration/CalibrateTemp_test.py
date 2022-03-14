from unittest import mock
from titration.utils.UIState.calibration.CalibrateTemp import CalibrateTemp
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(CalibrateTemp, "_setNextState")
def test_handleKey(mock):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.subState += 1
    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 3)

    calibrateTemp.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
def test_loop(mock1, mock2):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.loop()
    assert(calibrateTemp.values['expected_temperature'] == 5.5)
    assert(calibrateTemp.subState == 2)

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    assert mock2.called_with("record value", style=constants.LCD_CENT_JUST, line=4)
    mock2.reset_mock()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    assert mock2.called_with("{}".format(calibrateTemp.values['new_ref_resistance']), line=2)

# Test CalibrateTemp
@mock.patch.object(CalibrateTemp, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
def test_CalibrateTemp(mock1, mock2, mock3):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.loop()
    assert(calibrateTemp.values['expected_temperature'] == 5.5)
    assert(calibrateTemp.subState == 2)

    calibrateTemp.handleKey(1)

    calibrateTemp.loop()
    assert mock2.called_with("record value", style=constants.LCD_CENT_JUST, line=4)
    mock2.reset_mock()

    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 3)

    calibrateTemp.loop()
    assert mock2.called_with("{}".format(calibrateTemp.values['new_ref_resistance']), line=2)

    calibrateTemp.handleKey(1)
    assert mock3.called
