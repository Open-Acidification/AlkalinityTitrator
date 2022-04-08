from asyncore import read
from unittest import mock
from titration.utils.titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.ReadValues import ReadValues

# Test handleKey
@mock.patch.object(ReadValues, "_setNextState")
def test_handleKey(mock):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.handleKey(1)
    assert mock.called

# Test loop
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(interfaces, 'delay')
def test_loop(mock1, mock2):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.loop()
    assert mock1.called_with(readValues.values['timeStep'])
    for i in range(readValues.values['numVals']):
        mock2.assert_has_calls(
            [mock.call("Temp: {0:>4.3f} C".format(readValues.values['temp']), line=1),
            mock.call("Res:  {0:>4.3f} Ohms".format(readValues.values['res']), line=2),
            mock.call("pH:   {0:>4.5f} pH".format(readValues.values['pH_reading']), line=3),
            mock.call("pH V: {0:>3.4f} mV".format(readValues.values['pH_volts'] * 1000), line=4),
            mock.call("Reading: {}".format(i), 1, console=True)]
        )
    mock2.reset_called()
    mock2.assert_has_calls(
        [mock.call("Press any to cont.", line=1)]
    )

# Test ReadValues
@mock.patch.object(ReadValues, "_setNextState")
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(interfaces, 'delay')
def test_ReadValues(mock1, mock2, mock3):
    readValues = ReadValues(Titrator(), Titrator())

    readValues.loop()
    assert mock1.called_with(readValues.values['timeStep'])
    for i in range(readValues.values['numVals']):
        mock2.assert_has_calls(
            [mock.call("Temp: {0:>4.3f} C".format(readValues.values['temp']), line=1),
            mock.call("Res:  {0:>4.3f} Ohms".format(readValues.values['res']), line=2),
            mock.call("pH:   {0:>4.5f} pH".format(readValues.values['pH_reading']), line=3),
            mock.call("pH V: {0:>3.4f} mV".format(readValues.values['pH_volts'] * 1000), line=4),
            mock.call("Reading: {}".format(i), 1, console=True)]
        )
    mock2.reset_called()
    mock2.assert_has_calls(
        [mock.call("Press any to cont.", line=1)]
    )

    readValues.handleKey(1)
    assert mock3.called
