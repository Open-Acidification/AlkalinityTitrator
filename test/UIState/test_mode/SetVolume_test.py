from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.SetVolume import SetVolume

# Test handleKey
@mock.patch.object(SetVolume, "_setNextState")
def test_handleKey(mock):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_loop(mock1, mock2):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.loop()
    mock2.assert_has_calls(
        [mock.call("Press any to cont.", line=1)]
    )
    assert(setVolume.values['new_volume'] == 5.5)

# Test SetVolume
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(SetVolume, "_setNextState")
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_SetVolume(mock1, mock2, mock3):
    setVolume = SetVolume(Titrator(), Titrator())

    setVolume.loop()
    mock3.assert_has_calls(
        [mock.call("Press any to cont.", line=1)]
    )
    assert(setVolume.values['new_volume'] == 5.5)

    setVolume.handleKey(1)
    assert mock2.called
