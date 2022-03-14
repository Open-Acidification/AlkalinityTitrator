from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
from titration.utils.UIState.test_mode.ReadVolume import ReadVolume

# Test handleKey
@mock.patch.object(ReadVolume, "_setNextState")
def test_handleKey(mock):
    readVolume = ReadVolume(Titrator(), Titrator())

    readVolume.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, 'lcd_out')
def test_loop(mock):
    readVolume = ReadVolume(Titrator(), Titrator())

    readVolume.loop()
    assert mock.called_with("Press any to cont.", line=3)

# Test ReadVolume
@mock.patch.object(ReadVolume, "_setNextState")
@mock.patch.object(interfaces, 'lcd_out')
def test_ReadVolume(mock1, mock2):
    readVolume = ReadVolume(Titrator(), Titrator())

    readVolume.loop()
    assert mock1.called_with("Press any to cont.", line=3)

    readVolume.handleKey(1)
    assert mock2.called
