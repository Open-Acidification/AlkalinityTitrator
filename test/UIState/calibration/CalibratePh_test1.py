import pytest
from unittest import mock
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(mock):
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.subState += 1
    calibratePh.handleKey('a')
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value")
def test_loop1(mock):
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.loop()
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop2(mock):
    calibratePh = CalibratePh(Titrator(), Titrator())

    calibratePh.subState += 1
    calibratePh.loop()
    assert mock.called
