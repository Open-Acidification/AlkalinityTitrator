import pytest
from unittest import mock
from titration.utils.UIState.calibration.CalibrateTemp import CalibrateTemp
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

# Test handleKey
@mock.patch.object(CalibrateTemp, "_setNextState")
def test_handleKey(mock):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.subState += 1
    calibrateTemp.handleKey(1)
    assert(calibrateTemp.subState == 3)

    calibrateTemp.handleKey('')
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value")
def test_loop1(mock):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.loop()
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop2(mock):
    calibrateTemp = CalibrateTemp(Titrator(), Titrator())

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    assert mock.called
    mock.reset_mock()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    assert mock.called
