from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
from titration.utils.UIState.test_mode.ReadValues import ReadValues

# Test handleKey
@mock.patch.object(ReadValues, "_setNextState")
def test_handleKey(mock):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, 'lcd_out')
@mock.patch.object(interfaces, 'delay')
def test_loop(mock1, mock2):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.loop()
    assert mock1.called_with(readValues.values['timeStep'])
    assert mock2.called_with("Press any to cont.", line=1)

# Test ReadValues
@mock.patch.object(ReadValues, "_setNextState")
@mock.patch.object(interfaces, 'lcd_out')
@mock.patch.object(interfaces, 'delay')
def test_ReadValues(mock1, mock2, mock3):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.loop()
    assert mock1.called_with(readValues.values['timeStep'])
    assert mock2.called_with("Press any to cont.", line=1)

    readValues.handleKey(1)
    assert mock3.called
