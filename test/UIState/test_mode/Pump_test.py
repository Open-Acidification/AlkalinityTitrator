from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.Pump import Pump

# Test handleKey
@mock.patch.object(Pump, "_setNextState")
def test_handleKey(mock):
    pump = Pump(Titrator(), Titrator())

    pump.handleKey(0)
    assert(pump.values['p_direction'] == 0)
    assert(pump.subState == 2)

    pump.handleKey(0)
    assert mock.called

    pump = Pump(Titrator(), Titrator())

    pump.handleKey(1)
    assert(pump.values['p_direction'] == 1)
    assert(pump.subState == 2)

    pump.handleKey(0)
    assert mock.called

# Test loop
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_loop(mock1, mock2):
    pump = Pump(Titrator(), Titrator())

    pump.loop()
    assert(pump.values['p_volume'] == 5.5)
    mock2.assert_has_calls(
        [mock.call("In/Out (0/1):", line=1)]
    )
    mock2.reset_called()
    
    pump.subState += 1
    pump.loop()
    mock2.assert_has_calls(
        [mock.call("Pumping volume", line=1),
        mock.call("Press any to cont.", line=3)]
    )

# Test Pump
@mock.patch.object(Pump, "_setNextState")
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_Pump(mock1, mock2, mock3):
    pump = Pump(Titrator(), Titrator())

    pump.loop()
    assert(pump.values['p_volume'] == 5.5)
    mock2.assert_has_calls(
        [mock.call("In/Out (0/1):", line=1)]
    )
    mock2.reset_called()

    pump.handleKey(0)
    assert(pump.values['p_direction'] == 0)
    assert(pump.subState == 2)

    pump.loop()
    mock2.assert_has_calls(
        [mock.call("Pumping volume", line=1),
        mock.call("Press any to cont.", line=3)]
    )

    pump.handleKey(0)
    assert mock3.called
