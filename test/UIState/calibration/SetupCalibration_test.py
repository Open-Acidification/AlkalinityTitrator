import pytest
from unittest import mock
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

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
@mock.patch.object(interfaces, "display_list")
def test_loop1(mock):
    calibratePh = SetupCalibration(Titrator(), Titrator())

    calibratePh.loop()
    assert mock.called
