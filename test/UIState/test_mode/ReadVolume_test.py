from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.ReadVolume import ReadVolume

# Test handleKey
@mock.patch.object(ReadVolume, "_setNextState")
def test_handleKey(mock):
    readVolume = ReadVolume(Titrator(), Titrator())

    readVolume.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(LCD, 'lcd_out')
def test_loop(mock1):
    readVolume = ReadVolume(Titrator(), Titrator())

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
@mock.patch.object(LCD, 'lcd_out')
def test_ReadVolume(mock1, mock2):
    readVolume = ReadVolume(Titrator(), Titrator())

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

    readVolume.handleKey(1)
    assert mock2.called
