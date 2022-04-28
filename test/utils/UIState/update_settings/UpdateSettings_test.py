from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils.UIState.update_settings.UpdateSettings import UpdateSettings
from titration.utils import LCD

# Test handleKey
@mock.patch.object(UpdateSettings, "_setNextState")
def test_handleKey(mock):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.handleKey("y")
    assert(updateSettings.subState == 2)

    updateSettings.handleKey("1")
    assert(updateSettings.subState == 3)

    updateSettings.handleKey("y")
    assert(updateSettings.subState == 4)

    updateSettings.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.handleKey("n")
    assert(updateSettings.subState == 3)

    updateSettings.handleKey("n")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")

# Test loop
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock1, mock2):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Reset calibration", line=1), 
        mock.call("settings to default?", line=2),
        mock.call("(y/n)", line=3),
    ])
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Default constants", line=1), 
        mock.call("restored", line=2),
        mock.call("Press any to cont.", line=3),
    ])    
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Set volume in pump?", line=1), 
        mock.call("(y/n)", line=3)
    ])    
    mock1.reset_called()

    updateSettings.subState += 1
    updateSettings.loop()
    mock2.assert_called_with("Volume in pump: ")
    mock2.reset_called()
    assert(updateSettings.values['vol_in_pump'] == 5.5)

    updateSettings.subState += 1
    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Volume in pump set", line=1), 
        mock.call("Press any to cont.", line=3)
    ])    

# Test UpdateSettings
@mock.patch.object(LCD, "read_user_value", return_value=5.5)
@mock.patch.object(UpdateSettings, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
def test_PrimePump(mock1, mock2, mock3):
    updateSettings = UpdateSettings(Titrator(), MainMenu(Titrator()))

    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Reset calibration", line=1), 
        mock.call("settings to default?", line=2),
        mock.call("(y/n)", line=3),
    ])
    mock1.reset_called()

    updateSettings.handleKey("y")
    assert(updateSettings.subState == 2)

    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Default constants", line=1), 
        mock.call("restored", line=2),
        mock.call("Press any to cont.", line=3),
    ])
    mock1.reset_called()

    updateSettings.handleKey("1")
    assert(updateSettings.subState == 3)

    updateSettings.loop()
    mock1.assert_has_calls(
        [mock.call("Set volume in pump?", line=1), 
        mock.call("(y/n)", line=3)
    ])
    mock1.reset_called()

    updateSettings.handleKey("y")
    assert(updateSettings.subState == 4)

    updateSettings.loop()
    mock3.assert_called_with("Volume in pump: ")
    mock3.reset_called()
    assert(updateSettings.values['vol_in_pump'] == 5.5)

    mock1.assert_has_calls(
        [mock.call("Volume in pump set", line=1), 
        mock.call("Press any to cont.", line=3)
    ])

    updateSettings.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "MainMenu")
