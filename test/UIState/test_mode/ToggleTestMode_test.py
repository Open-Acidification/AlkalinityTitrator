from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
from titration.utils.UIState.test_mode.ToggleTestMode import ToggleTestMode

# Test handleKey
@mock.patch.object(ToggleTestMode, "_setNextState")
def test_handleKey(mock):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.loop()
    assert mock.called_with("Press any to cont.", line=3)

# Test ToggleTestMode
@mock.patch.object(ToggleTestMode, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
def test_ToggleTestMode(mock1, mock2):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.loop()
    assert mock1.called_with("Press any to cont.", line=3)

    toggleTestMode.handleKey(1)
    assert mock2.called

