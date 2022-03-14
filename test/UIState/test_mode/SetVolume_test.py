from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
from titration.utils.UIState.test_mode.SetVolume import SetVolume

# Test handleKey
@mock.patch.object(SetVolume, "_setNextState")
def test_handleKey(mock):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, 'read_user_value', return_value=5.5)
def test_loop(mock):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.loop()
    assert(setVolume.values['new_volume'] == 5.5)

# Test SetVolume
@mock.patch.object(SetVolume, "_setNextState")
@mock.patch.object(interfaces, 'read_user_value', return_value=5.5)
def test_SetVolume(mock1, mock2):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.loop()
    assert(setVolume.values['new_volume'] == 5.5)

    setVolume.handleKey(1)
    assert mock2.called
