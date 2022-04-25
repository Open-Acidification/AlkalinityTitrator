from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.test_mode.TestMode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import LCD
from titration.utils.UIState.test_mode.Pump import Pump

# Test handleKey
@mock.patch.object(Pump, "_setNextState")
def test_handleKey(mock):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.handleKey("0")
    assert(pump.values['p_direction'] == "0")
    assert(pump.subState == 2)

    pump.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.handleKey("1")
    assert(pump.values['p_direction'] == "1")
    assert(pump.subState == 2)

    pump.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD, 'lcd_out')
@mock.patch.object(LCD, 'read_user_value', return_value=5.5)
def test_loop(mock1, mock2):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

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
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    assert(pump.values['p_volume'] == 5.5)
    mock2.assert_has_calls(
        [mock.call("In/Out (0/1):", line=1)]
    )
    mock2.reset_called()

    pump.handleKey("0")
    assert(pump.values['p_direction'] == "0")
    assert(pump.subState == 2)

    pump.loop()
    mock2.assert_has_calls(
        [mock.call("Pumping volume", line=1),
        mock.call("Press any to cont.", line=3)]
    )

    pump.handleKey("0")
    mock3.assert_called_with(ANY, True)
    assert(mock3.call_args.args[0].name() == "TestMode")
    mock3.reset_mock()
