from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu 
from titration.utils.UIState.test_mode.TestMode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface, constants
from titration.utils.UIState.test_mode.ToggleTestMode import ToggleTestMode

# Test handleKey
@mock.patch.object(ToggleTestMode, "_setNextState")
def test_handleKey(mock):
    toggleTestMode = ToggleTestMode(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    toggleTestMode.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(mock1):
    toggleTestMode = ToggleTestMode(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    toggleTestMode.loop()
    mock1.assert_has_calls(
        [mock.call("Testing: {}".format(constants.IS_TEST), line=1),
        mock.call("Press any to cont.", line=3)]
    )

# Test ToggleTestMode
@mock.patch.object(ToggleTestMode, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_ToggleTestMode(mock1, mock2):
    toggleTestMode = ToggleTestMode(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    toggleTestMode.loop()
    mock1.assert_has_calls(
        [mock.call("Testing: {}".format(constants.IS_TEST), line=1),
        mock.call("Press any to cont.", line=3)]
    )

    toggleTestMode.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "TestMode")
    mock2.reset_mock()
