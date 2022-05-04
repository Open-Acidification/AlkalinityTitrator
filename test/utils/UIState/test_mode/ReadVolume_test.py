from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface, constants
from titration.utils.UIState.test_mode.ReadVolume import ReadVolume
from titration.utils.UIState.test_mode.TestMode import TestMode

# Test handleKey
@mock.patch.object(ReadVolume, "_setNextState")
def test_handleKey(mock):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, 'lcd_out')
def test_loop(mock1):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.loop()
    mock1.assert_has_calls(
        [mock.call("Pump Vol: ", line=1),
        mock.call(
            "{0:1.2f}".format(constants.volume_in_pump),
            style=constants.LCD_CENT_JUST,
            line=2,
        ),
        mock.call("Press any to cont.", line=3)]
    )

# Test ReadVolume
@mock.patch.object(ReadVolume, "_setNextState")
@mock.patch.object(LCD_interface, 'lcd_out')
def test_ReadVolume(mock1, mock2):
    readVolume = ReadVolume(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readVolume.loop()
    mock1.assert_has_calls(
        [mock.call("Pump Vol: ", line=1),
        mock.call(
            "{0:1.2f}".format(constants.volume_in_pump),
            style=constants.LCD_CENT_JUST,
            line=2,
        ),
        mock.call("Press any to cont.", line=3)]
    )

    readVolume.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "TestMode")
    mock2.reset_mock()
