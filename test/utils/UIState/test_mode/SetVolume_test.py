from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import LCD
from titration.utils.UIState.test_mode.SetVolume import SetVolume

# Test handleKey
@mock.patch.object(SetVolume, "_setNextState")
def test_handleKey(mock):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_loop(mock1, mock2):
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

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
    setVolume = SetVolume(Titrator(), MainMenu(Titrator()))

    setVolume.loop()
    mock3.assert_has_calls(
        [mock.call("Press any to cont.", line=1)]
    )
    assert(setVolume.values['new_volume'] == 5.5)

    setVolume.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "MainMenu")
    mock2.reset_mock()
