from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.ToggleTestMode import ToggleTestMode

# Test handleKey
@mock.patch.object(ToggleTestMode, "_setNextState")
def test_handleKey(mock):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock1):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.loop()
    mock1.assert_has_calls(
        [mock.call("Testing: {}".format(constants.IS_TEST), line=1),
        mock.call("Press any to cont.", line=3)]
    )

# Test ToggleTestMode
@mock.patch.object(ToggleTestMode, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
def test_ToggleTestMode(mock1, mock2):
    toggleTestMode = ToggleTestMode(Titrator(), Titrator())

    toggleTestMode.loop()
    mock1.assert_has_calls(
        [mock.call("Testing: {}".format(constants.IS_TEST), line=1),
        mock.call("Press any to cont.", line=3)]
    )

    toggleTestMode.handleKey(1)
    assert mock2.called

