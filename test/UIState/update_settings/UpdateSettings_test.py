from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
from titration.utils.UIState.update_settings.UpdateSettings import UpdateSettings

# Test handleKey
@mock.patch.object(UpdateSettings, "_setNextState")
def test_handleKey(mock):
    updateSettings = UpdateSettings(Titrator(), Titrator())

    updateSettings.handleKey('y')
    assert(updateSettings.subState == 2)

    updateSettings.handleKey('a')
    assert(updateSettings.subState == 3)

    updateSettings.handleKey('y')
    assert(updateSettings.subState == 4)

    updateSettings.handleKey('a')
    assert mock.called
    mock.reset_called()

    updateSettings = UpdateSettings(Titrator(), Titrator())

    updateSettings.handleKey('n')
    assert(updateSettings.subState == 3)

    updateSettings.handleKey('n')
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock1, mock2):
    updateSettings = UpdateSettings(Titrator(), Titrator())

    updateSettings.loop()
    mock1.assert_called_with("(y/n)", line=3)
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_called_with("Press any to cont.", line=3)
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_called_with("(y/n)", line=3)
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    assert(updateSettings.values['vol_in_pump'] == 5.5)

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_called_with("Press any to cont.", line=3)

# Test UpdateSettings
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(UpdateSettings, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
def test_PrimePump(mock1, mock2, mock3):
    updateSettings = UpdateSettings(Titrator(), Titrator())

    updateSettings.loop()
    mock1.assert_called_with("(y/n)", line=3)
    mock1.reset_called()

    updateSettings.handleKey('y')
    assert(updateSettings.subState == 2)

    updateSettings.loop()
    mock1.assert_called_with("Press any to cont.", line=3)
    mock1.reset_called()

    updateSettings.handleKey('a')
    assert(updateSettings.subState == 3)

    updateSettings.loop()
    mock1.assert_called_with("(y/n)", line=3)
    mock1.reset_called()

    updateSettings.handleKey('y')
    assert(updateSettings.subState == 4)

    updateSettings.loop()
    assert(updateSettings.values['vol_in_pump'] == 5.5)

    updateSettings.handleKey('a')

    updateSettings.loop()
    mock1.assert_called_with("Press any to cont.", line=3)

    updateSettings.handleKey('a')
    assert mock3.called
